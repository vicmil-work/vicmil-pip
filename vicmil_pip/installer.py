"""
This is the installer that contains all information for how to install things
"""

import platform

package_general = {

}

package_windows = {

}

package_linux = {

}

def _install(package_name: str, package_info):
    print(f"installing package {package_name}")

def install(package_name: str):
    platform_name = platform.system()
    if package_name in package_general.keys():
        pass

    if platform_name == "Windows" and package_name in package_windows.keys():
        pass

    elif platform_name == "Linux" and package_name in package_linux.keys():
        pass
    else:
        package_not_found = \
f"""
Could not find package: {package_name}
Try running:
python vicmil-pip.py update
"""
        print(package_not_found)