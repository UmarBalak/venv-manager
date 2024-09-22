# venv-manager

A command-line tool to manage Python virtual environments across your entire PC. This tool allows you to create, list, and delete virtual environments conveniently.

## Features

- **List virtual environments** in specified directories or throughout the entire PC.
- **Create new virtual environments** in a specified directory or the current directory.
- **Delete existing virtual environments** safely.
- **Display information about virtual environments** in simple way.

## Installation

To install `venv-manager`, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/UmarBalak/venv-manager.git
   cd venv-manager

2. Install the package in editable mode:
    ```bash
    pip install -e .

## Usage
### Command-Line Interface
The tool can be used with the following commands:

* List virtual environments:
    ```bash
    vm list [directory1] [directory2] ...
If no directories are specified, it searches the current working directory.

* Create a new virtual environment:
    ```bash
    vm create <env_name> [base_dir]
If no base directory is provided, it creates the environment in the current directory.

* Delete a virtual environment:
    ```bash
    vm delete <venv_path>

* Display information about a virtual environment:
    ```bash
    vm info <venv_path>
Displays the Python version and installed packages for the specified virtual environment.

### Help Cammand
For detailed usage information, run:
```bash
vm help

