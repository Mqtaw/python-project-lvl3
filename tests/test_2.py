import os.path
from page_loader.page_loader import download
from page_loader.page_loader import is_content_and_local
from page_loader.page_loader import convert_filename
from os import listdir
import tempfile
import sys
import requests
import pytest


@pytest.fixture
def response():
    with open('tests/fixtures/orig_page-loader-hexlet-repl-co.html') as f1:
        response = f1.read()
    return response


@pytest.fixture
def expect_html():
    with open('tests/fixtures/page-loader-hexlet-repl-co.html') as f1:
        response = f1.read()
    return response


def test_download(requests_mock, response, expect_html):
    link = 'https://page-loader.hexlet.repl.co/'
    resources = [
        "https://page-loader.hexlet.repl.co/assets/application.css",
        "https://page-loader.hexlet.repl.co/courses",
        "https://page-loader.hexlet.repl.co/assets/professions/nodejs.png",
        "https://page-loader.hexlet.repl.co/professions/nodejs",
        "https://page-loader.hexlet.repl.co/script.js",
    ]

    requests_mock.get(link, text=response)
    for res in resources:
        requests_mock.get(res, text='text')

    with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
        print('created temporary directory', tmpdir)
        with open(download(link, tmpdir)) as f2:
            downloaded = f2.read()

        # logging
        with open(os.path.join(sys.path[2], 'logs.log')) as file:
            logs = file.read()
        print(logs)

        assert expect_html == downloaded
        assert len(listdir(os.path.join(
            sys.path[0],
            'fixtures/page-loader-hexlet-repl-co_files'))) ==\
            len(listdir(os.path.join(
                tmpdir, 'page-loader-hexlet-repl-co_files')))


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


def test_exception_ConnectionError2(requests_mock):
    link = 'https://page-loader.hexlet.repl.co/'
    requests_mock.get(link, status_code=404)
    with pytest.raises(Exception):
        download('https://page-loader.hexlet.repl.co/')


def test_is_content_and_local():
    resources = [
        ("https://page-loader.hexlet.repl.co/assets/application.css", True),
        ("https://page-loader.hexlet.repl.co/courses", True),
        ("https://page-loader.hexlet.repl.co/professions/nodejs", True),
        ("https://pageloader.hexlet.repl.co/professions/nodejs", False),
        ("https://pageloader.hexlet.repl.co/", False)
    ]
    for res in resources:
        print(res)
        assert is_content_and_local(
            res[0], 'page-loader.hexlet.repl.co') == res[1]


def test_convert_filename():
    converted_name = convert_filename(
        'https://page-loader.hexlet.repl.co', output='/var/tmp')
    expected = '/var/tmp/page-loader-hexlet-repl-co.html'
    assert converted_name == expected

    converted_name = convert_filename(
        'https://page-loader.hexlet.repl.co/assets/application.css')
    expected = 'page-loader-hexlet-repl-co-assets-application.css'
    assert converted_name == expected
