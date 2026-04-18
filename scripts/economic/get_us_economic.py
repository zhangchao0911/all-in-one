#!/usr/bin/env python3
"""美国经济指标按 type 查询（统一接口）"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, BASE_URL

VALID_TYPES = [
    "ism-manufacturing",
    "ism-non-manufacturing",
    "nonfarm-payroll",
    "trade-balance",
    "unemployment-rate",
    "ppi-mom",
    "cpi-mom",
    "cpi-yoy",
    "core-cpi-mom",
    "core-cpi-yoy",
    "housing-starts",
    "existing-home-sales",
    "durable-goods-orders-mom",
    "cb-consumer-confidence",
    "gdp-yoy-preliminary",
    "fed-funds-rate-upper",
]


def main():
    parser = ArgParser(description="按 type 查询美国经济指标，返回时间序列（前值、现值、发布日期）")
    parser.add_argument(
        "--type",
        required=True,
        choices=VALID_TYPES,
        help="指标类型，如 ism-manufacturing, nonfarm-payroll, cpi-mom 等",
    )
    args = parser.parse_args()

    params = {"type": args.type}
    url = f"{BASE_URL}/data/api/v1/market/data/economic/us-economic?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
