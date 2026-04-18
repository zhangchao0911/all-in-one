#!/usr/bin/env python3
"""查询港股估值分析（分页，market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询港股估值分析（分页）")
    parser.add_argument(
        "--trade_code",
        default=None,
        help="港股代码，可选；如 00700.HK 或 700；不传则全市场分页",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="页码，从 1 开始，默认 1",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=20,
        help="每页条数，默认 20",
    )
    args = parser.parse_args()

    params = {"page": args.page, "page_size": args.page_size}
    if args.trade_code is not None and str(args.trade_code).strip() != "":
        params["trade_code"] = args.trade_code.strip()

    path = "/data/api/v1/market/data/hk/hk-valuatnanalyd"
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
