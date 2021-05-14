import os.path

from page_loader.page_loader import download
import tempfile
import sys
from os import listdir
from bs4 import BeautifulSoup
import requests
import re
# import requests_mock

def test():
    link = 'https://ru.code-basics.com'
    with open('tests/fixtures/ru-code-basics-com.html') as f1:
        response = f1.read()
    soup = BeautifulSoup(response, 'html.parser')
    response = soup.prettify(formatter="html5")
    sum_of_lines_in_test = len(re.findall(r"[\n']+?", response))


    # requests_mock.get('https://ru.hexlet.io/courses', text='data')
    with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
        print('created temporary directory', tmpdir)
        with open(download(link, tmpdir)) as f2:
            downloaded = f2.read()
            sum_of_lines_in_res = len(re.findall(r"[\n']+?", downloaded))
        assert sum_of_lines_in_test == sum_of_lines_in_res
        assert len(listdir(os.path.join(sys.path[0] ,'fixtures/ru-code-basics-com_files'))) == len(listdir(os.path.join(tmpdir ,'ru-code-basics-com_files')))
