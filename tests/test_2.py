import os.path
from page_loader.page_loader import download
from page_loader.page_loader import get_link
from page_loader.page_loader import is_content_and_local
from page_loader.page_loader import convert_filename
from os import listdir
import tempfile
import sys
import requests
import pytest
from bs4 import BeautifulSoup


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


def test_get_link():
    html_doc = '<link href="page-loader-hexlet-repl-co_files/' \
               'page-loader-hexlet-repl-co-assets-application.css"' \
               ' media="all" rel="stylesheet">'
    soup = BeautifulSoup(html_doc, 'html.parser')
    tag = soup.link
    link = 'page-loader-hexlet-repl-co_files/' \
           'page-loader-hexlet-repl-co-assets-application.css'
    assert get_link(tag) == link


def test_id_content_and_local():
    resources = [
        ("/assets/application.css", True),
        ("/courses", True),
        ("/professions/nodejs", True),
        ("/professions/nodejs", True),
        ("https://page-loader.hexlet.repl.co/professions/nodejs", True),
        ("https://pageloader.hexlet.repl.co/professions/nodejs", False),
        ("https://pageloader.hexlet.repl.co/", False)
    ]
    for res in resources:
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
