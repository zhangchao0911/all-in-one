#!/usr/bin/env python3
"""查询单只 ETF 盘前数据（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def main():
    parser = ArgParser(description="查询单只 ETF 盘前数据")
    parser.add_argument(
        "--symbol",
        required=True,
        help="ETF 标的代码，带交易所后缀，如 510300.XSHG、159915.XSHE",
    )
    parser.add_argument(
        "--date",
        type=int,
        default=None,
        help="交易日 YYYYMMDD，如 20260316；不传则使用当日（CST）",
    )
    args = parser.parse_args()

    params: dict = {"symbol": args.symbol}
    if args.date is not None:
        params["date"] = args.date

    path = "/data/api/v1/market/data/etf-pre-single?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    data = fetch_json(make_request(url, headers={"Content-Type": "application/json"}))
    output(data)


if __name__ == "__main__":
    main()
