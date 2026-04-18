#!/usr/bin/env python3
"""查询单只 A 股股票分时价格（一分钟级别）"""
import os
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, ft_headers, output

BEIJING_TZ = timezone(timedelta(hours=8))
ENDPOINT = "/app/api/v2/stocks/{stock}/prices"


def tm_ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def main():
    parser = ArgParser(description="查询单只 A 股股票分时价格（一分钟级别）")
    parser.add_argument(
        "--stock", required=True,
        help="股票标的键，需携带市场后缀，如 688295.XSHG / 000001.SZ / 920036.BJ",
    )
    parser.add_argument(
        "--since", default=None,
        help="时间范围起点（语义）：TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)；与 since_ts_ms 二选一",
    )
    parser.add_argument(
        "--since_ts_ms", type=int, default=None,
        help="时间范围起点（毫秒时间戳）；与 since 二选一",
    )
    args = parser.parse_args()

    if args.since is None and args.since_ts_ms is None:
        print("错误：since 与 since_ts_ms 二选一，必须提供其一", file=sys.stderr)
        sys.exit(1)
    if args.since is not None and args.since_ts_ms is not None:
        print("错误：since 与 since_ts_ms 二选一，不能同时传递", file=sys.stderr)
        sys.exit(1)

    params: dict = {}
    if args.since is not None:
        params["since"] = args.since
    else:
        params["since_ts_ms"] = args.since_ts_ms

    url = f"{BASE_URL}{ENDPOINT.format(stock=args.stock)}?{urllib.parse.urlencode(params)}"
    data = fetch_json(url, headers=ft_headers())
    for rec in data.get("prices", []):
        if "tm" in rec:
            rec["tm"] = tm_ms_to_iso(rec["tm"])
    output(data)


if __name__ == "__main__":
    main()
