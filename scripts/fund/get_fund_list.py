#!/usr/bin/env python3
"""查询所有基金概览信息（分页）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询所有基金概览信息（分页）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数，最大 1000（默认 20）")
    args = parser.parse_args()

    params = {"page": args.page, "page_size": args.page_size}
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-overview?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
