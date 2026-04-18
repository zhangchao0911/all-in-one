#!/usr/bin/env python3
"""指数权重统一查询（market.ft.tech）：支持 list / summary / download 三种模式"""
import argparse
import json
import os
import sys
import urllib.parse
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL


def _safe_output_path(path: str, base_dir: Optional[str] = None) -> str:
    """将 output 规范为绝对路径，并限制在 base_dir 内，防止路径遍历。"""
    base_dir = (base_dir or os.getcwd()).rstrip(os.sep)
    base_abs = os.path.abspath(base_dir)
    resolved = os.path.abspath(os.path.normpath(path))
    if os.path.commonpath([base_abs, resolved]) != base_abs:
        print(
            json.dumps(
                {"error": "output path must be under base directory", "base": base_abs},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    return resolved


def _mode_list(args):
    """分页查询指数权重列表"""
    index_code = args.index_code.strip()
    if not index_code:
        print("index_code 不能为空", file=sys.stderr)
        sys.exit(1)
    if args.page < 1:
        print("page 须 >= 1", file=sys.stderr)
        sys.exit(1)
    if args.page_size < 1 or args.page_size > 100:
        print("page_size 须在 1~100 之间", file=sys.stderr)
        sys.exit(1)

    params = {"index_code": index_code, "page": args.page, "page_size": args.page_size}
    if args.date is not None and str(args.date).strip() != "":
        params["date"] = args.date.strip()

    endpoint = "/data/api/v1/market/data/index/index_weight"
    url = BASE_URL + endpoint + "?" + urllib.parse.urlencode(params)
    data = fetch_json(url, headers=ft_headers())
    output(data)


def _mode_summary(args):
    """分页查询指数权重汇总"""
    if args.page < 1:
        print("page 须 >= 1", file=sys.stderr)
        sys.exit(1)
    if args.page_size < 1 or args.page_size > 100:
        print("page_size 须在 1~100 之间", file=sys.stderr)
        sys.exit(1)

    params = {"page": args.page, "page_size": args.page_size}
    endpoint = "/data/api/v1/market/data/index/index_weight_summary"
    url = BASE_URL + endpoint + "?" + urllib.parse.urlencode(params)
    data = fetch_json(url, headers=ft_headers())
    output(data)


def _mode_download(args):
    """根据 url_hash 下载指数权重 Excel"""
    url_hash = args.url_hash.strip()
    if not url_hash or "/" in url_hash or "\\" in url_hash:
        print(json.dumps({"error": "url_hash 非法"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    raw_output = args.output or f"{url_hash}.xlsx"
    out_path = _safe_output_path(raw_output)

    path_prefix = "/data/api/v1/market/data/index/index_weight/"
    path = path_prefix + urllib.parse.quote(url_hash, safe="")
    url = BASE_URL + path
    req = make_request(url, headers={"X-Client-Name": "ft-web"})

    try:
        with safe_urlopen(req) as resp:
            data = resp.read()

        if len(data) < 500 and data[:1] == b"{":
            try:
                err = json.loads(data.decode())
                print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
            except Exception:
                print(data.decode(errors="replace"), file=sys.stderr)
            sys.exit(1)

        with open(out_path, "wb") as f:
            f.write(data)
        output({"saved_to": os.path.abspath(out_path), "size_bytes": len(data)})
    except Exception as e:
        print(f"下载失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="指数权重统一查询（list / summary / download）")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["list", "summary", "download"],
        help="查询模式：list（权重列表）、summary（权重汇总）、download（下载 Excel）",
    )

    # list 模式参数
    parser.add_argument("--index-code", dest="index_code", default="", help="[list] 指数代码，如 000300")
    parser.add_argument("--date", default=None, help="[list] 查询日期，YYYYMMDD")

    # list / summary 共用分页参数
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始，默认 1")
    parser.add_argument("--page-size", dest="page_size", type=int, default=20, help="每页条数，默认 20，最大 100")

    # download 模式参数
    parser.add_argument("--url-hash", dest="url_hash", default=None, help="[download] 权重列表或汇总返回的 url_hash")
    parser.add_argument("--output", default=None, help="[download] 保存路径（默认 {url_hash}.xlsx）")

    args = parser.parse_args()

    if args.mode == "list":
        _mode_list(args)
    elif args.mode == "summary":
        _mode_summary(args)
    elif args.mode == "download":
        if not args.url_hash:
            print("--url-hash 在 download 模式下必填", file=sys.stderr)
            sys.exit(1)
        _mode_download(args)


if __name__ == "__main__":
    main()
