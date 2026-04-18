#!/usr/bin/env python3
"""获取 A 股 IPO 列表，支持分页与全量拉取"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, output, paginate

ENDPOINT = "/data/api/v1/market/data/stock-ipos"


def fetch_page(page: int, page_size: int) -> dict:
    params = urllib.parse.urlencode({"page": page, "page_size": page_size})
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    return fetch_json(url)


def main():
    parser = ArgParser(description="获取 A 股 IPO 列表")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始）")
    parser.add_argument("--page_size", type=int, default=20, help="每页记录数")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.fetch_all:
        items = paginate(f"{BASE_URL}{ENDPOINT}", page_size=args.page_size, max_pages=100)
        output({"items": items, "total_items": len(items)})
    else:
        result = fetch_page(args.page, args.page_size)
        output(result)


if __name__ == "__main__":
    main()
