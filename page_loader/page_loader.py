import argparse
import requests
import re
import os
from bs4 import BeautifulSoup


def createParser():
    parser = argparse.ArgumentParser(description='Download from link')
    parser.add_argument('link', type=str, help='')
    parser.add_argument('-o', '--output', default='./var/tmp',
                        type=str, help='output path')
    return parser


def download(link, output='/var/tmp'):
    request = requests.get(link)
    path_to_file = convert_filename(link, output)
    print(path_to_file)
    soup = BeautifulSoup(request.text, 'html.parser')
    path_to_resources = os.path.splitext(path_to_file)[0]+'_files'
    os.mkdir(path_to_resources)
    for pic in soup.find_all('img'):
        file_name = os.path.split(pic.get('src'))[-1]
        path_to_resource_pic = os.path.join(path_to_resources, file_name)
        link_to_resource_pic = link + pic.get('src')
        changed_link = os.path.join(os.path.split(path_to_resources)[-1],
                                    file_name)
        r_request = requests.get(link_to_resource_pic)
        with open(path_to_resource_pic, "wb") as f:
            f.write(r_request.content)
        pic['src'] = changed_link
    with open(path_to_file, "w") as f:
        f.write(soup.prettify(formatter="html5"))
    return path_to_file


def convert_filename(link, output):
    scheme_end = re.search('://', link).span()[1]
    link_without_scheme = link[scheme_end:]
    converted_link = re.sub(r'[\W_]', '-', link_without_scheme) + '.html'
    return os.path.join(output, converted_link)
