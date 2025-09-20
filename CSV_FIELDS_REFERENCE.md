# CSV項目詳細説明書

## 概要

このドキュメントでは、日本株価データ取得システムで生成されるすべてのCSVファイルの項目について詳細に説明します。

## 株価データ

### `stock_data.csv`

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| Date | datetime | 取引日 | 2024-01-15 |
| Open | float | 始値（円） | 1500.0 |
| High | float | 高値（円） | 1550.0 |
| Low | float | 安値（円） | 1480.0 |
| Close | float | 終値（円） | 1520.0 |
| Volume | int | 出来高（株数） | 1000000 |
| Dividends | float | 配当金（円） | 10.0 |
| Stock Splits | float | 株式分割比率 | 1.0 |
| ticker | int | 証券コード | 7203 |
| 銘柄名 | string | 会社名 | トヨタ自動車 |

### `pivot_data.csv`

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| Date | datetime | 取引日 | 2024-01-15 |
| 銘柄名1 | float | 銘柄1の終値 | 1520.0 |
| 銘柄名2 | float | 銘柄2の終値 | 850.0 |
| ... | float | その他の銘柄 | ... |

## 財務データ

### `income_statement.csv` (損益計算書)

| 項目名 | データ型 | 説明 | 単位 |
|--------|----------|------|------|
| Total Revenue | float | 総収益 | 百万円 |
| Cost Of Revenue | float | 売上原価 | 百万円 |
| Gross Profit | float | 売上総利益 | 百万円 |
| Operating Income | float | 営業利益 | 百万円 |
| Net Income | float | 純利益 | 百万円 |
| Earnings Per Share | float | 1株当たり利益 | 円 |
| Research Development | float | 研究開発費 | 百万円 |
| Selling General Administrative | float | 販売費及び一般管理費 | 百万円 |
| Interest Expense | float | 支払利息 | 百万円 |
| Income Before Tax | float | 税引前利益 | 百万円 |
| Income Tax Expense | float | 法人税等 | 百万円 |

### `balance_sheet.csv` (貸借対照表)

| 項目名 | データ型 | 説明 | 単位 |
|--------|----------|------|------|
| Total Assets | float | 総資産 | 百万円 |
| Total Liabilities | float | 総負債 | 百万円 |
| Total Stockholder Equity | float | 総株主資本 | 百万円 |
| Cash And Cash Equivalents | float | 現金及び現金同等物 | 百万円 |
| Total Debt | float | 総負債 | 百万円 |
| Net Debt | float | ネット負債 | 百万円 |
| Current Assets | float | 流動資産 | 百万円 |
| Current Liabilities | float | 流動負債 | 百万円 |
| Long Term Debt | float | 長期負債 | 百万円 |
| Short Term Debt | float | 短期負債 | 百万円 |
| Retained Earnings | float | 利益剰余金 | 百万円 |
| Common Stock | float | 普通株式 | 百万円 |

### `cashflow.csv` (キャッシュフロー計算書)

| 項目名 | データ型 | 説明 | 単位 |
|--------|----------|------|------|
| Operating Cash Flow | float | 営業キャッシュフロー | 百万円 |
| Investing Cash Flow | float | 投資キャッシュフロー | 百万円 |
| Financing Cash Flow | float | 財務キャッシュフロー | 百万円 |
| Free Cash Flow | float | フリーキャッシュフロー | 百万円 |
| Net Income | float | 純利益 | 百万円 |
| Depreciation | float | 減価償却費 | 百万円 |
| Capital Expenditures | float | 設備投資 | 百万円 |
| Dividends Paid | float | 配当金支払額 | 百万円 |
| Stock Buybacks | float | 自社株買い | 百万円 |

### `financial_ratios.csv` (財務比率)

