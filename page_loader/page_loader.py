import argparse
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from progress.bar import ChargingBar


tags_link = {'img': 'src', 'link': 'href', 'script': 'src'}


def createParser():
    logging.info('parser, start')
    parser = argparse.ArgumentParser(description='Download from link')
    parser.add_argument('link', type=str, help='')
    parser.add_argument('-o', '--output', default='./var/tmp',
                        type=str, help='output path')
    logging.info('parser, finish')
    return parser


def get_link(resource, link):
    if tags_link[resource.name] in resource.attrs:
        res_link = resource.get(tags_link[resource.name])
        main_link_parse = urlparse(link)
        parse = urlparse(res_link)
        if parse.netloc and main_link_parse.netloc != parse.netloc:
            return res_link
        if parse.path[0] == '/':
            path = parse.path
        else:
            path = main_link_parse.path + parse.path if  \
                main_link_parse.path[-1] == '/' else \
                main_link_parse.path + '/' + parse.path

        result = main_link_parse._replace(path=path,
                                          params=parse.params,
                                          query=parse.query,
                                          fragment=parse.fragment)
        return result.geturl()


def is_content_and_local(link, netloc):
    o = urlparse(link)
    if (o.netloc != netloc) or \
            (o.netloc == netloc and o.path == '/'):
        return False
    else:
        return True


def download(link, output='/var/tmp', download_res='yes'):
    link = link[:-1] if link[-1] == '/' else link
    logging.info('download, start')
    request = requests.get(link)
    if request.status_code != 200:
        raise Exception('Status code = {}'.format(request.status_code))
    path_to_file = convert_filename(link, output)
    print(path_to_file)
    soup = BeautifulSoup(request.text, 'html.parser')
    path_to_resources = os.path.splitext(path_to_file)[0] + '_files'
    os.mkdir(path_to_resources)
    logging.info('resource_download, start')
    with open(path_to_file, "w") as f:
        f.write(soup.prettify(formatter="html5"))
    logging.info('download, finish')
    resources = soup.find_all(['img', 'link', 'script'])
    if resources and download_res == 'yes':
        download_resources(resources, path_to_resources, link)
    with open(path_to_file, "w") as f:
        f.write(soup.prettify(formatter="html5"))
    logging.info('download, finish')
    return path_to_file


def download_resources(resources, path_to_resources, link):
    bar = ChargingBar('download resources', max=len(resources))
    for resource in resources:
        res_link = get_link(resource, link)
        if is_content_and_local(res_link, urlparse(link).netloc):
            logging.info('resource: ' + res_link)
            file_name = convert_filename(res_link)
            path_to_resource = os.path.join(path_to_resources, file_name)
            changed_link = os.path.join(os.path.split(path_to_resources)[-1],
                                        file_name)
            r_request = requests.get(res_link)
            with open(path_to_resource, "wb") as f:
                f.write(r_request.content)
            resource[tags_link[resource.name]] = changed_link
        bar.next()
    bar.finish()


def convert_filename(link, output=''):
    scheme_end = re.search('://', link).span()[1]
    if not output:
        link_without_scheme, end_of_link = os.path.splitext(link[scheme_end:])
        end_of_name = '.html' if end_of_link == '' else end_of_link
    else:
        link_without_scheme = link[scheme_end:]
        end_of_name = '.html'
    converted_link = re.sub(r'[\W_]', '-', link_without_scheme) + end_of_name
    return os.path.join(output, converted_link)
