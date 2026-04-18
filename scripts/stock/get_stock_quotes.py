#!/usr/bin/env python3
"""查询 A 股行情列表（分页）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, ft_headers, output

ENDPOINT = "/app/api/v2/stocks"


def main():
    parser = ArgParser(description="查询 A 股行情列表（分页）")
    parser.add_argument("--order_by", required=True, help="排序规则，如 change_rate desc")
    parser.add_argument("--page_no", type=int, required=True, help="页码，从 1 开始")
    parser.add_argument("--page_size", type=int, required=True, help="每页记录数")
    parser.add_argument("--filter", default="", help="筛选条件表达式，可选")
    parser.add_argument("--masks", default="", help="返回字段掩码，可选")
    args = parser.parse_args()

    params = {
        "order_by": args.order_by,
        "page_no": args.page_no,
        "page_size": args.page_size,
    }
    if args.filter:
        params["filter"] = args.filter
    if args.masks:
        params["masks"] = args.masks

    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    data = fetch_json(url, headers=ft_headers())
    output(data)


if __name__ == "__main__":
    main()
