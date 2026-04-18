#!/usr/bin/env python3
"""查询单只 ETF 成份（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def main():
    parser = ArgParser(description="查询单只 ETF 成份")
    parser.add_argument(
        "--symbol",
        required=True,
        help="ETF 标的代码，带交易所后缀，如 510300.XSHG、159915.XSHE、510300.SH",
    )
    args = parser.parse_args()

    path = "/data/api/v1/market/data/etf-component?" + urllib.parse.urlencode({"symbol": args.symbol})
    url = BASE_URL + path

    data = fetch_json(make_request(url, headers={"Content-Type": "application/json"}))
    output(data)


if __name__ == "__main__":
    main()
