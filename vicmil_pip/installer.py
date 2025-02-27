"""
This is the installer that contains all information for how to install things
"""

import platform
import requests
import zipfile
import os
import pathlib
import shutil

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


class GoogleDriveZipPackage:
    def __init__(self, drive_url):
        self.drive_url = drive_url

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
        self._download_file_from_google_drive(file_id, destination=temp_zip)

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


package_general = {
    "stb": GoogleDriveZipPackage("https://drive.google.com/file/d/1e3W8Zlyajzh-3W5CNYjxxbOJtaqBAgVP/view?usp=drive_link")
}

package_windows = {

}

package_linux = {

}

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


def install(package_name: str):
    if os.path.exists(get_directory_path(__file__, 0) + f"/{package_name}"):
        package_already_exists = \
f"""
package {package_name} already exists!

If really want to install the package again, use
python vicmil-pip.py force-install {package_name} 
    or
python3 vicmil-pip.py force-install {package_name} 
"""
        print(package_already_exists)
        return
    else:
        force_install(package_name)

    