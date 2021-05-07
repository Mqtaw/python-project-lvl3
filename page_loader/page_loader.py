import argparse
import requests
import re
import os


def createParser():
    parser = argparse.ArgumentParser(description='Download from link')
    parser.add_argument('link', type=str, help='')
    parser.add_argument('-o', '--output', default='./var/tmp',
                        type=str, help='output path')
    return parser


def download(link, output='/var/tmp'):
    request = requests.get(link)
    path_to_file = convert_filename(link, output)
    with open(path_to_file, "w") as f:
        f.write(request.text)
        f.close()
    print(path_to_file)
    return path_to_file


def convert_filename(link, output):
    scheme_end = re.search('://', link).span()[1]
    link_without_scheme = link[scheme_end:]
    converted_link = re.sub(r'[\W_]', '-', link_without_scheme) + '.html'
    return os.path.join(output, converted_link)
