# 📈 日本株ダッシュボード

Streamlitベースの日本株価分析ダッシュボードです。CSVデータを使用して、インタラクティブな株価チャートとテクニカル分析を提供します。

## ✨ 機能

- 📊 **インタラクティブな株価チャート**
  - ローソク足チャート
  - 出来高表示
  - テクニカル指標（RSI、MACD、移動平均線など）
  
- 🔍 **銘柄検索・選択**
  - 銘柄コードまたは会社名での検索
  - 利用可能な銘柄の一覧表示
  
- 📈 **リアルタイム分析**
  - 現在価格と前日比
  - 52週高値・安値
  - 出来高分析
  
- 📋 **詳細データ表示**
  - 株価データのテーブル表示
  - 企業基本情報
  - 財務比率データ

## 🚀 セットアップ

### 前提条件

- Python 3.13以上
- uv（Pythonパッケージマネージャー）

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/Akira-Osanai/j-stocks-dashboard.git
cd j-stocks-dashboard
```

2. 依存関係をインストール
```bash
uv sync
```

3. アプリケーションを起動
```bash
uv run streamlit run app.py
```

## 📁 プロジェクト構造

```
j-stocks-dashboard/
├── app.py                          # メインアプリケーション
├── pyproject.toml                  # プロジェクト設定
├── src/
│   ├── data/
│   │   └── loader.py              # データローダー
│   ├── components/
│   │   └── charts.py              # チャートコンポーネント
│   └── utils/                     # ユーティリティ
├── output/                        # 株価データ（CSVファイル）
│   ├── 7203/                     # トヨタ自動車のデータ例
│   │   ├── stock_data/
│   │   ├── company_info/
│   │   ├── technical_data/
│   │   └── financial_data/
│   └── ...
└── README.md
```

## 📊 データ形式

このダッシュボードは以下のCSVファイルを読み込みます：

- `stock_data.csv`: 株価データ（OHLCV）
- `company_info.csv`: 企業基本情報
- `technical_indicators.csv`: テクニカル指標
- `financial_ratios.csv`: 財務比率

詳細なデータ仕様については、`CSV_FIELDS_REFERENCE.md`を参照してください。

## 🎨 カスタマイズ

### チャートの設定

`src/components/charts.py`でチャートの外観や機能をカスタマイズできます。

### データローダーの拡張

`src/data/loader.py`で新しいデータソースやフィルタリング機能を追加できます。

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🔗 関連リンク

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
