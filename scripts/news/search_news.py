#!/usr/bin/env python3
"""语义搜索新闻（market.ft.tech）"""
import os
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL

BEIJING_TZ = timezone(timedelta(hours=8))


def _normalize_to_beijing_iso(value: str) -> str:
    """
    将输入时间规范为东八区 ISO 8601 字符串。
    - 无时区：按东八区解释
    - 有时区：统一转换到东八区
    """
    raw = value.strip()
    if not raw:
        return raw
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=BEIJING_TZ)
    else:
        dt = dt.astimezone(BEIJING_TZ)
    return dt.isoformat()


def main():
    parser = ArgParser(description="语义搜索新闻")
    parser.add_argument(
        "--query",
        required=True,
        help="搜索文字，如：人工智能",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="返回条数，默认 10",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="年份，仅支持当年，用于限定搜索范围；不传则由服务端决定",
    )
    parser.add_argument(
        "--start_time",
        default=None,
        help="开始时间（含），ISO 8601，如 2026-03-01T00:00:00+08:00",
    )
    parser.add_argument(
        "--end_time",
        default=None,
        help="结束时间（含），ISO 8601，如 2026-03-15T23:59:59+08:00",
    )
    args = parser.parse_args()

    params = {"query": args.query, "limit": args.limit}
    if args.year is not None:
        params["year"] = args.year
    try:
        if args.start_time:
            params["start_time"] = _normalize_to_beijing_iso(args.start_time)
        if args.end_time:
            params["end_time"] = _normalize_to_beijing_iso(args.end_time)
    except ValueError as e:
        print(f"时间格式错误：{e}", file=sys.stderr)
        sys.exit(1)

    url = BASE_URL + "/data/api/v1/market/data/semantic-search-news?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
