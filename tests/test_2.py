import os.path
from page_loader.page_loader import download
import tempfile
import sys
from os import listdir


def test():
    link = 'https://page-loader.hexlet.repl.co/'
    with open('tests/fixtures/page-loader-hexlet-repl-co.html') as f1:
        response = f1.read()
    with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
        print('created temporary directory', tmpdir)
        with open(download(link, tmpdir)) as f2:
            downloaded = f2.read()
        with open(os.path.join(sys.path[2], 'logs.log')) as file:
            logs = file.read()
        print(logs)
        assert response == downloaded
        assert len(listdir(os.path.join(
            sys.path[0], 'fixtures/page-loader-hexlet-repl-co_files'))) ==\
            len(listdir(os.path.join(
                tmpdir, 'page-loader-hexlet-repl-co_files')))
