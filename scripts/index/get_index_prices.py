#!/usr/bin/env python3
"""查询单只指数分钟级分时价格（market.ft.tech）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    parser = ArgParser(description="查询单只指数分时价格（一分钟级别）")
    parser.add_argument(
        "--index",
        required=True,
        help="指数标的键，带市场后缀，如 000001.XSHG、399001.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="时间范围起点：TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)；与 --since_ts_ms 二选一",
    )
    parser.add_argument(
        "--since_ts_ms",
        type=int,
        default=None,
        help="时间范围起点（毫秒时间戳）；不传 since 时必传",
    )
    args = parser.parse_args()

    if args.since is None and args.since_ts_ms is None:
        print("错误：必须指定 --since 或 --since_ts_ms 其一", file=sys.stderr)
        sys.exit(1)
    if args.since is not None and args.since_ts_ms is not None:
        print("错误：--since 与 --since_ts_ms 二选一", file=sys.stderr)
        sys.exit(1)

    params = {}
    if args.since is not None:
        params["since"] = args.since
    else:
        params["since_ts_ms"] = args.since_ts_ms

    path = f"/app/api/v2/indices/{args.index}/prices?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    data = fetch_json(url, headers=ft_headers())
    output(data)


if __name__ == "__main__":
    main()
