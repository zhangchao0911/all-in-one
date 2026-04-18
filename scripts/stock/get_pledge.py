#!/usr/bin/env python3
"""查询 A 股股权质押 — 市场总览 或 单只股票明细"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, output


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def normalize_summary(items: list) -> list:
    """标准化质押总览数据。"""
    result = []
    for item in items:
        result.append({
            "trade_date": item.get("trade_date", ""),
            "pledge_total_ratio": _to_float(item.get("pledge_total_ratio", 0)),
            "pledge_company_count": int(item.get("pledge_company_count", 0)),
            "pledge_deal_count": int(item.get("pledge_deal_count", 0)),
            "pledge_total_shares": _to_float(item.get("pledge_total_shares", 0)),
            "pledge_total_market_value": _to_float(item.get("pledge_total_market_value", 0)),
            "hs300_index": _to_float(item.get("hs300_index", 0)),
            "hs300_week_change_ratio": _to_float(item.get("hs300_week_change_ratio", 0)),
        })
    return result


def main():
    parser = ArgParser(description="查询 A 股股权质押数据")
    parser.add_argument(
        "--type", required=True, choices=["summary", "detail"],
        help="summary=市场质押总览，detail=单只股票质押明细",
    )
    # detail 模式参数
    parser.add_argument("--stock_code", default=None,
                        help="股票代码，含市场后缀（detail 模式必填）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（detail 默认 1）")
    parser.add_argument("--page_size", type=int, default=50, help="每页记录数（detail 默认 50）")
    args = parser.parse_args()

    if args.type == "summary":
        url = f"{BASE_URL}/data/api/v1/market/data/pledge/pledge-summary"
        raw = fetch_json(url)
        data = normalize_summary(raw)
    else:
        if not args.stock_code:
            print("错误：detail 模式需要 --stock_code", file=sys.stderr)
            sys.exit(1)
        params = urllib.parse.urlencode({
            "stock_code": args.stock_code,
            "page": args.page,
            "page_size": args.page_size,
        })
        url = f"{BASE_URL}/data/api/v1/market/data/pledge/pledge-detail?{params}"
        data = fetch_json(url)

    output(data)


if __name__ == "__main__":
    main()
