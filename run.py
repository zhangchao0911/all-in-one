"""FTShare All-in-One 统一调度入口。

支持两种调用方式：
  1. 分类路径:  python run.py stock/get_stock_list
  2. 旧名兼容:  python run.py stock-list-all-stocks

run.py 与 SKILL.md 位于同一目录，通过 __file__ 定位 scripts/。
"""

import os
import runpy
import sys

SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")

# ── 旧名 → 分类路径 映射表 ────────────────────────────
_NAME_MAP = {
    # stock
    "stock-list-all-stocks": "stock/get_stock_list",
    "stock-security-info": "stock/get_stock_detail",
    "stock-quotes-list": "stock/get_stock_quotes",
    "stock-ohlcs": "stock/get_stock_ohlcs",
    "stock-prices": "stock/get_stock_prices",
    "stock-ipos": "stock/get_stock_ipos",
    "block-trades": "stock/get_block_trades",
    "margin-trading-details": "stock/get_margin_trading",
    "stock-balance-all-stocks-specific-period": "stock/get_stock_balance",
    "stock-balance-single-stock-all-periods": "stock/get_stock_balance",
    "stock-cashflow-all-stocks-specific-period": "stock/get_stock_cashflow",
    "stock-cashflow-single-stock-all-periods": "stock/get_stock_cashflow",
    "stock-income-all-stocks-specific-period": "stock/get_stock_income",
    "stock-income-single-stock-all-periods": "stock/get_stock_income",
    "stock-performance-express-all-stocks-specific-period": "stock/get_stock_performance",
    "stock-performance-express-single-stock-all-periods": "stock/get_stock_performance",
    "stock-performance-forecast-all-stocks-specific-period": "stock/get_stock_performance_forecast",
    "stock-performance-forecast-single-stock-all-periods": "stock/get_stock_performance_forecast",
    "stock-holder-ten": "stock/get_stock_holders",
    "stock-holder-ften": "stock/get_stock_holders",
    "stock-holder-nums": "stock/get_stock_holders",
    "pledge-summary": "stock/get_pledge",
    "pledge-detail": "stock/get_pledge",
    "stock-share-chg": "stock/get_share_change",
    # etf
    "etf-detail": "etf/get_etf_detail",
    "etf-list-paginated": "etf/get_etf_list",
    "etf-ohlcs": "etf/get_etf_ohlcs",
    "etf-prices": "etf/get_etf_prices",
    "etf-component": "etf/get_etf_component",
    "etf-pre-single": "etf/get_etf_pre_single",
    "etf-pcfs": "etf/get_etf_pcfs",
    "etf-pcf-download": "etf/download_etf_pcf",
    "etf-description-all": "etf/get_etf_description",
    # index
    "index-detail": "index/get_index_detail",
    "index-list-paginated": "index/get_index_list",
    "index-ohlcs": "index/get_index_ohlcs",
    "index-prices": "index/get_index_prices",
    "index-description-all": "index/get_index_description",
    "index-description-paginated": "index/get_index_list",
    "index-description-download": "index/download_index_desc",
    "index-weight-list": "index/get_index_weight",
    "index-weight-summary": "index/get_index_weight",
    "index-weight-download": "index/get_index_weight",
    # fund
    "fund-basicinfo-single-fund": "fund/get_fund_detail",
    "fund-nav-single-fund-paginated": "fund/get_fund_nav",
    "fund-cal-return-single-fund-specific-period": "fund/get_fund_return",
    "fund-overview-all-funds-paginated": "fund/get_fund_list",
    "fund-support-symbols-all-funds-paginated": "fund/get_fund_symbols",
    # hk
    "hk-view": "hk/get_hk_view",
    "hk-candlesticks": "hk/get_hk_kline",
    "hk-valuatnanalyd": "hk/get_hk_valuation",
    "company-hk": "hk/get_company_hk",
    # cb
    "cb-base-data": "cb/get_cb_base",
    "cb-lists": "cb/get_cb_list",
    # economic
    "economic-china-gdp-quarterly": "economic/get_china_gdp",
    "economic-china-cpi-monthly": "economic/get_china_cpi",
    "economic-china-ppi-monthly": "economic/get_china_ppi",
    "economic-china-pmi-monthly": "economic/get_china_pmi",
    "economic-china-lpr-monthly": "economic/get_china_lpr",
    "economic-china-money-supply-monthly": "economic/get_china_money_supply",
    "economic-china-credit-loans-monthly": "economic/get_china_credit",
    "economic-china-customs-trade-monthly": "economic/get_china_trade",
    "economic-china-fiscal-revenue-monthly": "economic/get_china_fiscal",
    "economic-china-tax-revenue-monthly": "economic/get_china_tax",
    "economic-china-retail-sales-monthly": "economic/get_china_retail",
    "economic-china-fixed-asset-investment-monthly": "economic/get_china_fai",
    "economic-china-industrial-added-value-monthly": "economic/get_china_industrial",
    "economic-china-forex-gold-monthly": "economic/get_china_forex",
    "economic-china-reserve-ratio-monthly": "economic/get_china_reserve",
    "economic-us-economic-by-type": "economic/get_us_economic",
    # announcement
    "stock-announcements-all-stocks-specific-date": "announcement/get_announcements",
    "stock-announcements-single-stock-all-periods": "announcement/get_announcements",
    "stock-announcements-specific-url-hash": "announcement/download_announcement",
    "stock-reports-all-stocks-specific-date": "announcement/get_reports",
    "stock-reports-single-stock-all-periods": "announcement/get_reports",
    "stock-reports-specific-url-hash": "announcement/download_report",
    # news
    "semantic-search-news": "news/search_news",
    # utils
    "get-nth-trade-date": "utils/get_trade_date",
}


