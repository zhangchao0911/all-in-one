#!/usr/bin/env python3
"""获取所有 A 股股票代码列表"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import BASE_URL, fetch_json, output


def main():
    url = f"{BASE_URL}/data/api/v1/market/data/stock-list"
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
