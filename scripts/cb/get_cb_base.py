#!/usr/bin/env python3
"""查询单只可转债基础信息（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询可转债基础信息")
    parser.add_argument(
        "--symbol_code",
        required=True,
        help="转债代码，可带交易所后缀，如 110070.SH 或 110070",
    )
    args = parser.parse_args()

    path = "/data/api/v1/market/data/cb/cb-base-data"
    url = BASE_URL + path + "?" + urllib.parse.urlencode({"symbol_code": args.symbol_code})

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
