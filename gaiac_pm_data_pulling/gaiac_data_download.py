import requests
import sys

def download_files_from_server(urls):
    """
    Function to download files from a FastAPI server.

    Args:
        ip (str): The IP address of the FastAPI server.
        file_names (list): List of file names to download.

    Returns:
        None
    """
    for url in urls:
        file_name = url.split('/')[len(url.split('/'))-1]
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{file_name}", "wb") as f:
                f.write(response.content)
            print(f"File {file_name} downloaded successfully!")
        else:
            print(f"Failed to download {file_name}. Status code: {response.status_code}")

if __name__=="__main__":

    if len(sys.argv) > 1:
        files  = sys.argv[1].split(',')
        download_files_from_server( files)