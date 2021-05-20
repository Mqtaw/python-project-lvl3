import argparse
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


tags_link = {'img': 'src', 'link': 'href', 'script': 'src'}


def createParser():
    parser = argparse.ArgumentParser(description='Download from link')
    parser.add_argument('link', type=str, help='')
    parser.add_argument('-o', '--output', default='./var/tmp',
                        type=str, help='output path')
    return parser


def get_link(resource):
    if tags_link[resource.name] in resource.attrs:
        return resource[tags_link[resource.name]]


def is_content_and_local(link, netloc):
    o = urlparse(link)
    if (o.netloc and o.netloc != netloc) or \
            (o.netloc == netloc and o.path == '/'):
        return False
    else:
        return True


def download(link, output='/var/tmp'):
    request = requests.get(link)
    path_to_file = convert_filename(link, output)
    print(path_to_file)
    soup = BeautifulSoup(request.text, 'html.parser')
    path_to_resources = os.path.splitext(path_to_file)[0]+'_files'
    os.mkdir(path_to_resources)
    netloc = urlparse(link).netloc
    for resource in soup.find_all(['img', 'link', 'script']):
        res_link = get_link(resource)
        if res_link and is_content_and_local(res_link, netloc):
            file_name = os.path.split(resource.get(
                tags_link[resource.name]))[-1]
            path_to_resource = os.path.join(path_to_resources, file_name)
            link_to_resource = link + resource.get(tags_link[resource.name])
            # Тут нужно поправить случай. если придет ссылка
            # абсолютная на локальный ресурс
            changed_link = os.path.join(os.path.split(path_to_resources)[-1],
                                        file_name)
            r_request = requests.get(link_to_resource)
            with open(path_to_resource, "wb") as f:
                f.write(r_request.content)
            resource[tags_link[resource.name]] = changed_link
    with open(path_to_file, "w") as f:
        f.write(soup.prettify(formatter="html5"))
    return path_to_file


def convert_filename(link, output):
    scheme_end = re.search('://', link).span()[1]
    link_without_scheme = link[scheme_end:]
    converted_link = re.sub(r'[\W_]', '-', link_without_scheme) + '.html'
    return os.path.join(output, converted_link)
