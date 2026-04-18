#!/usr/bin/env python3
"""查询全部 ETF 基础信息（market.ft.tech）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, BASE_URL


def main():
    url = BASE_URL + "/data/api/v1/market/data/etf-description-all"
    data = fetch_json(make_request(url, headers={"Content-Type": "application/json"}))
    output(data)


if __name__ == "__main__":
    main()
