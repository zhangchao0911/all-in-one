#!/usr/bin/env python3
"""获取当前日期的前 N 个交易日（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def main():
    parser = ArgParser(description="获取当前日期的前 N 个交易日")
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="前 N 个交易日，必须 >= 1",
    )
    args = parser.parse_args()
    if args.n < 1:
        print("错误：n 必须大于等于 1", file=sys.stderr)
        sys.exit(1)

    url = BASE_URL + "/data/api/v1/market/data/time/get-nth-trade-date?" + urllib.parse.urlencode({"n": args.n})
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
