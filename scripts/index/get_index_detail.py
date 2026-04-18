#!/usr/bin/env python3
"""查询单只指数详情（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询单只指数详情")
    parser.add_argument(
        "--index",
        required=True,
        help="指数标的键，带市场后缀，如 000001.XSHG、399001.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--masks",
        default=None,
        help="可选，字段掩码，逗号分隔，如 name,symkey,latest,change_rate",
    )
    args = parser.parse_args()

    path = f"/app/api/v2/indices/{args.index}"
    if args.masks:
        path += "?" + urllib.parse.urlencode({"masks": args.masks})
    url = BASE_URL + path

    data = fetch_json(url, headers=ft_headers())
    output(data)


if __name__ == "__main__":
    main()
