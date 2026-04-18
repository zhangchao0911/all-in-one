#!/usr/bin/env python3
"""查询港股 K 线（market.ft.tech）"""
import argparse
import os
import re
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL

INTERVAL_UNITS = ("day", "month", "quarter", "year")
ADJUST_KINDS = ("forward", "none")

BEIJING_TZ = timezone(timedelta(hours=8))
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_date(value: str, name: str) -> str:
    """校验 YYYY-MM-DD 格式；若传入时带时间/时区则截取日期部分（东八区）。"""
    v = value.strip()
    if DATE_RE.match(v):
        return v
    try:
        raw = v
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BEIJING_TZ)
        else:
            dt = dt.astimezone(BEIJING_TZ)
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        print(f"{name} 格式错误，需为 YYYY-MM-DD：{value}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询港股 K 线")
    parser.add_argument(
        "--trade-code",
        dest="trade_code",
        required=True,
        help="港股代码，如 00700.HK 或 700；响应统一为 5 位 + .HK",
    )
    parser.add_argument(
        "--interval-unit",
        dest="interval_unit",
        required=True,
        choices=INTERVAL_UNITS,
        help="K 线间隔：day / month / quarter / year",
    )
    parser.add_argument(
        "--until-date",
        dest="until_date",
        required=True,
        help="结束日期，YYYY-MM-DD（东八区交易日）",
    )
    parser.add_argument(
        "--since-date",
        dest="since_date",
        default=None,
        help="开始日期，YYYY-MM-DD；不传则从库中最早数据起",
    )
    parser.add_argument(
        "--adjust-kind",
        dest="adjust_kind",
        default="forward",
        choices=ADJUST_KINDS,
        help="复权类型：forward（前复权，默认）或 none（不复权）",
    )
    parser.add_argument(
        "--interval-value",
        dest="interval_value",
        type=int,
        default=1,
        help="间隔数值，当前仅支持 1（默认 1）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="返回条数上限；日 K 在 SQL 层下推，月/季/年聚合后截取最近 N 根",
    )
    args = parser.parse_args()

    until_date = _validate_date(args.until_date, "--until-date")
    since_date = None
    if args.since_date is not None and args.since_date.strip():
        since_date = _validate_date(args.since_date, "--since-date")

    params = {
        "trade_code": args.trade_code.strip(),
        "interval_unit": args.interval_unit,
        "until_date": until_date,
        "adjust_kind": args.adjust_kind,
        "interval_value": args.interval_value,
    }
    if since_date is not None:
        params["since_date"] = since_date
    if args.limit is not None:
        params["limit"] = args.limit

    path = "/data/api/v1/market/data/hk/hk-candlesticks"
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
