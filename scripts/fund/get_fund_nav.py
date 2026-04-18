#!/usr/bin/env python3
"""查询指定基金的净值历史（分页）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询指定基金净值历史（分页）")
    parser.add_argument("--institution-code", required=True, help="6 位数字基金代码，如 000001")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=50, help="每页记录数（默认 50）")
    args = parser.parse_args()

    params = {
        "institution_code": args.institution_code,
        "page": args.page,
        "page_size": args.page_size,
    }
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-nav?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
