#!/usr/bin/env python3
"""获取可转债全量列表（market.ft.tech）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def main():
    url = BASE_URL + "/data/api/v1/market/data/cb/cb-lists"
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
