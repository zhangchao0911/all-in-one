#!/usr/bin/env python3
"""查询单只 A 股股票 OHLC K 线数据（含 MA5/MA10/MA20）"""
import os
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, BASE_URL, fetch_json, ft_headers, output

BEIJING_TZ = timezone(timedelta(hours=8))
ENDPOINT = "/app/api/v2/stocks/{stock}/ohlcs"


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def with_iso_timestamps(data: dict) -> dict:
    """将 ohlcs 的 otm/ctm、ma5/ma10/ma20 的 ctm 转为北京时间 ISO 字符串。"""
    for o in data.get("ohlcs", []):
        if "otm" in o:
            o["otm"] = ms_to_iso(o["otm"])
        if "ctm" in o:
            o["ctm"] = ms_to_iso(o["ctm"])
    for key in ("ma5", "ma10", "ma20"):
        for m in data.get(key, []):
            if "ctm" in m:
                m["ctm"] = ms_to_iso(m["ctm"])
    return data


def main():
    parser = ArgParser(description="查询单只 A 股股票 OHLC K 线数据")
    parser.add_argument(
        "--stock", required=True,
        help="股票标的键，需携带市场后缀，如 688295.XSHG / 000001.SZ / 920036.BJ",
    )
    parser.add_argument(
        "--span", required=True,
        choices=["DAY1", "WEEK1", "MONTH1", "YEAR1"],
        help="K 线周期：DAY1（日线）、WEEK1（周线）、MONTH1（月线）、YEAR1（年线）",
    )
    parser.add_argument("--limit", type=int, default=None, help="返回 K 线根数上限，建议不超过 2000")
    parser.add_argument("--until_ts_ms", type=int, default=None, help="截止时间戳（毫秒）")
    args = parser.parse_args()

    params: dict = {"span": args.span}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.until_ts_ms is not None:
        params["until_ts_ms"] = args.until_ts_ms

    url = f"{BASE_URL}{ENDPOINT.format(stock=args.stock)}?{urllib.parse.urlencode(params)}"
    data = fetch_json(url, headers=ft_headers())
    with_iso_timestamps(data)
    output(data)


if __name__ == "__main__":
    main()
