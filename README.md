# FTShare All-in-One

全市场金融数据统一技能集 —— 适用于 Claude Code / ClawHub 等 AI 编程助手。

## 数据来源

**非凸科技** ([market.ft.tech](https://market.ft.tech))

## 功能概览

| 类别 | 覆盖范围 |
|------|----------|
| A 股 | 股票列表、行情、K 线、分时、IPO、大宗交易、融资融券、财报（资产负债/现金流/利润）、业绩快报/预告、十大股东、股权质押、股东增减持 |
| ETF | 详情、列表、K 线、分时、成份股、盘前数据、PCF 清单与下载、ETF 描述 |
| 指数 | 详情、列表、K 线、分时、权重、描述与下载 |
| 基金 | 详情、净值、收益率（1M/3M/6M/1Y/3Y/5Y/YTD）、列表、标的代码 |
| 港股 | 行情、K 线、估值、公司信息 |
| 可转债 | 列表、详情（转股价/转股价值等） |
| 宏观经济 | 中国 15 项（GDP/CPI/PPI/PMI/LPR/M2/社融/进出口/财政/税收/社零/固投/工业增加值/外汇储备/存准率）+ 美国 16 类 |
| 公告研报 | 全市场/个股公告与研报查询、PDF 下载 |
| 新闻 | 语义搜索 |

## 目录结构

```
ftshare-all-in-one/
├── SKILL.md                      # Skill 定义文件（AI 助手行为指南）
├── run.py                        # 统一调度入口（支持分类路径 + 旧名兼容）
├── test_all.sh                   # 连通性测试脚本
├── scripts/
│   ├── common.py                 # 公共模块（HTTP 请求 / URL 校验 / 输出）
│   ├── stock/                    # A 股（16 个脚本）
│   ├── etf/                      # ETF（8 个脚本）
│   ├── index/                    # 指数（7 个脚本）
│   ├── fund/                     # 基金（5 个脚本）
│   ├── hk/                       # 港股（4 个脚本）
│   ├── cb/                       # 可转债（2 个脚本）
│   ├── economic/                 # 宏观经济（16 个脚本）
│   ├── announcement/             # 公告研报（4 个脚本）
│   ├── news/                     # 新闻（1 个脚本）
│   └── utils/                    # 工具（交易日查询）
```

## 安装

将整个目录复制到 Claude Code 的 skills 目录：

```bash
cp -r ftshare-all-in-one ~/.claude/skills/
```

安装后，新对话中即可通过自然语言触发。例如：

- "查一下贵州茅台的行情"
- "沪深 300 最近 30 日 K 线"
- "510300 ETF 成份股"
- "最新 CPI 数据"
- "搜一下人工智能相关新闻"

## 使用方式

### 方式一：直接调用脚本

```bash
# A 股行情
python scripts/stock/get_stock_detail.py --symbol 600519.SH

# ETF K 线
python scripts/etf/get_etf_ohlcs.py --etf 510050.XSHG --span DAY1 --limit 50

# 指数分时
python scripts/index/get_index_prices.py --index 000001.XSHG --since TODAY

# 基金收益率
python scripts/fund/get_fund_return.py --institution-code 159619 --cal-type 1Y

# 港股行情
python scripts/hk/get_hk_view.py --hk_code 00700.HK

# 中国 GDP
python scripts/economic/get_china_gdp.py

# 美国非农
python scripts/economic/get_us_economic.py --type nonfarm-payroll

# 新闻搜索
python scripts/news/search_news.py --query 人工智能 --limit 10

# 交易日查询
python scripts/utils/get_trade_date.py --n 5
```

### 方式二：通过 run.py 统一调度

```bash
# 分类路径（推荐）
python run.py stock/get_stock_detail --symbol 600519.SH
python run.py etf/get_etf_ohlcs --etf 510050.XSHG --span DAY1 --limit 50

# 旧名兼容
python run.py etf-detail --etf 510050.XSHG
python run.py stock-quotes-list --order_by "change_rate desc" --page_no 1 --page_size 20
```

## 常用接口速查

### A 股

| 功能 | 命令 |
|------|------|
| 股票列表 | `python scripts/stock/get_stock_list.py` |
| 股票详情 | `python scripts/stock/get_stock_detail.py --symbol 600519.SH` |
| 行情排序 | `python scripts/stock/get_stock_quotes.py --order_by "change_rate desc" --page_no 1 --page_size 20` |
| K 线 | `python scripts/stock/get_stock_ohlcs.py --stock 000001.SZ --span DAY1 --limit 50` |
| 分时 | `python scripts/stock/get_stock_prices.py --stock 000001.SZ --since TODAY` |
| IPO | `python scripts/stock/get_stock_ipos.py --page 1 --page_size 20` |
| 大宗交易 | `python scripts/stock/get_block_trades.py` |
| 融资融券 | `python scripts/stock/get_margin_trading.py --page 1 --page_size 20` |
| 资产负债表 | `python scripts/stock/get_stock_balance.py --mode single --stock-code 000001.SZ` |
| 现金流量表 | `python scripts/stock/get_stock_cashflow.py --mode single --stock-code 000001.SZ` |
| 利润表 | `python scripts/stock/get_stock_income.py --mode single --stock-code 000001.SZ` |
| 业绩快报 | `python scripts/stock/get_stock_performance.py --mode single --stock-code 000001.SZ` |
| 业绩预告 | `python scripts/stock/get_stock_performance_forecast.py --mode single --stock-code 000001.SZ` |
| 十大股东 | `python scripts/stock/get_stock_holders.py --type ten --stock_code 603323.SH` |
| 十大流通股东 | `python scripts/stock/get_stock_holders.py --type ften --stock_code 603323.SH` |
| 股东人数 | `python scripts/stock/get_stock_holders.py --type nums --stock_code 603323.SH` |
| 股权质押 | `python scripts/stock/get_pledge.py --type detail --stock_code 603323.SH` |
| 股东增减持 | `python scripts/stock/get_share_change.py --stock_code 603323.SH` |

### ETF

| 功能 | 命令 |
|------|------|
| ETF 详情 | `python scripts/etf/get_etf_detail.py --etf 510050.XSHG` |
| ETF 列表 | `python scripts/etf/get_etf_list.py --page_size 20 --page_no 1` |
| ETF K 线 | `python scripts/etf/get_etf_ohlcs.py --etf 510050.XSHG --span DAY1 --limit 50` |
| ETF 分时 | `python scripts/etf/get_etf_prices.py --etf 510050.XSHG --since TODAY` |
| ETF 成份股 | `python scripts/etf/get_etf_component.py --symbol 510300.XSHG` |
| ETF 盘前数据 | `python scripts/etf/get_etf_pre_single.py --symbol 510300.XSHG` |
| ETF PCF 列表 | `python scripts/etf/get_etf_pcfs.py --date 20260309` |
| ETF 描述 | `python scripts/etf/get_etf_description.py` |

### 指数

| 功能 | 命令 |
|------|------|
| 指数详情 | `python scripts/index/get_index_detail.py --index 000001.XSHG` |
| 指数列表 | `python scripts/index/get_index_list.py --page_size 20 --page_no 1` |
| 指数 K 线 | `python scripts/index/get_index_ohlcs.py --index 000001.XSHG --span DAY1 --limit 50` |
| 指数分时 | `python scripts/index/get_index_prices.py --index 000001.XSHG --since TODAY` |
| 指数描述 | `python scripts/index/get_index_description.py` |
| 指数权重 | `python scripts/index/get_index_weight.py --mode summary --page 1 --page-size 20` |

### 基金

| 功能 | 命令 |
|------|------|
| 基金详情 | `python scripts/fund/get_fund_detail.py --institution-code 000001` |
| 基金净值 | `python scripts/fund/get_fund_nav.py --institution-code 000001 --page 1 --page-size 50` |
| 基金收益率 | `python scripts/fund/get_fund_return.py --institution-code 159619 --cal-type 1Y` |
| 基金列表 | `python scripts/fund/get_fund_list.py --page 1 --page-size 20` |
| 基金标的 | `python scripts/fund/get_fund_symbols.py --page 1 --page-size 20` |

### 港股

| 功能 | 命令 |
|------|------|
| 港股行情 | `python scripts/hk/get_hk_view.py --hk_code 00700.HK` |
| 港股 K 线 | `python scripts/hk/get_hk_kline.py --trade-code 00700.HK --interval-unit day --until-date 2026-04-18 --since-date 2026-04-01 --limit 20` |
| 港股估值 | `python scripts/hk/get_hk_valuation.py --trade_code 00700.HK --page 1 --page_size 20` |
| 港股公司信息 | `python scripts/hk/get_company_hk.py --trade_code 00700.HK` |

### 可转债

| 功能 | 命令 |
|------|------|
| 可转债列表 | `python scripts/cb/get_cb_list.py` |
| 可转债详情 | `python scripts/cb/get_cb_base.py --symbol_code 110070.SH` |

### 宏观经济

| 功能 | 命令 |
|------|------|
| 中国 GDP | `python scripts/economic/get_china_gdp.py` |
| 中国 CPI | `python scripts/economic/get_china_cpi.py` |
| 中国 PPI | `python scripts/economic/get_china_ppi.py` |
| 中国 PMI | `python scripts/economic/get_china_pmi.py` |
| 中国 LPR | `python scripts/economic/get_china_lpr.py` |
| 货币供应量 | `python scripts/economic/get_china_money_supply.py` |
| 信贷/社融 | `python scripts/economic/get_china_credit.py` |
| 进出口 | `python scripts/economic/get_china_trade.py` |
| 财政收入 | `python scripts/economic/get_china_fiscal.py` |
| 税收 | `python scripts/economic/get_china_tax.py` |
| 社零 | `python scripts/economic/get_china_retail.py` |
| 固投 | `python scripts/economic/get_china_fai.py` |
| 工业增加值 | `python scripts/economic/get_china_industrial.py` |
| 外汇/黄金储备 | `python scripts/economic/get_china_forex.py` |
| 存准率 | `python scripts/economic/get_china_reserve.py` |
| 美国经济数据 | `python scripts/economic/get_us_economic.py --type <type>` |

美国经济数据 `--type` 可选值：`ism-manufacturing` / `ism-non-manufacturing` / `nonfarm-payroll` / `trade-balance` / `unemployment-rate` / `ppi-mom` / `cpi-mom` / `cpi-yoy` / `core-cpi-mom` / `core-cpi-yoy` / `housing-starts` / `existing-home-sales` / `durable-goods-orders-mom` / `cb-consumer-confidence` / `gdp-yoy-preliminary` / `fed-funds-rate-upper`

### 公告研报

| 功能 | 命令 |
|------|------|
| 全市场公告 | `python scripts/announcement/get_announcements.py --mode all --start-date 20260418 --page 1 --page-size 20` |
| 个股公告 | `python scripts/announcement/get_announcements.py --mode single --stock-code 000001.SZ --page 1 --page-size 20` |
| 下载公告 PDF | `python scripts/announcement/download_announcement.py --url-hash <hash> --output announcement.pdf` |
| 全市场研报 | `python scripts/announcement/get_reports.py --mode all --start-date 20260418 --page 1 --page-size 20` |
| 个股研报 | `python scripts/announcement/get_reports.py --mode single --stock-code 000001.SZ --page 1 --page-size 20` |
| 下载研报 PDF | `python scripts/announcement/download_report.py --url-hash <hash> --output report.pdf` |

### 新闻

| 功能 | 命令 |
|------|------|
| 语义搜索 | `python scripts/news/search_news.py --query 人工智能 --limit 10` |

## 连通性测试

```bash
bash test_all.sh
```

自动遍历全部接口并输出 PASS/FAIL 汇总。

## 技术细节

- **纯 Python 实现**，零外部依赖，仅使用标准库（`urllib` / `argparse` / `json`）
- **安全校验**：所有 HTTP 请求限制在 `market.ft.tech` 和 `ftai.chat` 域名白名单内
- **统一入口**：`run.py` 支持分类路径和旧名兼容两种调用方式
- **统一输出**：所有脚本返回 JSON 格式

## 代码约定

| 模块 | 说明 |
|------|------|
| `common.py` | `fetch_json()` 统一请求、`output()` 统一 JSON 输出、`paginate()` 自动翻页、`ArgParser` 带通用参数 |
| 各子脚本 | 使用 `argparse` 定义参数，调用 `common.py` 的函数发起请求 |

## License

本项目仅供学习交流使用。数据来源于非凸科技，请遵守相关使用条款。
