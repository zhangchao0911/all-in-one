#!/usr/bin/env python3
"""根据 url_hash 下载指数描述 PDF（market.ft.tech）"""
import argparse
import json
import os
import sys
import urllib.parse
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import safe_urlopen, fetch_json, output, ArgParser, make_request, ft_headers, BASE_URL

PATH_PREFIX = "/data/api/v1/market/data/index/index_description/"


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


def main():
    parser = argparse.ArgumentParser(description="下载指数描述 PDF（路径参数 url_hash）")
    parser.add_argument(
        "--url-hash",
        required=True,
        help="列表接口 index-description-paginated 返回的 url_hash",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="保存路径（默认当前目录下 {url_hash}.pdf）",
    )
    args = parser.parse_args()

    url_hash = args.url_hash.strip()
    if not url_hash or "/" in url_hash or "\\" in url_hash:
        print(json.dumps({"error": "url_hash 非法"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    raw_output = args.output or f"{url_hash}.pdf"
    out_path = _safe_output_path(raw_output)

    path = PATH_PREFIX + urllib.parse.quote(url_hash, safe="")
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


if __name__ == "__main__":
    main()
