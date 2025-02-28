"""
This is the installer that contains all information for how to install things
"""

import platform
import requests
import zipfile
import os
import pathlib
import shutil
import importlib
import sys

def get_directory_path(__file__in, up_directories):
    return str(pathlib.Path(__file__in).parents[up_directories].resolve()).replace("\\", "/")


def delete_file(file: str):
    if os.path.exists(file):
        os.remove(file)


def delete_folder_with_contents(file: str):
    if os.path.exists(file):
        shutil.rmtree(file)  # Deletes the folder and its contents


def unzip_file(zip_file: str, destination_folder: str):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)


def go_to_url(url: str):
    # Opens the webbrowser with the provided url
    import webbrowser
    webbrowser.open(url, new=0, autoraise=True)


def python_virtual_environment(env_directory_path):
    # Setup a python virtual environmet
    os.makedirs(env_directory_path, exist_ok=True) # Ensure directory exists
    my_os = platform.system()
    if my_os == "Windows":
        os.system(f'python -m venv "{env_directory_path}"')
    else:
        os.system(f'python3 -m venv "{env_directory_path}"')


def pip_install_packages_in_virtual_environment(env_directory_path, packages):
    if not os.path.exists(env_directory_path):
        print("Invalid path")
        raise Exception("Invalid path")
  
    my_os = platform.system()
    for package in packages:
        if my_os == "Windows":
            os.system(f'powershell; &"{env_directory_path}/Scripts/pip" install {package}')
        else:
            os.system(f'"{env_directory_path}/bin/pip" install {package}')


def get_site_packages_path(venv_path):
    """Returns the site-packages path for a given virtual environment."""
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    
    # Construct the expected site-packages path
    if os.name == "nt":  # Windows
        site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
    else:  # macOS/Linux
        site_packages_path = os.path.join(venv_path, "lib", python_version, "site-packages")

    return site_packages_path if os.path.exists(site_packages_path) else None


def use_other_venv_if_missing(package_name, other_venv_path):
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name} is already installed in the current environment.")
    except ImportError:
        print(f"⚠️ {package_name} not found. Using the package from the other environment.")
        other_venv_path = get_site_packages_path(other_venv_path)
        print(other_venv_path)
        sys.path.insert(0, other_venv_path)  # Add other venv's site-packages to sys.path


class GoogleDriveZipPackage:
    def __init__(self, drive_url, large=False):
        self.drive_url = drive_url
        self.large = large # large packages require special treatment using a library called gdown

    def _download_file_from_google_drive(self, id, destination):
        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value

            return None

        def save_response_content(response, destination):
            CHUNK_SIZE = 32768

            with open(destination, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)

        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = get_confirm_token(response)

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)

        save_response_content(response, destination)    

    def _download_large_file_from_google_drive(self, id, destination):
        use_other_venv_if_missing("gdown", get_directory_path(__file__, 0) + "/venv")
        import gdown
        # Construct the direct URL
        url = f"https://drive.google.com/uc?id={id}"

        # Download the file
        gdown.download(url, destination, quiet=False)


    def _extract_id_from_url(self, url: str):
        url2 = url.split("drive.google.com/file/d/")[1]
        file_id = url2.split("/")[0]
        return file_id


    def _download_file_and_unzip(self, url: str):
        # Setup where the file should be downloaded
        temp_zip: str = get_directory_path(__file__, 0) + "/temp.zip"
        dest_folder: str = get_directory_path(__file__, 0)

        # Download zip from google drive
        file_id = self._extract_id_from_url(url)
        print("Downloading package...")
        if not self.large:
            self._download_file_from_google_drive(file_id, destination=temp_zip)
        else:
            self._download_large_file_from_google_drive(file_id, destination=temp_zip)

        if not os.path.exists(temp_zip):
            raise Exception("ERROR: download failed!")

        # Unzip file to folder and delete zip
        print("unzipping package...")
        try:
            unzip_file(zip_file=temp_zip, destination_folder=dest_folder)
        except Exception as e:
            print("ERROR: download failed!")
            print(e)
        delete_file(temp_zip)

    def install(self):
        print("Installing package from google drive")
        self._download_file_and_unzip(self.drive_url)
    


class ManualInstallFromWebpage:
    def __init__(self, url):
        self.url = url

    def install(self):
        print("Manual installation required: A page with instructions should have opened")
        go_to_url(self.url)


