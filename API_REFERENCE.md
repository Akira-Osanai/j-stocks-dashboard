# 🔧 API仕様書

## 概要

日本株ダッシュボードの内部API仕様書です。各コンポーネントの使用方法とパラメータを説明します。

## 📊 データローダー（StockDataLoader）

### 基本情報
- **ファイル**: `src/data/loader.py`
- **クラス**: `StockDataLoader`

### 主要メソッド

#### 株価データ関連

```python
def load_stock_data(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 指定された銘柄の株価データを読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード（例：`"7203"`）
- **戻り値**: 株価データのDataFrame（Date, Open, High, Low, Close, Volume列を含む）

```python
def load_company_info(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 指定された銘柄の企業情報を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 企業情報のDataFrame（company_name, sector, industry列を含む）

```python
def load_technical_indicators(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 指定された銘柄のテクニカル指標を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: テクニカル指標のDataFrame

#### 財務データ関連

```python
def load_income_statement(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 損益計算書を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 損益計算書のDataFrame（各行が異なる年度のデータ）

```python
def load_balance_sheet(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 貸借対照表を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 貸借対照表のDataFrame

```python
def load_cashflow(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: キャッシュフロー計算書を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: キャッシュフロー計算書のDataFrame

```python
def load_financial_ratios(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 財務比率を読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 財務比率のDataFrame（ticker, ratio, value列を含む）

#### 配当データ関連

```python
def load_dividend_data(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 配当履歴データを読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 配当データのDataFrame（date, dividend, ticker, year列を含む）

```python
def load_dividend_analysis(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: 配当分析データを読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 配当分析のDataFrame

```python
def load_news_data(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: ニュースデータを読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: ニュースデータのDataFrame（id, content列を含む）

```python
def load_news_analysis(self, ticker: str) -> Optional[pd.DataFrame]
```
- **説明**: ニュース分析データを読み込み
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: ニュース分析のDataFrame

#### ユーティリティメソッド

```python
def get_available_tickers(self) -> List[str]
```
- **説明**: 利用可能な銘柄コードの一覧を取得
- **戻り値**: 銘柄コードのリスト

```python
def get_ticker_name(self, ticker: str) -> str
```
- **説明**: 銘柄コードから銘柄名を取得
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 銘柄名（文字列）

```python
def get_ticker_display_name(self, ticker: str) -> str
```
- **説明**: 表示用の銘柄名を取得（データ不足の場合は記号を付加）
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 表示用銘柄名（データ不足の場合は⚠️マーク付き）

```python
def check_data_completeness(self, ticker: str) -> Dict[str, bool]
```
- **説明**: 銘柄のデータ完全性をチェック
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: 各データタイプの存在フラグ（辞書）

```python
def is_data_sufficient(self, ticker: str) -> bool
```
- **説明**: データが十分かどうかを判定
- **パラメータ**:
  - `ticker` (str): 銘柄コード
- **戻り値**: データが十分な場合はTrue

## 📈 チャートコンポーネント（StockChart）

### 基本情報
- **ファイル**: `src/components/charts.py`
- **クラス**: `StockChart`

### 主要メソッド

```python
def create_candlestick_chart(
    self,
    df: pd.DataFrame,
    show_volume: bool = True,
    height: int = 600
) -> go.Figure
```
- **説明**: ローソク足チャートを作成
- **パラメータ**:
  - `df` (pd.DataFrame): 株価データ
  - `show_volume` (bool): 出来高を表示するか
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_technical_indicators_chart(
    self,
    df: pd.DataFrame,
    height: int = 400
) -> go.Figure
```
- **説明**: テクニカル指標チャートを作成
- **パラメータ**:
  - `df` (pd.DataFrame): テクニカル指標データ
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

## 💰 財務分析コンポーネント（FinancialAnalysis）

### 基本情報
- **ファイル**: `src/components/financial_analysis.py`
- **クラス**: `FinancialAnalysis`

### 主要メソッド

#### チャート作成メソッド

```python
def create_income_statement_chart(
    df: pd.DataFrame,
    title: str = "損益計算書",
    height: int = 600
) -> go.Figure
```
- **説明**: 損益計算書の可視化
- **パラメータ**:
  - `df` (pd.DataFrame): 損益計算書のDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_balance_sheet_chart(
    df: pd.DataFrame,
    title: str = "貸借対照表",
    height: int = 600
) -> go.Figure
```
- **説明**: 貸借対照表の可視化
- **パラメータ**:
  - `df` (pd.DataFrame): 貸借対照表のDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_cashflow_chart(
    df: pd.DataFrame,
    title: str = "キャッシュフロー計算書",
    height: int = 600
) -> go.Figure
```
- **説明**: キャッシュフロー計算書の可視化
- **パラメータ**:
  - `df` (pd.DataFrame): キャッシュフロー計算書のDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_profitability_analysis_chart(
    df: pd.DataFrame,
    title: str = "収益性分析",
    height: int = 500
) -> go.Figure
```
- **説明**: 収益性分析の可視化
- **パラメータ**:
  - `df` (pd.DataFrame): 損益計算書のDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

#### ユーティリティメソッド

```python
def display_data_quality_warning(df: pd.DataFrame, data_type: str) -> None
```
- **説明**: データ品質の警告を表示
- **パラメータ**:
  - `df` (pd.DataFrame): データのDataFrame
  - `data_type` (str): データの種類

## 💎 配当分析コンポーネント（DividendAnalysis）

### 基本情報
- **ファイル**: `src/components/dividend_analysis.py`
- **クラス**: `DividendAnalysis`

### 主要メソッド

#### チャート作成メソッド

```python
def create_dividend_timeline_chart(
    df: pd.DataFrame,
    title: str = "配当履歴",
    height: int = 500
) -> go.Figure
```
- **説明**: 配当履歴のタイムライン表示
- **パラメータ**:
  - `df` (pd.DataFrame): 配当データのDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_dividend_yield_chart(
    dividend_data: pd.DataFrame,
    stock_data: pd.DataFrame,
    title: str = "配当利回り推移",
    height: int = 500
) -> go.Figure
```
- **説明**: 配当利回りの推移を表示
- **パラメータ**:
  - `dividend_data` (pd.DataFrame): 配当データのDataFrame
  - `stock_data` (pd.DataFrame): 株価データのDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_dividend_growth_chart(
    df: pd.DataFrame,
    title: str = "配当成長率",
    height: int = 400
) -> go.Figure
```
- **説明**: 配当成長率の推移を表示
- **パラメータ**:
  - `df` (pd.DataFrame): 配当データのDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

```python
def create_dividend_consistency_chart(
    df: pd.DataFrame,
    title: str = "配当の一貫性",
    height: int = 400
) -> go.Figure
```
- **説明**: 配当の一貫性を表示
- **パラメータ**:
  - `df` (pd.DataFrame): 配当データのDataFrame
  - `title` (str): チャートのタイトル
  - `height` (int): チャートの高さ
- **戻り値**: PlotlyのFigureオブジェクト

#### ユーティリティメソッド

```python
def display_dividend_summary(
    dividend_analysis: pd.DataFrame,
    dividend_data: pd.DataFrame
) -> None
```
- **説明**: 配当サマリー情報を表示
- **パラメータ**:
  - `dividend_analysis` (pd.DataFrame): 配当分析データのDataFrame
  - `dividend_data` (pd.DataFrame): 配当データのDataFrame

```python
def display_data_quality_warning(df: pd.DataFrame, data_type: str) -> None
```
- **説明**: データ品質の警告を表示
- **パラメータ**:
  - `df` (pd.DataFrame): データのDataFrame
  - `data_type` (str): データの種類

## 📁 データ構造

### 株価データ（stock_data.csv）
```csv
Date,Open,High,Low,Close,Volume
2024-01-01,2500,2550,2480,2520,1000000
```

### 企業情報（company_info.csv）
```csv
ticker,company_name,sector,industry
7203,トヨタ自動車,自動車,自動車製造
```

### 財務データ（income_statement.csv）
```csv
Total Revenue,Gross Profit,Operating Income,Net Income
144904000000,109899000000,51660000000,41731000000
99981000000,72116000000,26958000000,17584000000
```

### 配当データ（dividend_data.csv）
```csv
date,dividend,ticker,year
2024-03-27,3.333333,8136,2024
2023-03-27,3.333333,8136,2023
```

## 🔧 カスタマイズ

### 新しいチャートの追加

1. 適切なコンポーネントファイルにメソッドを追加
2. メソッドは`go.Figure`を返すように実装
3. アプリケーションファイル（`app.py`）で呼び出し

### 新しいデータソースの追加

1. `StockDataLoader`クラスに新しいメソッドを追加
2. データの読み込みと前処理を実装
3. エラーハンドリングを含める

### スタイルのカスタマイズ

- チャートの色は`colors`配列で定義
- レイアウトは`fig.update_layout()`で設定
- テンプレートは`template="plotly_white"`で統一

## 5. NewsSentimentAnalysis クラス

### 概要
ニュース・センチメント分析を表示するクラス

### メソッド

#### create_sentiment_overview_chart(news_analysis, title, height)
センチメント概要の円グラフを作成

**パラメータ:**
- `news_analysis` (pd.DataFrame): ニュース分析データのDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_sentiment_timeline_chart(news_data, title, height)
センチメントの時系列推移を表示

**パラメータ:**
- `news_data` (pd.DataFrame): ニュースデータのDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_news_source_chart(news_data, title, height)
ニュースソースの分析チャートを作成

**パラメータ:**
- `news_data` (pd.DataFrame): ニュースデータのDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_sentiment_score_chart(news_analysis, title, height)
センチメントスコアの表示

**パラメータ:**
- `news_analysis` (pd.DataFrame): ニュース分析データのDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### display_news_summary(news_analysis, news_data)
ニュースサマリー情報を表示

**パラメータ:**
- `news_analysis` (pd.DataFrame): ニュース分析データのDataFrame
- `news_data` (pd.DataFrame): ニュースデータのDataFrame

#### display_news_list(news_data, max_news)
ニュース一覧を表示

**パラメータ:**
- `news_data` (pd.DataFrame): ニュースデータのDataFrame
- `max_news` (int): 表示する最大ニュース数

#### display_data_quality_warning(df, data_type)
データ品質の警告を表示

**パラメータ:**
- `df` (pd.DataFrame): データのDataFrame
- `data_type` (str): データの種類

### ニュースデータの構造

#### ニュースデータ（news_data.csv）
```csv
id,content
d4f7ffb7-e65a-359e-b390-916f10bef293,"{'id': 'd4f7ffb7-e65a-359e-b390-916f10bef293', 'contentType': 'STORY', 'title': 'Sanrio (TSE:8136): Evaluating Valuation After Strong Share Price Momentum', 'summary': '...', 'pubDate': '2025-09-10T11:13:45Z', 'provider': {'displayName': 'Simply Wall St.'}, ...}"
```

#### ニュース分析データ（news_analysis.csv）
```csv
ticker,has_news,total_news,news_frequency,positive_news,negative_news,neutral_news,overall_sentiment,sentiment_score,confidence
8136,True,5,low,0,0,5,neutral,0.0,0.0
```

## 6. SectorAnalysis クラス

### 概要
セクター分析を表示するクラス

### メソッド

#### load_sector_data()
全銘柄のセクター情報を読み込み

**戻り値:**
- `pd.DataFrame`: セクター情報のDataFrame

#### create_sector_overview_chart(sector_data, title, height)
セクター別銘柄数の円グラフを作成

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_sector_performance_chart(sector_data, title, height)
セクター別のパフォーマンス比較チャートを作成

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_industry_analysis_chart(sector_data, selected_sector, title, height)
選択されたセクター内の業界分析チャートを作成

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame
- `selected_sector` (str): 選択されたセクター
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### create_company_comparison_chart(sector_data, selected_sector, title, height)
セクター内の銘柄比較チャートを作成

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame
- `selected_sector` (str): 選択されたセクター
- `title` (str): チャートのタイトル
- `height` (int): チャートの高さ

**戻り値:**
- `go.Figure`: PlotlyのFigureオブジェクト

#### display_sector_summary(sector_data)
セクターサマリー情報を表示

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame

#### display_company_list(sector_data, selected_sector, max_companies)
セクター内の銘柄一覧を表示

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame
- `selected_sector` (str): 選択されたセクター
- `max_companies` (int): 表示する最大銘柄数

#### display_data_quality_warning(sector_data)
データ品質の警告を表示

**パラメータ:**
- `sector_data` (pd.DataFrame): セクター情報のDataFrame

### セクターデータの構造

#### 企業情報データ（company_info.csv）
```csv
ticker,symbol,company_name,sector,industry,market_cap,employees,website,description,country,city,state,zip,phone,ceo,exchange,currency,timezone,quote_type,shares_outstanding,float_shares,implied_shares_outstanding,market_cap_billion,company_size,sector_category,estimated_market
8136,8136.T,"Sanrio Company, Ltd.",Consumer Cyclical,Specialty Retail,1613077544960,1445,https://www.sanrio.co.jp,"...",Japan,Tokyo,,141-8603,81 3 3779 8111,,JPX,JPY,,EQUITY,237287077,185911510,240882336,1613.07754496,超大規模,製造業,プライム
```

#### 株価データ（stock_data.csv）
```csv
Open,High,Low,Close,Volume,Dividends,Stock Splits,ticker,Date,銘柄名,Capital Gains
488.2814025878906,488.2814025878906,488.2814025878906,488.2814025878906,0,0.0,0.0,8136,2001-01-01,サンリオ,
```
