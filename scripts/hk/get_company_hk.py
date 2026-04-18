#!/usr/bin/env python3
"""查询港股公司介绍（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询港股公司介绍")
    parser.add_argument(
        "--trade_code",
        required=True,
        help="港股交易代码，须带市场后缀，如 00700.HK",
    )
    args = parser.parse_args()

    path = "/data/api/v1/market/data/hk/company-hk"
    url = BASE_URL + path + "?" + urllib.parse.urlencode({"trade_code": args.trade_code})

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
