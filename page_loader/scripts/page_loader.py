#!/usr/bin/env python
from page_loader.page_loader import createParser
from page_loader.page_loader import download
import logging


def main():
    logging.basicConfig(filename='logs.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)
    logging.info('started')
    parser = createParser()
    args = parser.parse_args()
    link = args.link
    output_path = args.output
    download(link, output_path)
    logging.info('finished')


if __name__ == '__main__':
    main()