package_info = \
"""
// Instructions
(not added yet) python vicmil.py install gcc // explains how to install gcc

// Util
(not added yet) python vicmil.py install util-pysetup // usefull for setting up projects
(not added yet) python vicmil.py install util-hpp // util files for c++
(not added yet) python vicmil.py install util-mkdocs // util files for setting up mkdocs to write documentation 
(not added yet) python vicmil.py install cpp-build // build c++ projects using python 

// Other Code/libraries
(not added yet) python vicmil.py install SDL2-opengl // c++ graphics library
(not added yet) python vicmil.py install socketIO // c++ networking 
(not added yet) python vicmil.py install emscripten // c++ web compiler
python vicmil.py install stb // c++ load images and fonts
(not added yet) python vicmil.py install glm // c++ linear algebra
python vicmil.py install miniz // c++ zip
(not added yet) python vicmil.py install tiny-obj-loader // c++ load obj files

// Assets
(not added yet) python vicmil.py install vit-b // segmentation model for python
(not added yet) python vicmil.py install roboto-mono // font
(not added yet) python vicmil.py install obj-model // example obj model
"""

package_general = {
    "stb":  GoogleDriveZipPackage("https://drive.google.com/file/d/1e3W8Zlyajzh-3W5CNYjxxbOJtaqBAgVP/view?usp=drive_link"),
    "miniz": GoogleDriveZipPackage("https://drive.google.com/file/d/16YkWE2GwYB8gQxQmmEJOQ2fwyjcAnh3S/view?usp=drive_link"),
    "glm": GoogleDriveZipPackage("https://drive.google.com/file/d/1_HlE1QI6W6X_NNZzTZE5YdeFcRXNa8Ei/view?usp=drive_link"),
    "tiny-obj-loader": GoogleDriveZipPackage("https://drive.google.com/file/d/1PLCBebGr_kuzzxSbUnJgJN8O6Kn_fpL9/view?usp=drive_link"),
    "socket.io-client-cpp": GoogleDriveZipPackage("https://drive.google.com/file/d/1lH9CF9kTNqbS6BdUKrwcQJybUeWVlzjX/view?usp=drive_link", large=True),
}

package_windows = {
    "gcc": ManualInstallFromWebpage("https://code.visualstudio.com/docs/cpp/config-mingw"),
    "emsdk": GoogleDriveZipPackage("https://drive.google.com/file/d/1bYu_jhoHGCNVD9WTA79SoBsj9NAESYsw/view?usp=drive_link", large=True),
    "sdl-opengl": GoogleDriveZipPackage("https://drive.google.com/file/d/1RJS3ciVAHyfCJ8btsjTx6I5ArHYfOczG/view?usp=drive_link", large=True),
}

package_linux = {
    "gcc": ManualInstallFromWebpage("https://medium.com/@adwalkz/demystifying-development-a-guide-to-build-essential-in-ubuntu-for-seamless-software-compilation-b590b5a298bb"),
    "emsdk": GoogleDriveZipPackage("https://drive.google.com/file/d/1YJOSAtA0lOfuWHxL6ZxptuoHlZliXsin/view?usp=drive_link", large=True),
    "sdl-opengl": ManualInstallFromWebpage("https://github.com/vicmil-work/docs_common/blob/master/docs_common/docs/cpp_opengl.md"),
}

def list_packages():
    dirs = os.listdir(get_directory_path(__file__, 0))           
    folders = list()
    for f in dirs:
        if not os.path.isdir(os.path.join(get_directory_path(__file__, 0), f)):
            continue
        if f == "__pycache__":
            continue
        folders.append(f)

    print(f"found {len(folders)} installed packages")
    print(folders)

def remove(package_name: str):
    if os.path.exists(get_directory_path(__file__, 0) + f"/{package_name}"):
        print(f"Removing package {package_name}")
        delete_folder_with_contents(get_directory_path(__file__, 0) + f"/{package_name}")
        print("Done!")
    else:
        print(f"Could not remove package. Package {package_name} does not exist")


def force_install(package_name: str):
    if os.path.exists(get_directory_path(__file__, 0) + f"/{package_name}"):
        print("Removing old installation...")
        delete_folder_with_contents(get_directory_path(__file__, 0) + f"/{package_name}")

    platform_name = platform.system()
    if package_name in package_general.keys():
        print(f"Installing {package_name}...")
        package_general[package_name].install()
        print(f"Successfully installed {package_name}")

    elif platform_name == "Windows" and package_name in package_windows.keys():
        print(f"Installing {package_name}...")
        package_windows[package_name].install()
        print(f"Successfully installed {package_name}")

    elif platform_name == "Linux" and package_name in package_linux.keys():
        print(f"Installing {package_name}...")
        package_linux[package_name].install()
        print(f"Successfully installed {package_name}")

    else:
        package_not_found = \
f"""
Could not find package: {package_name}
Try running:
python vicmil-pip.py update
    or
python3 vicmil-pip.py update
"""
        print(package_not_found)


def install(package_name: str, debug=True):
    if os.path.exists(get_directory_path(__file__, 0) + f"/{package_name}"):
        if debug:
            package_already_exists = \
f"""
package {package_name} already exists!

If really want to install the package again, use
python vicmil-pip.py force-install {package_name} 
    or
python3 vicmil-pip.py force-install {package_name} 
"""
            print(package_already_exists)
        else:
            print(f"package {package_name} already exists!")
        return
    else:
        force_install(package_name)

    