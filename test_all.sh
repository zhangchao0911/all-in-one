#!/bin/bash
# FTShare All-in-One 连通性测试脚本
SKILL_DIR="/Users/chaozhang/.claude/skills/ftshare-all-in-one"
cd "$SKILL_DIR"
PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    shift
    TOTAL=$((TOTAL + 1))
    local output
    output=$(timeout 15 python3 "$@" 2>&1)
    local exit_code=$?
    if [ $exit_code -eq 124 ]; then
        echo "TIMEOUT | $name"
    elif echo "$output" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        echo "PASS    | $name"
        PASS=$((PASS + 1))
    else
        local err=$(echo "$output" | head -1)
        echo "FAIL    | $name | $err"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== FTShare All-in-One 连通性测试 ==="
echo ""

# stock
run_test "stock/get_stock_list" scripts/stock/get_stock_list.py
run_test "stock/get_stock_detail" scripts/stock/get_stock_detail.py --symbol 600519.SH
run_test "stock/get_stock_quotes" scripts/stock/get_stock_quotes.py --order_by "change_rate desc" --page_no 1 --page_size 3
run_test "stock/get_stock_ohlcs" scripts/stock/get_stock_ohlcs.py --stock 600519.SH --span DAY1 --limit 3
run_test "stock/get_stock_prices" scripts/stock/get_stock_prices.py --stock 600519.SH --since TODAY
run_test "stock/get_stock_ipos" scripts/stock/get_stock_ipos.py --page 1 --page_size 3
run_test "stock/get_block_trades" scripts/stock/get_block_trades.py
run_test "stock/get_margin_trading" scripts/stock/get_margin_trading.py --page 1 --page_size 3
run_test "stock/get_stock_balance" scripts/stock/get_stock_balance.py --mode single --stock-code 600519.SH
run_test "stock/get_stock_cashflow" scripts/stock/get_stock_cashflow.py --mode single --stock-code 600519.SH
run_test "stock/get_stock_income" scripts/stock/get_stock_income.py --mode single --stock-code 600519.SH
run_test "stock/get_stock_performance" scripts/stock/get_stock_performance.py --mode single --stock-code 600519.SH
run_test "stock/get_stock_performance_forecast" scripts/stock/get_stock_performance_forecast.py --mode single --stock-code 600519.SH
run_test "stock/get_stock_holders_ten" scripts/stock/get_stock_holders.py --type ten --stock_code 600519.SH
run_test "stock/get_stock_holders_ften" scripts/stock/get_stock_holders.py --type ften --stock_code 600519.SH
run_test "stock/get_stock_holders_nums" scripts/stock/get_stock_holders.py --type nums --stock_code 600519.SH
run_test "stock/get_pledge_summary" scripts/stock/get_pledge.py --type summary
run_test "stock/get_pledge_detail" scripts/stock/get_pledge.py --type detail --stock_code 600519.SH
run_test "stock/get_share_change" scripts/stock/get_share_change.py --stock_code 600519.SH

# etf
run_test "etf/get_etf_detail" scripts/etf/get_etf_detail.py --etf 510050.XSHG
run_test "etf/get_etf_list" scripts/etf/get_etf_list.py --page_size 3 --page_no 1
run_test "etf/get_etf_ohlcs" scripts/etf/get_etf_ohlcs.py --etf 510050.XSHG --span DAY1 --limit 3
run_test "etf/get_etf_prices" scripts/etf/get_etf_prices.py --etf 510050.XSHG --since TODAY
run_test "etf/get_etf_component" scripts/etf/get_etf_component.py --symbol 510300.XSHG
run_test "etf/get_etf_pre_single" scripts/etf/get_etf_pre_single.py --symbol 510300.XSHG
run_test "etf/get_etf_pcfs" scripts/etf/get_etf_pcfs.py --date 20260418
run_test "etf/get_etf_description" scripts/etf/get_etf_description.py

