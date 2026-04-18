#!/usr/bin/env python3
"""查询 A 股公告列表 --mode all（按日期查全市场）或 --mode single（按股票代码查全部时期）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def _query_by_date(start_date, page, page_size):
    """按日期查全市场公告"""
    params = {
        "start_date": start_date,
        "end_date": start_date,
        "type": "stock",
        "page": page,
        "page_size": page_size,
    }
    url = f"{BASE_URL}/data/api/v1/market/data/announcements/stock-announcements?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def _query_by_stock(stock_code, page, page_size):
    """按股票代码查全部时期公告"""
    params = {
        "stock_code": stock_code,
        "type": "stock",
        "page": page,
        "page_size": page_size,
    }
    url = f"{BASE_URL}/data/api/v1/market/data/announcements/stock-announcements?" + urllib.parse.urlencode(params)
    return fetch_json(url)


def main():
    parser = ArgParser(description="查询 A 股公告列表（支持按日期或按股票代码查询）")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["all", "single"],
        help='模式：all=按日期查全市场，single=按股票代码查全部时期',
    )
    parser.add_argument("--start-date", default=None, help="查询日期，格式 YYYYMMDD（mode=all 时必填）")
    parser.add_argument("--stock-code", default=None, help="股票代码，含市场后缀，如 603323.SH（mode=single 时必填）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数（默认 20）")
    args = parser.parse_args()

    if args.mode == "all":
        if not args.start_date:
            print("错误：mode=all 时必须指定 --start-date", file=sys.stderr)
            sys.exit(1)
        data = _query_by_date(args.start_date, args.page, args.page_size)
    else:
        if not args.stock_code:
            print("错误：mode=single 时必须指定 --stock-code", file=sys.stderr)
            sys.exit(1)
        data = _query_by_stock(args.stock_code, args.page, args.page_size)

    output(data)


if __name__ == "__main__":
    main()
