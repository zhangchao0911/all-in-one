#!/usr/bin/env python3
"""查询全部指数基础信息（market.ft.tech）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL

ENDPOINT = "/data/api/v1/market/data/index-description-all"


def main():
    url = BASE_URL + ENDPOINT
    data = fetch_json(url, headers=ft_headers())
    output(data)


if __name__ == "__main__":
    main()
