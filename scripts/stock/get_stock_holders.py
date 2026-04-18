#!/usr/bin/env python3
"""查询 A 股股东信息 — 十大股东 / 十大流通股东 / 股东人数"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, output

# 不同 type 对应不同的 API endpoint
ENDPOINTS = {
    "ten": "/data/api/v1/market/data/holder/stock-holder-ten",
    "ften": "/data/api/v1/market/data/holder/stock-holder-ften",
    "nums": "/data/api/v1/market/data/holder/stock-holder-nums",
}


def main():
    parser = ArgParser(description="查询 A 股股东信息")
    parser.add_argument(
        "--type", required=True, choices=["ten", "ften", "nums"],
        help="ten=十大股东，ften=十大流通股东，nums=股东人数",
    )
    parser.add_argument(
        "--stock_code", required=True,
        help="股票代码，需携带市场后缀，如 603323.SH / 000001.SZ / 833171.BJ",
    )
    args = parser.parse_args()

    endpoint = ENDPOINTS[args.type]
    params = urllib.parse.urlencode({"stock_code": args.stock_code})
    url = f"{BASE_URL}{endpoint}?{params}"
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
