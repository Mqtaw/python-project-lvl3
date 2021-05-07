#!/usr/bin/env python
from page_loader.page_loader import createParser
from page_loader.page_loader import download


def main():
    parser = createParser()
    args = parser.parse_args()
    link = args.link
    output_path = args.output
    download(link, output_path)


if __name__ == '__main__':
    main()
