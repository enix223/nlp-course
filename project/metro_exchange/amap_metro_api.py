#!/usr/local/env python

"""
====================================
Metro stations crawler with amap API
====================================

Data source:
---------------------

* Beijing metro     http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json
* Guangzhou metro   http://map.amap.com/service/subway?_1543416340902&srhdata=4401_drw_guangzhou.json
* Shanghai metro    http://map.amap.com/service/subway?_1543416382291&srhdata=3100_drw_shanghai.json
* Shenzhen metro    http://map.amap.com/service/subway?_1543416413108&srhdata=4403_drw_shenzhen.json

Output format Example:
---------------------
{
    'city': 'BJ',
    'lines': [
        {
            'line_name': '1号线',
            'stations': [
                {'station': '苹果园', 'lon': 116.177388, 'lat': 39.926727},
                {'station': '古城', 'lon': 116.190337, 'lat': 39.907450}
            ]
        },
        {
            'line_name': '2号线',
            'stations': [
                {'station': '西直门', 'lon': 116.177388, 'lat': 39.926727},
                {'station': '积水潭', 'lon': 116.177388, 'lat': 39.926727}
            ]
        }
    ]
}

Usage Example

$ python amap_metro_api.py BJ amap.bj.metro.json
"""

import sys
import time
import json
import logging
import argparse
import requests

FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def save_file(outpath, data):
    # save the result
    with open(outpath, 'w') as fp:
        json.dump(data, fp)

    logger.info('Crawl finished. Output file: {}'.format(outpath))


city_mapping = {
    'BJ': '1100_drw_beijing.json',
    'GZ': '4401_drw_guangzhou.json',
    'SH': '3100_drw_shanghai.json',
    'SZ': '4403_drw_shenzhen.json',
}


def metro_api(outpath, city):
    rhdata = city_mapping.get(city, None)
    assert rhdata is not None, '{} is not supported'.format(city)

    url = 'http://map.amap.com/service/subway?_{}&srhdata={}'.format(
        int(time.time()),
        rhdata
    )
    res = requests.get(url)
    metros = {
        'city': 'BJ',
        'lines': []
    }
    if res.status_code == 200:
        try:
            payload = res.json()
            for line in payload['l']:
                line_name = line['ln']
                stations = [
                    {
                        'station': st['n'],
                        'lon': float(st['sl'].split(',')[0]),
                        'lat': float(st['sl'].split(',')[1])
                    } for st in line['st']
                ]
                if line['lo'] == '1':
                    # this is a loop line, eg, BJ No.2 line,
                    # so add the first station to the end
                    stations.append(stations[0])

                metros['lines'].append({
                    'line_name': line_name,
                    'stations': stations,
                })

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
    metro_api(args.outpath, args.city)
