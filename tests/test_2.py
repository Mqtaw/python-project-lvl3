import os.path
from page_loader.page_loader import download
import tempfile
import sys
import requests
import pytest


@pytest.fixture
def response():
    with open('tests/fixtures/page-loader-hexlet-repl-co.html') as f1:
        response = f1.read()
    return response


def test(requests_mock, response):
    link = 'https://page-loader.hexlet.repl.co/'
    requests_mock.get(link, text=response)
    with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
        print('created temporary directory', tmpdir)
        with open(download(link, tmpdir, download_res='no')) as f2:
            downloaded = f2.read()

        # logging
        with open(os.path.join(sys.path[2], 'logs.log')) as file:
            logs = file.read()
        print(logs)

        assert response == downloaded
        # assert len(listdir(os.path.join(
        #    sys.path[0], 'fixtures/page-loader-hexlet-repl-co_files'))) ==\
        #    len(listdir(os.path.join(
        #        tmpdir, 'page-loader-hexlet-repl-co_files')))


def test_exception_FileNotFoundError(requests_mock):
    requests_mock.get('https://page-loader.hexlet.repl.co/', text='response')
    with pytest.raises(FileNotFoundError):
        download('https://page-loader.hexlet.repl.co/', output='nodir')


def test_exception_FileExistsError(requests_mock, response):
    link = 'https://page-loader.hexlet.repl.co/'
    requests_mock.get(link, text=response)
    with pytest.raises(FileExistsError):
        with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
            with open(download(link, tmpdir, download_res='no')) as f2:
                f2.read()
            with open(download(link, tmpdir, download_res='no')) as f2:
                f2.read()


def test_exception_ConnectionError():
    with pytest.raises(requests.exceptions.ConnectionError):
        download('https://page-loaer.hexet.rep.co/', output='nodir')
