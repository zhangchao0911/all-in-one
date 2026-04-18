#!/usr/bin/env python3
"""指数分页列表（market.ft.tech）：分页、排序、筛选"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="指数分页列表，支持排序、筛选、分页")
    parser.add_argument(
        "--order_by",
        default=None,
        help="排序方式，如 change_rate desc、name asc",
    )
    parser.add_argument(
        "--ob",
        default=None,
        help="与 order_by 同义",
    )
    parser.add_argument(
        "--filter",
        default=None,
        help="过滤条件表达式，如 change_rate != null、name ~ \"上证\"",
    )
    parser.add_argument(
        "--masks",
        default=None,
        help="字段掩码，逗号分隔，如 name,symkey,latest,change_rate",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=None,
        help="每页条数，不传则不分页",
    )
    parser.add_argument(
        "--page_no",
        type=int,
        default=None,
        help="页码，从 1 开始",
    )
    args = parser.parse_args()

    params = {}
    if args.order_by is not None:
        params["order_by"] = args.order_by
    elif args.ob is not None:
        params["ob"] = args.ob
    if args.filter is not None:
        params["filter"] = args.filter
    if args.masks is not None:
        params["masks"] = args.masks
    if args.page_size is not None:
        params["page_size"] = args.page_size
    if args.page_no is not None:
        params["page_no"] = args.page_no

    path = "/app/api/v2/indices"
    if params:
        path += "?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    data = fetch_json(url, headers=ft_headers())
    output(data)


if __name__ == "__main__":
    main()
