#!/usr/bin/env python3
"""查询单只股票/基金/指数信息（ftai.chat）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ArgParser, fetch_json, make_request, output

# 本接口域名固定为 ftai.chat，不使用 common 的 BASE_URL
FTAI_BASE = "https://ftai.chat"


def main():
    parser = ArgParser(description="查询单只股票/基金/指数信息")
    parser.add_argument("--symbol", required=True, help="标的代码，带市场后缀，如 600519.SH")
    args = parser.parse_args()

    url = f"{FTAI_BASE}/api/v1/market/security/{args.symbol}/info"
    req = make_request(url)
    data = fetch_json(req)
    output(data)


if __name__ == "__main__":
    main()
