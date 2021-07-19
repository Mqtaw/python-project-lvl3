from page_loader.page_loader import get_link
from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def response():
    with open('tests/fixtures/for_ref_page-loader-hexlet-repl-co.html') as f1:
        response = f1.read()
    return response


def test_get_link(response):
    link = 'https://page-loader.hexlet.repl.co/dir'
    results = [
        'https://page-loader.hexlet.repl.co/assets/application.css',
        'https://page-loader.hexlet.repl.co/courses',
        'https://page-loader.hexlet.repl.co/courses',
        'https://page-loader.hexlet.repl.co/dir/courses',
        'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png',
        'https://page-loader.hexlet.repl.co/script.js',
        'https://hexlet.repl.co/courses'
    ]
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.find_all(['img', 'link', 'script'])
    print(links)
    for i in range(len(links)):
        assert results[i] == get_link(links[i], link)
