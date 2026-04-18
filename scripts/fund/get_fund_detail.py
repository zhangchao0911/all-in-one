#!/usr/bin/env python3
"""查询指定基金的基础信息"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询指定基金基础信息")
    parser.add_argument("--institution-code", required=True, help="6 位数字基金代码，如 000001")
    args = parser.parse_args()

    params = {"institution_code": args.institution_code}
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-basicinfo?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
