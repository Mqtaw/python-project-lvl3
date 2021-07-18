#!/usr/bin/env python
from page_loader.page_loader import createParser
from page_loader.page_loader import download
import logging
import requests
import sys


def main():
    logging.basicConfig(filename='logs.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)
    logging.info('started')
    parser = createParser()
    args = parser.parse_args()
    link = args.link
    output_path = args.output
    try:
        download(link, output_path)
    except FileNotFoundError:
        logging.error('no such directory')
        sys.exit(1)
    except FileExistsError:
        logging.error('already downloaded')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        logging.error('Connection Error')
        sys.exit(1)
    logging.info('finished')


if __name__ == '__main__':
    main()
