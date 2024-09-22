import os
import sys
import shutil
import subprocess

def find_venvs(root_dir):
    """
    Recursively search for Python virtual environments in the given root directory.
    Skips 'bin', 'RECYCLE.BIN', and 'Scripts' folders, only lists venv directories.
    """
    venvs = []
    for root, dirs, files in os.walk(root_dir):
        # Skip irrelevant directories
        if any(skip in root for skip in ['bin', 'Scripts', 'RECYCLE.BIN']):
            continue
        if 'pyvenv.cfg' in files:  # 'pyvenv.cfg' indicates a Python virtual environment
            venvs.append(root)
    return venvs

def list_venvs(base_dirs):
    """
    List all Python virtual environments across multiple base directories.
    """
    all_venvs = []
    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            venvs = find_venvs(base_dir)
            all_venvs.extend(venvs)
        else:
            print(f"Directory does not exist: {base_dir}")

    if not all_venvs:
        print("No virtual environments found.")
    else:
        print("Found virtual environments:")
        for venv in all_venvs:
            print(f"- {venv}")

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
                                         If no directory is provided, it searches the current directory.

      create <env_name> [base_dir]       Create a new virtual environment with the given name.
                                         If base_dir is not provided, the environment is created in the current directory.

      delete <venv_path>                 Delete the virtual environment at the specified path.

    Examples:
      vm list        Lists all virtual environments on the entire system.
      vm list ~/projects /path/to/another_dir
                                         Lists virtual environments in the specified directories.
      vm create myenv
                                         Creates a virtual environment named 'myenv' in the current directory.
      vm create myenv ~/projects
                                         Creates 'myenv' in the '~/projects' directory.
      vm delete ~/projects/myenv
                                         Deletes the virtual environment at '~/projects/myenv'.
    """
    print(help_message)

def main():
    if len(sys.argv) < 2:
        print("Usage: vm [list|create|delete] <args>")
        print("  list [base_dir1, base_dir2, ...]     - List all virtual environments")
        print("  create <env_name> [base_dir]         - Create a virtual environment")
        print("  delete <venv_path>                   - Delete a virtual environment")
        return
    
    command = sys.argv[1].lower()  # Case-insensitive commands
    
    if command == "help":
        help()

    elif command == "list":
        base_dirs = sys.argv[2:] if len(sys.argv) > 2 else ['/']
        print("Searching for virtual environments, this may take a while...")
        list_venvs(base_dirs)
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("Usage: vm create <env_name> [base_dir]")
        else:
            env_name = sys.argv[2]
            base_dir = sys.argv[3] if len(sys.argv) == 4 else None
            create_venv(env_name, base_dir)
    
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: vm delete <venv_path>")
        else:
            venv_path = sys.argv[2]
            delete_venv(venv_path)
    
    else:
        print(f"Unknown command: {command}")
        print("Usage: vm [list|create|delete] <args>")

if __name__ == "__main__":
    main()
