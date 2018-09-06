"""This is a command-line program to download remote files.

In essence it is just a wrapper around `wget`. That is, you have to have `wget`
installed on your system otherwise it wont work.

Usage:
    python download.py <url> | --use-config
"""

import os
import sys
import json
import shutil


def download(url):
    file_name = os.path.basename(url)
    if os.path.isfile(file_name):
        print(f'File: {file_name} already exists.')
    else:
        os.system(f'wget {url}')
        print(f'Downloaded file: {file_name}')


def get_url_from_config_file():
    with open('links.json') as fp:
        contents = json.load(fp)
    return contents['url']


if __name__ == '__main__':
    if not shutil.which('wget'):
        print('Error: you have to have wget installed to use this program.')
        sys.exit(1)

    if len(sys.argv) == 2:
        if sys.argv[-1] == '--use-config':
            url = get_url_from_config_file()
        else:
            url = sys.argv[-1]
        download(url)
    else:
        print(__doc__)
        sys.exit(1)