| 項目名 | データ型 | 説明 | 計算式 |
|--------|----------|------|--------|
| PER | float | 株価収益率 | 時価総額 ÷ 純利益 |
| PBR | float | 株価純資産倍率 | 時価総額 ÷ 純資産 |
| ROE | float | 自己資本利益率 | 純利益 ÷ 自己資本 × 100 |
| ROA | float | 総資産利益率 | 純利益 ÷ 総資産 × 100 |
| Debt to Equity | float | 負債対自己資本比率 | 総負債 ÷ 自己資本 |
| Current Ratio | float | 流動比率 | 流動資産 ÷ 流動負債 |
| Quick Ratio | float | 当座比率 | 当座資産 ÷ 流動負債 |
| Interest Coverage | float | インタレスト・カバレッジ | 営業利益 ÷ 支払利息 |
| Asset Turnover | float | 総資産回転率 | 売上高 ÷ 総資産 |
| Inventory Turnover | float | 在庫回転率 | 売上原価 ÷ 平均在庫 |
| Receivables Turnover | float | 売上債権回転率 | 売上高 ÷ 平均売上債権 |
| Gross Margin | float | 売上総利益率 | 売上総利益 ÷ 売上高 × 100 |
| Operating Margin | float | 営業利益率 | 営業利益 ÷ 売上高 × 100 |
| Net Margin | float | 純利益率 | 純利益 ÷ 売上高 × 100 |

## 企業基本情報・配当データ

### `company_info.csv` (企業基本情報)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| company_name | string | 会社名 | トヨタ自動車株式会社 |
| sector | string | セクター | Consumer Discretionary |
| industry | string | 業界 | Auto Manufacturers |
| sector_category | string | 業種詳細分類 | 製造業 |
| market_cap | float | 時価総額 | 25000000000000 |
| market_cap_billion | float | 時価総額（億円） | 2500000.0 |
| employees | int | 従業員数 | 372817 |
| company_size | string | 企業規模分類 | 超大規模 |
| estimated_market | string | 上場市場推定 | プライム |
| country | string | 国 | Japan |
| website | string | ウェブサイト | https://www.toyota.co.jp |
| city | string | 本社所在地 | 愛知県 |
| state | string | 都道府県 | 愛知県 |
| zip | string | 郵便番号 | 471-8571 |
| phone | string | 電話番号 | 0565-28-2121 |
| address1 | string | 住所1 | 豊田市トヨタ町1番地 |
| address2 | string | 住所2 | - |
| description | string | 企業説明 | 自動車の製造・販売 |

### `dividend_data.csv` (配当履歴)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| date | datetime | 配当日 | 2024-03-31 |
| dividend | float | 配当金額（円） | 120.0 |
| ticker | int | 証券コード | 7203 |

### `dividend_analysis.csv` (配当分析)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| has_dividends | bool | 配当の有無 | True |
| total_dividends | float | 総配当額 | 1200.0 |
| dividend_yield | float | 配当利回り（%） | 2.5 |
| dividend_frequency | string | 配当頻度 | 四半期配当 |
| last_dividend_date | datetime | 最新配当日 | 2024-03-31 |
| dividend_growth_rate | float | 配当成長率（年率%） | 5.2 |
| dividend_consistency | float | 配当の一貫性スコア（%） | 85.0 |
| dividend_count | int | 配当回数 | 20 |
| average_dividend | float | 平均配当額 | 60.0 |

## アナリスト予測データ

### `recommendations.csv` (アナリスト推奨)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| strongBuy | int | 強気買い推奨数 | 5 |
| buy | int | 買い推奨数 | 8 |
| hold | int | 中立推奨数 | 3 |
| sell | int | 売り推奨数 | 1 |
| strongSell | int | 強気売り推奨数 | 0 |

### `earnings_forecasts.csv` (業績予想)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| date | datetime | 予想日 | 2024-01-15 |
| revenue_estimate | float | 売上予想（百万円） | 30000000 |
| earnings_estimate | float | 利益予想（百万円） | 2500000 |
| revenue_actual | float | 売上実績（百万円） | 29500000 |
| earnings_actual | float | 利益実績（百万円） | 2400000 |

