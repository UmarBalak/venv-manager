import os
import sys
import shutil
import subprocess
# import logging

BLACKLIST = ['bin', 'Scripts', 'Recycle.Bin', '$RECYCLE.BIN', "Windows", "Program Files", "Program Files (x86)", "ProgramData"]

def get_python_version(venv_path):
    """
    Get the Python version used in the virtual environment.
    """
    try:
        # Path to the Python executable in the virtual environment
        python_executable = os.path.join(venv_path, 'bin', 'python') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'python.exe')
        
        # Run 'python --version' command
        result = subprocess.run([python_executable, '--version'], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()  # Return Python version
        else:
            return "Unable to retrieve Python version"
    except Exception as e:
        return str(e)
    
def get_installed_packages(venv_path):
    """
    Get the list of installed packages in the virtual environment.
    """
    try:
        # Path to the Python executable in the virtual environment
        python_executable = os.path.join(venv_path, 'bin', 'python') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'python.exe')
        
        # Run 'pip list' command
        result = subprocess.run([python_executable, '-m', 'pip', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()  # Return installed packages list
        else:
            return "Unable to retrieve installed packages"
    except Exception as e:
        return str(e)
    
def display_venv_details(venv_path):
    """
    Display details about the specified virtual environment.
    """
    if not os.path.exists(venv_path) or not os.path.exists(os.path.join(venv_path, 'pyvenv.cfg')):
        print(f"{venv_path} is not a valid virtual environment.")
        return

    # Get Python version and installed packages using existing functions
    python_version = get_python_version(venv_path)
    installed_packages = get_installed_packages(venv_path)

    # Calculate the size of the venv directory
    venv_size = sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(venv_path) for file in files)

    # Print details
    print(f"Details for virtual environment at: {venv_path}")
    print(f"Python Version: {python_version}")
    print("Installed Packages:")
    print(installed_packages if installed_packages else "(No packages installed)")
    print(f"\nSize: {venv_size / (1024 ** 2):.2f} MB")

def find_venvs(root_dir, current_depth, max_depth):
    """
    The function `find_venvs` recursively searches for virtual environments (venvs) within a specified
    directory up to a certain depth.
    
    :param root_dir: The `root_dir` parameter in the `find_venvs` function represents the directory from
    which the search for virtual environments (venvs) will start. It is the starting point for the
    search within the file system
    :param current_depth: The `current_depth` parameter in the `find_venvs` function represents the
    current depth level in the directory structure being searched. It is used to keep track of how deep
    the function has traversed into the directory hierarchy. This parameter is incremented as the
    function recursively searches through directories to avoid exceeding
    :param max_depth: The `max_depth` parameter in the `find_venvs` function represents the maximum
    depth to which the function will search for virtual environments (venvs) within the directory
    structure. If the current depth of the search exceeds this `max_depth`, the function will stop
    searching further into subdirectories
    :return: The function `find_venvs` returns a list of paths to directories that contain a
    `pyvenv.cfg` file within the specified depth limit from the root directory.
    """
    venvs = []

    # If current depth exceeds max depth, stop searching
    if current_depth > max_depth:
        return venvs

    try:
        with os.scandir(root_dir) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    # Skip irrelevant directories
                    if any(entry.path.startswith(root_dir + skip) for skip in BLACKLIST)  or entry.path == root_dir + "\Public":
                        # print(f"Skipping irrelevant directory: {entry.path}")
                        # logging.warning("skipping")
                        continue

                    # Check if 'pyvenv.cfg' exists in this directory
                    if os.path.exists(os.path.join(entry.path, 'pyvenv.cfg')):
                        venvs.append(entry.path)
                    else:
                        # Recursively search in subdirectories, increasing the depth
                        venvs.extend(find_venvs(entry.path, current_depth + 1, max_depth))
    except (PermissionError, FileNotFoundError) as e:
        pass
    return venvs

def list_venvs(base_dirs, max_depth=5):
    """
    List all Python virtual environments across multiple base directories, 
    with a limit on how deep to search.
    """
    all_venvs = []
    
    for base_dir in base_dirs:
        print(f"Checking base directory: {base_dir}")
        if os.path.exists(base_dir):
            venvs = find_venvs(base_dir, current_depth=0, max_depth=max_depth)
            all_venvs.extend(venvs)
        else:
            print(f"Directory does not exist: {base_dir}")

    if not all_venvs:
        print("No virtual environments found.")
    else:
        print("Found virtual environments:")
        for i, venv in enumerate(all_venvs):
            print(f"  {i+1}. {venv}")
        print(f"VENV Count: {len(all_venvs)}")
       
def create_venv(env_name, base_dir=None):
    """
    Create a Python virtual environment in the specified base directory.
    If no base directory is provided, create it in the current directory.
    """
    # Use current directory if base_dir is None or empty
    if not base_dir:
        base_dir = os.getcwd()
    
    venv_path = os.path.join(base_dir, env_name)
    
    if not os.path.exists(base_dir):
        print(f"Base directory does not exist: {base_dir}")
        return
    
    if os.path.exists(venv_path):
        print(f"Virtual environment '{env_name}' already exists in {base_dir}.")
    else:
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(f"Virtual environment '{env_name}' created at {venv_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def delete_venv(venv_path):
    """
    Delete the specified virtual environment.
    """
    if os.path.exists(venv_path):
        # Check if it's a valid virtual environment
        if not os.path.exists(os.path.join(venv_path, 'pyvenv.cfg')):
            print(f"{venv_path} is not a valid virtual environment.")
            return
        
        try:
            shutil.rmtree(venv_path)
            print(f"Virtual environment at {venv_path} deleted.")
        except Exception as e:
            print(f"Error deleting virtual environment: {e}")
    else:
        print(f"Virtual environment not found at {venv_path}.")

def help():
    """
    Display help message explaining how to use the script and its commands.
    """
    help_message = """
    Python Virtual Environment Manager

    Usage:
      vm [command] <args>

    Commands:
      list [base_dir1] [base_dir2] ...   List all virtual environments in the specified directories.
                                         If no directory is provided, it searches the entire filesystem.

      create <env_name> [base_dir]       Create a new virtual environment with the given name.
                                         If base_dir is not provided, the environment is created in the current directory.

      delete <venv_path>                 Delete the virtual environment at the specified path.

      info <venv_path>                   Display information about the specified virtual environment.

      help                                 Display this help message.

    Examples:
      vm list                             Lists all virtual environments in the current directory.
      vm list ~/projects /path/to/another_dir
                                         Lists virtual environments in the specified directories.
      vm create myenv                    Creates a virtual environment named 'myenv' in the current directory.
      vm create myenv ~/projects         Creates 'myenv' in the '~/projects' directory.
      vm delete ~/projects/myenv         Deletes the virtual environment at '~/projects/myenv'.
      vm info ~/projects/myenv           Displays information about the virtual environment at '~/projects/myenv'.
    """
    print(help_message)

def main():
    if len(sys.argv) < 2:
        print("Usage: vm [list|create|delete|info|help] <args>")
        print("  list [base_dir1, base_dir2, ...]     - List all virtual environments in specified directories.")
        print("  create <env_name> [base_dir]         - Create a new virtual environment with the given name.")
        print("  delete <venv_path>                   - Delete the virtual environment at the specified path.")
        print("  info <venv_path>                     - Display information about the specified virtual environment.")
        print("  help                                   - Display this help message.")
        return
    
    command = sys.argv[1].lower()  # Case-insensitive commands
    
    if command == "help":
        help()
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: vm info <venv_path>")
            print("Please provide a path to the virtual environment.")
        else:
            venv_path = sys.argv[2]
            display_venv_details(venv_path)

    elif command == "list":
        base_dirs = sys.argv[2:] if len(sys.argv) > 2 else ['/']
        print("Searching for virtual environments, this may take a while...")
        list_venvs(base_dirs)

    elif command == "create":
        if len(sys.argv) < 3:
            print("Usage: vm create <env_name> [base_dir]")
            print("Please provide a name for the virtual environment.")
        else:
            env_name = sys.argv[2]
            base_dir = sys.argv[3] if len(sys.argv) == 4 else None
            create_venv(env_name, base_dir)
    
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: vm delete <venv_path>")
            print("Please provide the path of the virtual environment to delete.")
        else:
            venv_path = sys.argv[2]
            delete_venv(venv_path)
    
    else:
        print(f"Unknown command: {command}")
        print("Usage: vm [list|create|delete|info|help] <args>")

if __name__ == "__main__":
    main()
