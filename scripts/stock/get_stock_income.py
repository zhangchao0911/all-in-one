#!/usr/bin/env python3
"""查询 A 股利润表 — 全市场指定报告期 或 单只股票全部报告期"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, output

VALID_REPORT_TYPES = ["q1", "q2", "q3", "annual"]


def main():
    parser = ArgParser(description="查询 A 股利润表")
    parser.add_argument(
        "--mode", required=True, choices=["all", "single"],
        help="all=全市场指定报告期，single=单只股票全部报告期",
    )
    parser.add_argument("--year", type=int, default=None, help="报告所属年度（all 模式必填）")
    parser.add_argument("--report-type", default=None, choices=VALID_REPORT_TYPES,
                        help="报告期类型（all 模式必填）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数（默认 20）")
    parser.add_argument("--stock-code", default=None, help="股票代码，含市场后缀（single 模式必填）")
    args = parser.parse_args()

    if args.mode == "all":
        if not args.year or not args.report_type:
            print("错误：all 模式需要 --year 和 --report-type", file=sys.stderr)
            sys.exit(1)
        params = {
            "year": args.year,
            "report_type": args.report_type,
            "page": args.page,
            "page_size": args.page_size,
        }
    else:
        if not args.stock_code:
            print("错误：single 模式需要 --stock-code", file=sys.stderr)
            sys.exit(1)
        params = {"stock_code": args.stock_code}

    url = f"{BASE_URL}/data/api/v1/market/data/finance/income?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
