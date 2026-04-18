#!/usr/bin/env python3
"""查询单只 A 股股票所有报告期的股东增减持信息"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, output

ENDPOINT = "/data/api/v1/market/data/holder/stock-share-chg"


def main():
    parser = ArgParser(description="查询 A 股股东增减持信息")
    parser.add_argument(
        "--stock_code", required=True,
        help="股票代码，需携带市场后缀，如 603323.SH / 000001.SZ / 833171.BJ",
    )
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page_size", type=int, default=50, help="每页记录数，默认 50")
    args = parser.parse_args()

    params = urllib.parse.urlencode({
        "stock_code": args.stock_code,
        "page": args.page,
        "page_size": args.page_size,
    })
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
