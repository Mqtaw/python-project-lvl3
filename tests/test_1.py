from page_loader.page_loader import download
import tempfile
import sys
import requests
# import requests_mock

def test():
    link = 'https://ru.code-basics.com'
    with open('tests/fixtures/ru-code-basics-com.html') as f1:
        response = f1.read()
        f1.close()
    # requests_mock.get('https://ru.hexlet.io/courses', text='data')
    with tempfile.TemporaryDirectory(dir=sys.path[0]) as tmpdir:
        print('created temporary directory', tmpdir)
        with open(download(link, tmpdir)) as f2:
            downloaded = f2.read()
            f2.close()
        assert len(downloaded) == len(response)
