#!/usr/bin/env python3
"""获取指定日期 ETF PCF 列表（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def main():
    parser = ArgParser(description="获取指定日期 ETF PCF 列表")
    parser.add_argument(
        "--date",
        required=True,
        type=int,
        help="日期，YYYYMMDD 整型，如 20260309",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=20,
        help="每页记录数，默认 20，最大 100",
    )
    args = parser.parse_args()

    params = {"date": args.date, "page": args.page, "page_size": args.page_size}
    url = BASE_URL + "/data/api/v1/market/data/etf-pcf/etf-pcfs?" + urllib.parse.urlencode(params)

    data = fetch_json(make_request(url))
    output(data)


if __name__ == "__main__":
    main()
