"""
# Info
vicmil-pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

# Getting started
python vicmil-pip.py help 
    or
python3 vicmil-pip.py help 

# Documentation
https://vicmil.uk/vicmil-pip



# More details
When you install something, a map called vicmil/ will be created, where all packages
    you install will be stored. Nothing external will be installed on your computer.

The idea is for all the packages to be cross-platform(windows, linux, mac), so the thing
    that actually gets installed may vary depending on platform. The idea is for all packages 
    to use a permissive licence, so they can be used in commercial applications. Read more
    about specific packages at: https://vicmil.uk/vicmil-pip

You can also opt-out of using vicmil-pip but still use the packages by navigating to
    https://vicmil.uk/vicmil-pip, there you will find install instructions for installing
    the packages manually and read more about where they came from.

This is the main file, and the only thing you need to use vicmil-pip
"""

import sys
import pathlib
import os
import urllib.request

def path_traverse_up(path: str, count: int) -> str:
    """Traverse the provided path upwards

    Parameters
    ----------
        path (str): The path to start from, tips: use __file__ to get path of the current file
        count (int): The number of directories to go upwards

    Returns
    -------
        str: The path after the traversal, eg "/some/file/path"
    """

    parents = pathlib.Path(path).parents
    path_raw = str(parents[count].resolve())
    return path_raw.replace("\\", "/")

def install_installer():
    vicmil_pip_path = path_traverse_up(__file__, 0) + "/vicmil_pip"
    if not os.path.exists(vicmil_pip_path):
        os.makedirs(vicmil_pip_path, exist_ok=True)

    with open(vicmil_pip_path + "/__init__.py", "w") as _: # Create the init file
        pass

    with open(vicmil_pip_path + "/.gitignore", "w") as file_: # Create the gitignore file
        file_.write("__pycache__*\nvenv/")

    with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil-work/vicmil-pip/refs/heads/main/vicmil_pip/installer.py') as f:
        html = f.read().decode('utf-8')
        with open(vicmil_pip_path + "/installer.py", "w") as install_file: # Create install file
            install_file.write(html)

    if not os.path.exists(vicmil_pip_path+ "/venv"):
        import vicmil_pip.installer
        vicmil_pip.installer.python_virtual_environment(vicmil_pip_path + "/venv")
        vicmil_pip.installer.pip_install_packages_in_virtual_environment(vicmil_pip_path + "/venv", ["gdown"])

def installer_exists():
    vicmil_pip_path = path_traverse_up(__file__, 0) + "/vicmil_pip"
    if os.path.exists(vicmil_pip_path + "/installer.py"):
        return True
    return False

def update_vicmil_pip():
    # Download the latest features into this file
    with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil-work/vicmil-pip/refs/heads/main/vicmil-pip.py') as f:
        html = f.read().decode('utf-8')
        with open(__file__, "w") as this_file: # Create install file
            this_file.write(html)


if __name__ == "__main__":
    arguments: list = sys.argv[1:]
    print(arguments)

    if len(arguments) == 0 or arguments[0] == "help":
        help_str = \
"""
vicmil-pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

(not added yet) Visit https://vicmil.uk/vicmil-pip for more info

Commands:
python3 vicmil-pip.py help // prints help and info
python3 vicmil-pip.py update // updates vicmil.py to latest version
python3 vicmil-pip.py install … // Install a package
python3 vicmil-pip.py remove … // remove a package
python3 vicmil-pip.py install -r vicmil-requirements.txt // install all vicmil packages listed in file
python3 vicmil-pip.py list // lists installed vicmil packages
python3 vicmil-pip.py packages // list all available packages with more info
"""
        print(help_str)
        exit(0)

    if arguments[0] == "install":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        if len(arguments) == 2 and arguments[1] == "-r":
            print("You need to specify a file to install from file")

        if len(arguments) > 2 and arguments[1] == "-r":
            print("Installing from requirements file")
            # open file and iterate through it line by line
            # install each package on each line
            filename = arguments[2]
            try:
                with open(filename, "r") as file:
                    for line in file:
                        vicmil_pip.installer.install(line.strip(), debug=False)

            except FileNotFoundError:
                print(f"Error: The file '{filename}' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

            print("Done!")

        elif len(arguments) > 1:
            vicmil_pip.installer.install(arguments[1])

    if arguments[0] == "force-install":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        if len(arguments) > 1:
            vicmil_pip.installer.force_install(arguments[1])
        
    if arguments[0] == "update":
        print("upgrade vicmil_pip/installer.py")
        install_installer()
        print("upgrade current file")
        update_vicmil_pip()

    if arguments[0] == "remove":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        if len(arguments) > 1:
            vicmil_pip.installer.remove(arguments[1])

    if arguments[0] == "list":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        vicmil_pip.installer.list_packages()

    if arguments[0] == "packages":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        print(vicmil_pip.installer.package_info)
    