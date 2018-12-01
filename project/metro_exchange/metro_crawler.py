#!/usr/local/env python

"""
======================
Metro stations crawler
======================

Data source:
---------------------

* Beijing metro:    https://map.bjsubway.com/
* Shanghai metro:   http://m.shmetro.com/core/shmetro/mdstationinfoback_new.ashx?act=getAllStations
* Guangzhou metro   http://cs.gzmtr.com/base/doLoadLines.do?callback=gzmetro
* Shenzhen metro    http://www.szmc.net/ver2/operating/search?scode=0101&xl=1

Output format Example:
---------------------
{
    'city': 'BJ',
    'lines': [
        {
            'line_name': '1号线',
            'stations': [
                {'station': '苹果园', 'x': },
                {'station': '古城'}
            ]
        },
        {
            'line_name': '2号线',
            'stations': [
                {'station': '西直门'},
                {'station': '积水潭'}
            ]
        }
    ]
}

Usage Example

$ python metro_crawler.py BJ bj.metro.json
"""

import re
import sys
import json
import logging
import argparse
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree

FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def save_file(outpath, data):
    # save the result
    with open(outpath, 'w') as fp:
        json.dump(data, fp)

    logger.info('Crawl finished. Output file: {}'.format(outpath))


def crawl_sz(outpath):
    url = 'http://www.szmc.net/public/scripts/sites.js'
    res = requests.get(url)
    lines = re.search(r'(?<=var xls=)\S+(?=;)', res.text).group()
    lines = re.findall(r'\'(\w+)\'', lines)

    metros = {
        'city': 'SZ',
        'lines': []
    }
    for idx, name in enumerate(lines):
        pattern = r'(?<=var site%d=)\S+(?=;)' % (idx + 1)
        data = re.search(pattern, res.text).group()
        stations = re.findall(r'(?<=n:\')\w+', data)
        stations = list(map(lambda x: {'station_name': x}, stations))
        line = {'line_name': name, 'stations': stations}
        metros['lines'].append(line)

    save_file(outpath, metros)


def crawl_gz(outpath):
    prefix = 'gzmetro'
    url = 'http://cs.gzmtr.com/base/doLoadLines.do?callback={}'.format(prefix)
    res = requests.get(url)
    metros = {
        'city': 'GZ',
        'lines': []
    }
    if res.status_code == 200:
        try:
            data = res.text.lstrip(prefix)  # exclude callback
            data = data[1:len(data) - 1]    # exclude parenthesis
            lines = json.loads(data)
            for node in lines['lines']:
                line = {'line_name': node['lineName']}
                line['stations'] = list(map(lambda x: {'station_name': x['stageName']}, node['stages']))
                metros['lines'].append(line)

            # save the result
            save_file(outpath, metros)
        except Exception:
            logger.exception('Failed to parse the metro station output')
    else:
        logger.error('Failed to get guangzhou metro stations, code: {}'.format(
            res.status_code
        ))


def crawl_sh(outpath):
    # step 1 - get all lines
    def parse_line(line):
        link = line.select_one('a')
        line_name = link.text.strip()
        line_no = int(re.search(r'(?<=/axlcz)\d+', link.attrs['href']).group())
        return (line_no, line_name)

    url = 'http://service.shmetro.com/axlcz01/index.htm'
    res = requests.get(url)
    line_names = []
    if res.status_code == 200:
        bs = BeautifulSoup(res.text, features='html.parser')
        lines_nodes = bs.select('ul.site_select_list > li')
        line_names = dict(map(lambda x: parse_line(x), lines_nodes))
    else:
        logger.error('Failed to get shanghai metro lines')

    # step 2 - get all stations
    url = 'http://m.shmetro.com/core/shmetro/mdstationinfoback_new.ashx?act=getAllStations'
    res = requests.get(url)
    metros = {
        'city': 'SH',
        'lines': []
    }
    if res.status_code == 200:
        try:
            stations = json.loads(res.text)
            prev = ''
            for station in stations:
                line = int(station['key'][:2])
                line_name = line_names[line]
                if prev != line_name:
                    metros['lines'].append({
                        'line_name': line_name,
                        'stations': []
                    })

                metros['lines'][-1]['stations'].append({
                    'station_name': station['value']
                })
                prev = line_name

            # save the result
            save_file(outpath, metros)
        except Exception:
            logger.exception('Failed to parse the metro station output')
    else:
        logger.error('Failed to get shanghai metro stations, code: {}'.format(
            res.status_code
        ))


def crawl_bj(outpath):
    url = 'https://map.bjsubway.com/subwaymap/beijing.xml'
    res = requests.get(url)
    metros = {
        'city': 'BJ',
        'lines': []
    }
    if res.status_code == 200:
        try:
            res.encoding = 'utf-8'
            root = ElementTree.fromstring(res.text)  # root = <sw>
            for line_child in root:
                # <l> tag
                line = {'line_name': line_child.attrib.get('lb')}
                stations = line_child.findall('./p')
                stations = filter(lambda x: x.attrib.get('lb', '') != '', stations)
                line['stations'] = list(map(lambda x: {'station_name': x.attrib.get('lb')}, stations))
                if line_child.attrib.get('loop') == 'true':
                    line['stations'].append(line['stations'][0])
                metros['lines'].append(line)

            # save the result
            save_file(outpath, metros)
        except Exception:
            logger.exception('Failed to parse the metro station xml output')
    else:
        logger.error('Failed to get Beijing metro stations, code: {}'.format(
            res.status_code
        ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'city',
        type=str,
        help='The city you need to grap, current support BJ, SH, GZ, SZ'
    )
    parser.add_argument(
        'outpath',
        type=str,
        help='The output path for metro stations map'
    )
    args = parser.parse_args(sys.argv[1:])

    _CRWAL_MAPPING = {
        'BJ': crawl_bj,
        'SH': crawl_sh,
        'GZ': crawl_gz,
        'SZ': crawl_sz,
    }

    crawler = _CRWAL_MAPPING.get(args.city, None)
    if crawler is not None:
        crawler(args.outpath)
    else:
        logger.info('{} city is not supported'.format(args.city))
