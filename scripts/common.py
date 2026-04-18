"""FTShare 公共模块 — 统一 HTTP 请求、URL 校验、参数解析。"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

# ── 配置 ──────────────────────────────────────────────
BASE_URL = "https://market.ft.tech"
CLIENT_NAME = "ft-web"
ALLOWED_NETLOCS = {"market.ft.tech", "ftai.chat"}

# ── 安全 URL 开启器 ───────────────────────────────────
SAFE_URLOPENER = urllib.request.build_opener()


def safe_urlopen(url_or_req, timeout=30):
    """发起 HTTPS GET 请求，校验目标域名是否为 market.ft.tech。"""
    url = url_or_req if isinstance(url_or_req, str) else url_or_req.full_url
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_NETLOCS:
        print(f"[security] 拒绝非法 URL: {url}", file=sys.stderr)
        sys.exit(1)
    if isinstance(url_or_req, str):
        url_or_req = urllib.request.Request(url_or_req)
    return urllib.request.urlopen(url_or_req, timeout=timeout)


def make_request(url, headers=None, method="GET"):
    """构造带默认请求头的 Request 对象。"""
    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    return req


def ft_headers():
    """返回需要鉴权的接口所需的请求头。"""
    return {
        "X-Client-Name": CLIENT_NAME,
        "Content-Type": "application/json",
    }


def fetch_json(url_or_req, headers=None):
    """发起请求并返回解析后的 JSON。出错时写 stderr 并 exit。"""
    if isinstance(url_or_req, str) and headers:
        url_or_req = make_request(url_or_req, headers)
    try:
        with safe_urlopen(url_or_req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def paginate(url, params=None, headers=None, page_size=20, max_pages=10):
    """自动翻页，收集所有 items。"""
    all_items = []
    for page in range(1, max_pages + 1):
        q = dict(params or {})
        q["page"] = page
        q["page_size"] = page_size
        qs = urllib.parse.urlencode(q, doseq=True)
        full_url = f"{url}?{qs}"
        data = fetch_json(full_url, headers=headers)
        items = data if isinstance(data, list) else data.get("items", data.get("data", []))
        if isinstance(items, list):
            all_items.extend(items)
        total = data.get("total", 0) if isinstance(data, dict) else len(items)
        if page * page_size >= total:
            break
    return all_items


def output(data):
    """统一输出：JSON 打印到 stdout。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ── 命令行工具 ────────────────────────────────────────
class ArgParser(argparse.ArgumentParser):
    """带 --json 开关的统一参数解析器。"""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.add_argument("--json", action="store_true", help="JSON 格式输出")