# index
run_test "index/get_index_detail" scripts/index/get_index_detail.py --index 000001.XSHG
run_test "index/get_index_list" scripts/index/get_index_list.py --page_size 3 --page_no 1
run_test "index/get_index_ohlcs" scripts/index/get_index_ohlcs.py --index 000001.XSHG --span DAY1 --limit 3
run_test "index/get_index_prices" scripts/index/get_index_prices.py --index 000001.XSHG --since TODAY
run_test "index/get_index_description" scripts/index/get_index_description.py
run_test "index/get_index_weight" scripts/index/get_index_weight.py --mode summary --page 1 --page-size 5

# fund
run_test "fund/get_fund_detail" scripts/fund/get_fund_detail.py --institution-code 000001
run_test "fund/get_fund_nav" scripts/fund/get_fund_nav.py --institution-code 000001 --page 1 --page-size 3
run_test "fund/get_fund_return" scripts/fund/get_fund_return.py --institution-code 159619 --cal-type 1Y
run_test "fund/get_fund_list" scripts/fund/get_fund_list.py --page 1 --page-size 3
run_test "fund/get_fund_symbols" scripts/fund/get_fund_symbols.py --page 1 --page-size 3

# hk
run_test "hk/get_hk_view" scripts/hk/get_hk_view.py --hk_code 00700.HK
run_test "hk/get_hk_kline" scripts/hk/get_hk_kline.py --trade-code 00700.HK --interval-unit day --until-date 2026-04-18 --since-date 2026-04-01 --limit 5
run_test "hk/get_hk_valuation" scripts/hk/get_hk_valuation.py --trade_code 00700.HK --page 1 --page_size 3
run_test "hk/get_company_hk" scripts/hk/get_company_hk.py --trade_code 00700.HK

# cb
run_test "cb/get_cb_list" scripts/cb/get_cb_list.py
run_test "cb/get_cb_base" scripts/cb/get_cb_base.py --symbol_code 110070.SH

# economic
run_test "economic/get_china_gdp" scripts/economic/get_china_gdp.py
run_test "economic/get_china_cpi" scripts/economic/get_china_cpi.py
run_test "economic/get_china_ppi" scripts/economic/get_china_ppi.py
run_test "economic/get_china_pmi" scripts/economic/get_china_pmi.py
run_test "economic/get_china_lpr" scripts/economic/get_china_lpr.py
run_test "economic/get_china_money_supply" scripts/economic/get_china_money_supply.py
run_test "economic/get_china_credit" scripts/economic/get_china_credit.py
run_test "economic/get_china_trade" scripts/economic/get_china_trade.py
run_test "economic/get_china_fiscal" scripts/economic/get_china_fiscal.py
run_test "economic/get_china_tax" scripts/economic/get_china_tax.py
run_test "economic/get_china_retail" scripts/economic/get_china_retail.py
run_test "economic/get_china_fai" scripts/economic/get_china_fai.py
run_test "economic/get_china_industrial" scripts/economic/get_china_industrial.py
run_test "economic/get_china_forex" scripts/economic/get_china_forex.py
run_test "economic/get_china_reserve" scripts/economic/get_china_reserve.py
run_test "economic/get_us_economic" scripts/economic/get_us_economic.py --type nonfarm-payroll

# news
run_test "news/search_news" scripts/news/search_news.py --query 人工智能 --limit 3

# utils
run_test "utils/get_trade_date" scripts/utils/get_trade_date.py --n 5

# announcement
run_test "announcement/get_announcements_all" scripts/announcement/get_announcements.py --mode all --start-date 20260418 --page 1 --page-size 3
run_test "announcement/get_announcements_single" scripts/announcement/get_announcements.py --mode single --stock-code 000001.SZ --page 1 --page-size 3
run_test "announcement/get_reports_all" scripts/announcement/get_reports.py --mode all --start-date 20260418 --page 1 --page-size 3
run_test "announcement/get_reports_single" scripts/announcement/get_reports.py --mode single --stock-code 000001.SZ --page 1 --page-size 3

echo ""
echo "=== 测试汇总 ==="
echo "总计: $TOTAL"
echo "通过: $PASS"
echo "失败: $FAIL"