### `price_targets.csv` (価格目標)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| date | datetime | 目標設定日 | 2024-01-15 |
| target_price | float | 目標株価（円） | 1800.0 |
| current_price | float | 現在株価（円） | 1500.0 |
| upside_potential | float | 上昇余地（%） | 20.0 |

## テクニカル指標データ

### `technical_indicators.csv` (テクニカル指標)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| Date | datetime | 日付 | 2024-01-15 |
| Open | float | 始値 | 1500.0 |
| High | float | 高値 | 1550.0 |
| Low | float | 安値 | 1480.0 |
| Close | float | 終値 | 1520.0 |
| Volume | int | 出来高 | 1000000 |
| SMA_5 | float | 5日単純移動平均 | 1510.0 |
| SMA_10 | float | 10日単純移動平均 | 1505.0 |
| SMA_20 | float | 20日単純移動平均 | 1500.0 |
| SMA_50 | float | 50日単純移動平均 | 1480.0 |
| SMA_100 | float | 100日単純移動平均 | 1450.0 |
| SMA_200 | float | 200日単純移動平均 | 1400.0 |
| EMA_12 | float | 12日指数移動平均 | 1512.0 |
| EMA_26 | float | 26日指数移動平均 | 1508.0 |
| EMA_50 | float | 50日指数移動平均 | 1490.0 |
| MACD | float | MACDライン | 4.0 |
| MACD_Signal | float | MACDシグナル | 2.0 |
| MACD_Histogram | float | MACDヒストグラム | 2.0 |
| RSI | float | 相対力指数 | 65.5 |
| BB_Upper | float | ボリンジャーバンド上 | 1580.0 |
| BB_Middle | float | ボリンジャーバンド中 | 1500.0 |
| BB_Lower | float | ボリンジャーバンド下 | 1420.0 |
| BB_Width | float | バンド幅 | 160.0 |
| BB_Position | float | バンドポジション | 0.5 |
| Stoch_K | float | ストキャスティクス%K | 75.0 |
| Stoch_D | float | ストキャスティクス%D | 70.0 |
| Williams_R | float | ウィリアムズ%R | -25.0 |
| ATR | float | 平均真の範囲 | 25.0 |
| Volume_SMA_10 | float | 10日出来高移動平均 | 1200000 |
| Volume_SMA_20 | float | 20日出来高移動平均 | 1100000 |
| Volume_Ratio | float | 出来高比率 | 0.91 |
| OBV | float | オン・バランス・ボリューム | 50000000 |

### `technical_signals.csv` (テクニカルシグナル)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| trend_signal | string | トレンドシグナル | 強気 |
| momentum_signal | string | モメンタムシグナル | 強気 |
| volatility_signal | string | ボラティリティシグナル | 中程度 |
| volume_signal | string | 出来高シグナル | 高出来高 |
| overall_signal | string | 総合シグナル | 買い |
| current_price | float | 現在価格 | 1520.0 |
| rsi | float | RSI値 | 65.5 |
| macd | float | MACD値 | 4.0 |
| bb_position | float | ボリンジャーバンドポジション | 0.5 |

## ニュース・センチメントデータ

### `news_data.csv` (ニュースデータ)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| uuid | string | ニュースID | abc123def456 |
| title | string | タイトル | トヨタ自動車、四半期決算で増益 |
| summary | string | 要約 | トヨタ自動車は... |
| providerPublishTime | int | 公開日時（Unix時間） | 1704067200 |
| publisher | string | 出版社 | 日本経済新聞 |

### `news_analysis.csv` (センチメント分析)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| has_news | bool | ニュースの有無 | True |
| total_news | int | 総ニュース数 | 25 |
| positive_news | int | ポジティブニュース数 | 15 |
| negative_news | int | ネガティブニュース数 | 5 |
| neutral_news | int | ニュートラルニュース数 | 5 |
| overall_sentiment | string | 全体センチメント | positive |
| sentiment_score | float | センチメントスコア | 0.3 |
| confidence | float | 信頼度スコア | 0.8 |
| recent_sentiment_trend | string | 最近のセンチメントトレンド | improving |
| news_frequency | string | ニュース頻度 | high |
| recent_news_count | int | 最近のニュース数（過去7日） | 8 |
| news_diversity | float | ニュース多様性 | 0.7 |