def _allowed_scripts():
    """扫描 scripts/ 下所有 .py 文件，返回白名单集合。"""
    allowed = set()
    for root, _dirs, files in os.walk(SCRIPTS_DIR):
        for f in files:
            if f.endswith(".py") and f != "__init__.py" and f != "common.py":
                rel = os.path.relpath(os.path.join(root, f), SCRIPTS_DIR)
                name = rel.replace(os.sep, "/")[:-3]  # scripts/stock/get_list.py → stock/get_list
                allowed.add(name)
    return allowed


def _resolve(sub_skill):
    """将用户传入的子命令解析为 scripts/ 下的相对路径。"""
    # 1. 先查旧名映射
    mapped = _NAME_MAP.get(sub_skill)
    if mapped:
        return mapped
    # 2. 直接当分类路径用
    return sub_skill


def _execute_handler(script_rel, extra_args):
    """在当前进程中执行 handler 脚本。"""
    script_path = os.path.join(SCRIPTS_DIR, f"{script_rel}.py")
    if not os.path.isfile(script_path):
        print(f"未找到脚本: {script_rel} ({script_path})", file=sys.stderr)
        sys.exit(1)

    saved_cwd = os.getcwd()
    saved_argv = sys.argv[:]
    try:
        sys.argv = [script_path] + extra_args
        os.chdir(os.path.dirname(script_path))
        runpy.run_path(script_path, run_name="__main__")
    except SystemExit as e:
        if e.code not in (None, 0):
            raise
    finally:
        os.chdir(saved_cwd)
        sys.argv = saved_argv


def main():
    if len(sys.argv) < 2:
        print("用法: python run.py <子命令> [参数...]", file=sys.stderr)
        print("示例: python run.py etf/get_etf_detail --etf 510050.XSHG", file=sys.stderr)
        print("      python run.py etf-detail --etf 510050.XSHG  (旧名兼容)", file=sys.stderr)
        sys.exit(1)

    sub_skill = sys.argv[1]
    extra_args = sys.argv[2:]

    allowed = _allowed_scripts()
    resolved = _resolve(sub_skill)

    if resolved not in allowed:
        print(f"未知子命令: {sub_skill}", file=sys.stderr)
        print(f"可用命令: {', '.join(sorted(allowed)[:20])}...", file=sys.stderr)
        sys.exit(1)

    _execute_handler(resolved, extra_args)


if __name__ == "__main__":
    main()
