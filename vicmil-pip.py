"""
# Info
vicmil-pip is a package manager for installing things, much like pip in python
(but with other things such as utility files and other things that may not be related to python)

# Getting started
python vicmil-pip.py help 
    or
python3 vicmil-pip.py help 

# Documentation
https://vicmil.uk/packages



# More details
When you install something, a map called vicmil/ will be created, where all packages
    you install will be stored. Nothing external will be installed on your computer.

The idea is for all the packages to be cross-platform(windows, linux, mac), so the thing
    you actually install may vary depending on platform. The idea is for all packages to
    use a permissive licence, so they can be used in commercial applications. Read more
    about specific packages at: https://vicmil.uk/packages

You can also opt-out of using vicmil-lib but still use the packages by navigating to
    https://vicmil.uk/packages, there you will find install instructions for installing
    the packages manually and read more about where they came from.

This is the main file, and the only thing you need to use vicmil-pip
"""

import sys

if __name__ == "__main__":
    arguments: list = sys.argv[1:]
    print(arguments)
    if arguments[0] == "install":
        pass # Not implemented yet
    if arguments[0] == "update":
        pass # Not implemented yet
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