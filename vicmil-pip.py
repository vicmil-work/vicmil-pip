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

    if not os.path.exists(vicmil_pip_path+ "/__init__.py"):
        with open(vicmil_pip_path + "/__init__.py", "w") as _: # Create the file
            pass

    with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil-work/vicmil-pip/refs/heads/main/vicmil-installer.py') as f:
        html = f.read().decode('utf-8')
        with open(vicmil_pip_path + "/installer.py", "w") as install_file: # Create install file
            install_file.write(html)

def installer_exists():
    vicmil_pip_path = path_traverse_up(__file__, 0) + "/vicmil_pip"
    if os.path.exists(vicmil_pip_path + "/installer.py"):
        return True
    return False


if __name__ == "__main__":
    arguments: list = sys.argv[1:]
    print(arguments)

    if arguments[0] == "install":
        if not installer_exists():
            install_installer()

        import vicmil_pip.installer

        if len(arguments) > 1:
            vicmil_pip.installer.install(arguments[1])
        
    if arguments[0] == "update":
        install_installer()

    if arguments[0] == "list":
        pass # Not implemented yet
    if arguments[0] == "remove":
        pass # Not implemented yet
    if arguments[0] == "help":
        help_str = \
"""
vicmil-pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

Visit vicmil.uk/docs for general info
(not added yet) Visit vicmil.uk/package for more info about packages

Commands:
python vicmil.py help // prints help and info
(not added yet) python vicmil.py update // updates vicmil.py to latest version
(not added yet) python vicmil.py list // lists installed vicmil packages
(not added yet) python vicmil.py install -r vicmil-requirements.txt // install all vicmil packages from file
(not added yet) python vicmil.py remove … // remove a package

// Instructions
(not added yet) python vicmil.py install gcc // explains how to install gcc

// Util
(not added yet) python vicmil.py install util-pysetup // usefull for setting up projects
(not added yet) python vicmil.py install util-hpp // util files for c++
(not added yet) python vicmil.py install util-mkdocs // util files for setting up mkdocs to write documentation 
(not added yet) python vicmil.py install cpp-build // build c++ projects using python 

// Other Code/libraries
(not added yet) python vicmil.py install opengl // c++ graphics library
(not added yet) python vicmil.py install SDL2 // c++ graphics library
(not added yet) python vicmil.py install socketIO // c++ networking 
(not added yet) python vicmil.py install emscripten // c++ web compiler
(not added yet) python vicmil.py install stb // c++ load images and fonts
(not added yet) python vicmil.py install glm // c++ linear algebra
(not added yet) python vicmil.py install miniz // c++ zip
(not added yet) python vicmil.py install tiny-obj-loader // c++ load obj files

// Assets
(not added yet) python vicmil.py install vit-b // segmentation model for python
(not added yet) python vicmil.py install roboto-mono // font
(not added yet) python vicmil.py install obj-model // example obj model
"""
        print(help_str)