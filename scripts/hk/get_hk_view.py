#!/usr/bin/env python3
"""查询港股基础视图（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询港股基础视图")
    parser.add_argument(
        "--hk_code",
        required=True,
        help="港股代码，如 00700.HK",
    )
    args = parser.parse_args()

    path = "/data/api/v1/market/data/hk/hk-view"
    url = BASE_URL + path + "?" + urllib.parse.urlencode({"hk_code": args.hk_code})

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
