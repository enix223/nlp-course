"""
==============================================
Chinese classic novels crawler (中国古典小说爬虫)

Data from http://www.shicimingju.com
==============================================

Usage
------

positional arguments:
  outpath      Download files path

optional arguments:
  -h, --help   show this help message and exit
  --skip SKIP  How many books you need to skip? default 0
  --stop STOP  How many books you need to download? default 0
  --wait WAIT  No of seconds to wait between two books

Example
------

# Download all books in the catalog, and keep the data in current dir
$ python crawler_china_classic_novels.py .

# Skip 1 book, and download 1 book, and keep the data in current dir
$ python crawler_china_classic_novels.py . --stop 1 --skip 1

# Skip 1 book, and download 5 book, and insert a 5 sec sleep step between each book,
# and keep the data in current dir
$ python crawler_china_classic_novels.py . --stop 5 --skip 1 --wait 5

==============================================
"""

from bs4 import BeautifulSoup
import requests
import logging
import argparse
import time
import sys
import os

logger = logging.getLogger(__name__)
FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


from_url = 'http://www.shicimingju.com/book/'
domain = 'http://www.shicimingju.com'


def download_chapter(name, link, out):
    logger.info('Requesting chapter {}: {}...'.format(name, link))
    resp = requests.get(link)
    if resp.status_code != 200:
        logger.error('Failed to download chapter: {}, code: {}, err: {}'.format(name, resp.status_code, resp.text))
        return

    html = BeautifulSoup(resp.text, 'html.parser')
    paragraphs = html.select('.chapter_content p')

    if len(paragraphs) == 0:
        paragraphs = html.select('.chapter_content')

    out.write(name)
    out.write('\n\n')

    for paragraph in paragraphs:
        out.write(paragraph.text)
        out.write('\n\n')


def download_book(book_name, link, outdir):
    logger.info('Requesting book {}: {}...'.format(book_name, link))
    resp = requests.get(link)
    if resp.status_code != 200:
        logger.error('Failed to download book: {}, code: {}, err: {}'.format(book_name, resp.status_code, resp.text))
        return

    html = BeautifulSoup(resp.text, 'html.parser')
    chapters = html.select('.book-mulu li a')

    for chapter in chapters:
        filename = os.path.join(outdir, '{}-{}.txt'.format(book_name, chapter.text.replace(' ', '')))
        with open(filename, 'w') as out:
            name, link = chapter.text, '{}{}'.format(domain, chapter['href'])
            download_chapter(name, link, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'outpath',
        type=str,
        help='Download files path'
    )
    parser.add_argument(
        '--skip',
        type=int,
        default=0,
        help='How many books you need to skip? default 0'
    )
    parser.add_argument(
        '--stop',
        type=int,
        default=0,
        help='How many books you need to download? default 0'
    )
    parser.add_argument(
        '--wait',
        type=int,
        default=0,
        help='No of seconds to wait between two books'
    )
    args = parser.parse_args(sys.argv[1:])

    resp = requests.get(from_url)
    if resp.status_code == 200:
        logger.info('Requesting classic novels...')
        html = BeautifulSoup(resp.text, 'html.parser')
        book_hrefs = html.select('.bookmark-list li a')
        success = 0
        for i, href in enumerate(book_hrefs):
            book_name = href.text

            if i >= args.skip:
                book_link = '{}{}'.format(domain, href['href'])
                download_book(book_name, book_link, args.outpath)

                success += 1
                if args.stop > 0 and success >= args.stop:
                    break

                if args.wait > 0:
                    time.sleep(args.wait)
            else:
                logger.info('Skip book {}'.format(book_name))

        logger.info('Download finished. Total book downloaded: {}. Books in {}'.format(success, args.outpath))
