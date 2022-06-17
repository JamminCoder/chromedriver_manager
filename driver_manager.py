import subprocess
import os
import urllib.request
import zipfile
import json

def read(path):
    with open(path, 'r') as f:
        return f.read()

def write(path, contents):
    with open(path, 'w') as f:
        f.write(contents)

def read_json(path):
    return json.loads(read(path))





def is_unix():
    return 'posix' == os.name

def is_windows():
    return 'nt' == os.name

def get_chrome_version():
    windows_check_cmd = 'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value'.split(' ')
    posix_check_cmd = 'google-chrome --version'.split(' ')

    if is_unix():
        # Get chrome version on linux
        output = subprocess.check_output(posix_check_cmd).decode().strip()
        return output.split(' ')[-1].strip()

    if is_windows():
        # Get chrome version on windows
        output = subprocess.check_output(windows_check_cmd).strip()
        return output.split('=')[-1].strip()


    # Line is reached is OS is not supported
    print('Unsupported operating system')
    exit()


def get_platform_folder():
    if is_windows():
        return 'chromedriver_win32.zip'
    
    if is_unix():
        return 'chromedriver_linux64.zip'


def get_output_path():
    username = os.environ.get('USERNAME')
    if is_unix():
        path = f'/home/{username}/chromedriver_linux64/'
        
    if is_windows():
        path = f'C:\\Users\\{username}\\chromedriver_win32\\'

    return path


def download(url, out):
    print(f'Downloading {url}')
    print(f'Outputing to {out}')
    try:
        urllib.request.urlretrieve(url, out)
    except Exception as e:
        print(e)
        print(f'[-] Error! Something went wrong while downloading from {url}')
        exit()

    print('Done.')


def extract(zip_file, output_dir):
    print(f'Extracting {zip_file} contents to {output_dir}...')
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print('Done.')


def get_driver_exec_path():
    if is_windows():
        path = get_output_path() + 'chromedriver.exe'
        if os.path.isfile(path):
            return path

    if is_unix():
        path = get_output_path() + 'chromedriver'
        if os.path.isfile(path):
            return path

    return None


def driver_matches_chrome():
    if not os.path.exists('driver_version.txt'):
        return False

    driver_version = read('driver_version.txt').strip()
    return driver_version == get_chrome_version()




def chrome_driver_should_update():
    print('Checking to see if chrome driver should update...')
    if not driver_matches_chrome():
        print('Can\'t tell if Chrome driver matches Chrome version.')
        return True
    
    if not get_driver_exec_path():
        print('No chrome driver found!')
        return True
    
    return False



def update_chrome_driver():
    chrome_version = get_chrome_version()
    platform_folder = get_platform_folder()
    download_path = platform_folder.replace('.zip', f'-{chrome_version}.zip')
    download_url = f'https://chromedriver.storage.googleapis.com/{chrome_version}/{platform_folder}'
    exec_output_dir = get_output_path()
    if not os.path.exists(exec_output_dir):
        os.mkdir(exec_output_dir)

    download(download_url, download_path)
    extract(download_path, exec_output_dir)

    os.remove(download_path)

    write('driver_version.txt', chrome_version)

    print('Succesfully updated Chrome driver.')
    print(f'Driver stored in {get_driver_exec_path()}')


if __name__ == '__main__':
    if chrome_driver_should_update():
        update_chrome_driver()