## サマリーファイル

### `company_summary.csv` (企業基本情報サマリー)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| company_name | string | 会社名 | トヨタ自動車株式会社 |
| sector | string | セクター | Consumer Discretionary |
| industry | string | 業界 | Auto Manufacturers |
| sector_category | string | 業種詳細分類 | 製造業 |
| market_cap_billion | float | 時価総額（億円） | 2500000.0 |
| employees | int | 従業員数 | 372817 |
| company_size | string | 企業規模分類 | 超大規模 |
| estimated_market | string | 上場市場推定 | プライム |
| country | string | 国 | Japan |
| website | string | ウェブサイト | https://www.toyota.co.jp |

### `dividend_summary.csv` (配当分析サマリー)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| has_dividends | bool | 配当の有無 | True |
| total_dividends | float | 総配当額 | 1200.0 |
| dividend_yield | float | 配当利回り（%） | 2.5 |
| dividend_frequency | string | 配当頻度 | 四半期配当 |
| dividend_growth_rate | float | 配当成長率（年率%） | 5.2 |
| dividend_consistency | float | 配当の一貫性スコア（%） | 85.0 |
| dividend_count | int | 配当回数 | 20 |
| average_dividend | float | 平均配当額 | 60.0 |

### `technical_signals_summary.csv` (テクニカルシグナルサマリー)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| trend_signal | string | トレンドシグナル | 強気 |
| momentum_signal | string | モメンタムシグナル | 強気 |
| volatility_signal | string | ボラティリティシグナル | 中程度 |
| volume_signal | string | 出来高シグナル | 高出来高 |
| overall_signal | string | 総合シグナル | 買い |
| current_price | float | 現在価格 | 1520.0 |
| rsi | float | RSI値 | 65.5 |
| macd | float | MACD値 | 4.0 |
| bb_position | float | ボリンジャーバンドポジション | 0.5 |

### `news_sentiment_summary.csv` (ニュース・センチメントサマリー)

| 項目名 | データ型 | 説明 | 例 |
|--------|----------|------|-----|
| ticker | int | 証券コード | 7203 |
| has_news | bool | ニュースの有無 | True |
| total_news | int | 総ニュース数 | 25 |
| positive_news | int | ポジティブニュース数 | 15 |
| negative_news | int | ネガティブニュース数 | 5 |
| neutral_news | int | ニュートラルニュース数 | 5 |
| overall_sentiment | string | 全体センチメント | positive |
| sentiment_score | float | センチメントスコア | 0.3 |
| confidence | float | 信頼度スコア | 0.8 |
| recent_sentiment_trend | string | 最近のセンチメントトレンド | improving |
| news_frequency | string | ニュース頻度 | high |
| recent_news_count | int | 最近のニュース数（過去7日） | 8 |
| news_diversity | float | ニュース多様性 | 0.7 |

## データ型の説明

### 基本データ型
- **int**: 整数
- **float**: 浮動小数点数
- **string**: 文字列
- **bool**: 真偽値（True/False）
- **datetime**: 日時

### 特別な値
- **NaN**: データが存在しない場合
- **None**: 値が設定されていない場合
- **空文字列**: 文字列データが存在しない場合

### 単位
- **円**: 日本円
- **百万円**: 百万円単位
- **%**: パーセント
- **株数**: 株式数
- **Unix時間**: 1970年1月1日からの秒数

## 注意事項

1. **データの更新頻度**: データは日次で更新されます
2. **欠損データ**: 一部の項目でデータが取得できない場合があります
3. **計算精度**: 浮動小数点数の計算精度により、微小な誤差が生じる場合があります
4. **データソース**: すべてのデータはYahoo Financeから取得されています
5. **利用規約**: Yahoo Financeの利用規約に従ってご利用ください
