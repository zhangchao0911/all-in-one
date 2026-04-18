#!/usr/bin/env python3
"""中国海关进出口（月度）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, BASE_URL


def main():
    url = f"{BASE_URL}/data/api/v1/market/data/economic/china-customs-trade"
    data = fetch_json(url)
    output(data)


if __name__ == "__main__":
    main()
