#!/usr/bin/env python3
"""查询指定基金在指定区间的累计收益率时间序列"""
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL

VALID_CAL_TYPES = ["1M", "3M", "6M", "1Y", "3Y", "5Y", "YTD"]


def main():
    parser = ArgParser(description="查询基金累计收益率")
    parser.add_argument("--institution-code", required=True, help="6 位数字基金代码，如 159619")
    parser.add_argument("--cal-type", required=True, choices=VALID_CAL_TYPES,
                        help="区间类型：1M / 3M / 6M / 1Y / 3Y / 5Y / YTD")
    args = parser.parse_args()

    params = {"institution_code": args.institution_code, "cal-type": args.cal_type}
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-cal-return?" + urllib.parse.urlencode(params)

    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
