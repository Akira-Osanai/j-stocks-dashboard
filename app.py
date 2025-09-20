"""
日本株ダッシュボード
Streamlitベースの株価分析ツール
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# パスを追加
sys.path.append(str(Path(__file__).parent / "src"))

from data.loader import StockDataLoader
from components.charts import StockChart
from components.financial_analysis import FinancialAnalysis

# ページ設定
st.set_page_config(
    page_title="日本株ダッシュボード",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """メイン関数"""
    
    # ヘッダー
    st.markdown('<h1 class="main-header">📈 日本株ダッシュボード</h1>', unsafe_allow_html=True)
    
    # データローダーを初期化
    @st.cache_resource
    def get_data_loader():
        return StockDataLoader()
    
    data_loader = get_data_loader()
    
    # サイドバー
    with st.sidebar:
        st.header("🔍 銘柄選択")
        
        # 銘柄検索
        search_query = st.text_input("銘柄名またはコードで検索", placeholder="例: トヨタ, 7203")
        
        if search_query:
            search_results = data_loader.search_tickers(search_query)
            if search_results:
                st.write("検索結果:")
                for ticker, name in search_results[:10]:  # 最大10件表示
                    if st.button(f"{ticker}: {name}", key=f"search_{ticker}"):
                        st.session_state.selected_ticker = ticker
            else:
                st.write("該当する銘柄が見つかりませんでした")
        
        # 銘柄選択
        available_tickers = data_loader.get_available_tickers()
        
        # 表示用の銘柄リストを作成
        ticker_options = []
        for ticker in available_tickers:
            display_name = data_loader.get_ticker_display_name(ticker)
            ticker_options.append((ticker, display_name))
        
        # 選択ボックスのオプション
        ticker_display_names = [f"{ticker}: {display_name}" for ticker, display_name in ticker_options]
        
        selected_display = st.selectbox(
            "銘柄を選択してください",
            options=ticker_display_names,
            index=0 if not hasattr(st.session_state, 'selected_ticker') else 
                  next((i for i, (ticker, _) in enumerate(ticker_options) if ticker == st.session_state.selected_ticker), 0)
        )
        
        # 選択された銘柄コードを取得
        selected_ticker = next(ticker for ticker, display_name in ticker_options 
                              if f"{ticker}: {display_name}" == selected_display)
        
        # チャート設定
        st.header("📊 チャート設定")
        show_volume = st.checkbox("出来高を表示", value=True)
        chart_height = st.slider("チャートの高さ", min_value=400, max_value=800, value=600)
        
        # 日付範囲設定
        st.header("📅 期間設定")
        use_date_range = st.checkbox("期間を指定する")
        
        if use_date_range:
            start_date = st.date_input("開始日")
            end_date = st.date_input("終了日")
        else:
            start_date = None
            end_date = None
    
    # メインコンテンツ
    if selected_ticker:
        # タブを作成
        tab1, tab2 = st.tabs(["📈 株価分析", "💰 財務分析"])
        
        with tab1:
            # データの完全性をチェック
            if not data_loader.is_data_sufficient(selected_ticker):
                st.warning("⚠️ この銘柄のデータが不足しています。一部の機能が制限される可能性があります。")
                
                # データの詳細状況を表示
                completeness = data_loader.check_data_completeness(selected_ticker)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    status = "✅" if completeness['stock_data'] else "❌"
                    st.write(f"株価データ: {status}")
                
                with col2:
                    status = "✅" if completeness['company_info'] else "❌"
                    st.write(f"企業情報: {status}")
                
                with col3:
                    status = "✅" if completeness['technical_data'] else "❌"
                    st.write(f"テクニカル指標: {status}")
                
                with col4:
                    status = "✅" if completeness['financial_data'] else "❌"
                    st.write(f"財務データ: {status}")
            
            # データを読み込み
            with st.spinner(f"銘柄 {selected_ticker} のデータを読み込み中..."):
                stock_data = data_loader.load_stock_data(selected_ticker)
                company_info = data_loader.load_company_info(selected_ticker)
                technical_data = data_loader.load_technical_indicators(selected_ticker)
            
            if stock_data is not None and not stock_data.empty:
                # 日付範囲でフィルタリング
                if use_date_range and start_date and end_date:
                    stock_data = stock_data[
                        (stock_data['Date'].dt.date >= start_date) & 
                        (stock_data['Date'].dt.date <= end_date)
                    ]
                
                # フィルタリング後にデータが空でないかチェック
                if stock_data.empty:
                    st.warning("指定された期間にデータがありません。期間を変更してください。")
                    return
                
                # 銘柄情報表示
                if company_info is not None and not company_info.empty:
                    company_name = company_info.iloc[0].get('company_name', f'銘柄{selected_ticker}')
                    sector = company_info.iloc[0].get('sector', '不明')
                    industry = company_info.iloc[0].get('industry', '不明')
                    
                    st.markdown(f"### {company_name} ({selected_ticker})")
                    st.markdown(f"**セクター:** {sector} | **業界:** {industry}")
                
                # 基本統計情報
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    current_price = stock_data['Close'].iloc[-1]
                    st.metric("現在価格", f"¥{current_price:,.0f}")
                
                with col2:
                    if len(stock_data) >= 2:
                        price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
                        price_change_pct = (price_change / stock_data['Close'].iloc[-2]) * 100
                        st.metric(
                            "前日比", 
                            f"¥{price_change:+,.0f}",
                            f"{price_change_pct:+.2f}%"
                        )
                    else:
                        st.metric("前日比", "データ不足", "N/A")
                
                with col3:
                    volume = stock_data['Volume'].iloc[-1]
                    st.metric("出来高", f"{volume:,}")
                
                with col4:
                    high_52w = stock_data['High'].max()
                    low_52w = stock_data['Low'].min()
                    st.metric("52週高値", f"¥{high_52w:,.0f}")
                    st.metric("52週安値", f"¥{low_52w:,.0f}")
            
                # チャート表示
                st.markdown("### 📈 株価チャート")
                
                # ローソク足チャート
                candlestick_chart = StockChart.create_candlestick_chart(
                    stock_data,
                    title=f"{selected_ticker} 株価チャート",
                    height=chart_height,
                    show_volume=show_volume
                )
                
                st.plotly_chart(candlestick_chart, use_container_width=True)
                
                # テクニカル指標
                if technical_data is not None and not technical_data.empty:
                    # テクニカル指標も同じ日付範囲でフィルタリング
                    if use_date_range and start_date and end_date:
                        technical_data = technical_data[
                            (technical_data['Date'].dt.date >= start_date) & 
                            (technical_data['Date'].dt.date <= end_date)
                        ]
                    
                    if not technical_data.empty:
                        st.markdown("### 📊 テクニカル指標")
                        
                        technical_chart = StockChart.create_technical_indicators_chart(
                            technical_data,
                            title=f"{selected_ticker} テクニカル指標",
                            height=chart_height
                        )
                        
                        st.plotly_chart(technical_chart, use_container_width=True)
                
                # データテーブル
                with st.expander("📋 詳細データ"):
                    st.dataframe(
                        stock_data.tail(20),
                        width='stretch',
                        height=400
                    )
            
            else:
                st.error(f"銘柄 {selected_ticker} のデータが見つかりませんでした")
        
        with tab2:
            # 財務分析タブ
            st.markdown("### 💰 財務分析")
            
            # 財務データを読み込み
            with st.spinner("財務データを読み込み中..."):
                income_statement = data_loader.load_income_statement(selected_ticker)
                balance_sheet = data_loader.load_balance_sheet(selected_ticker)
                cashflow = data_loader.load_cashflow(selected_ticker)
                financial_ratios = data_loader.load_financial_ratios(selected_ticker)
            
            # データ品質の表示
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                FinancialAnalysis.display_data_quality_warning(income_statement, "損益計算書")
            
            with col2:
                FinancialAnalysis.display_data_quality_warning(balance_sheet, "貸借対照表")
            
            with col3:
                FinancialAnalysis.display_data_quality_warning(cashflow, "キャッシュフロー")
            
            with col4:
                FinancialAnalysis.display_data_quality_warning(financial_ratios, "財務比率")
            
            # 損益計算書
            if income_statement is not None and not income_statement.empty:
                st.markdown("#### 📊 損益計算書")
                income_chart = FinancialAnalysis.create_income_statement_chart(
                    income_statement,
                    title=f"{selected_ticker} 損益計算書",
                    height=500
                )
                st.plotly_chart(income_chart, use_container_width=True)
            
            # 貸借対照表
            if balance_sheet is not None and not balance_sheet.empty:
                st.markdown("#### 🏦 貸借対照表")
                balance_chart = FinancialAnalysis.create_balance_sheet_chart(
                    balance_sheet,
                    title=f"{selected_ticker} 貸借対照表",
                    height=500
                )
                st.plotly_chart(balance_chart, use_container_width=True)
            
            # キャッシュフロー計算書
            if cashflow is not None and not cashflow.empty:
                st.markdown("#### 💸 キャッシュフロー計算書")
                cashflow_chart = FinancialAnalysis.create_cashflow_chart(
                    cashflow,
                    title=f"{selected_ticker} キャッシュフロー計算書",
                    height=500
                )
                st.plotly_chart(cashflow_chart, use_container_width=True)
            
            # 財務比率
            if financial_ratios is not None and not financial_ratios.empty:
                st.markdown("#### 📈 財務比率")
                ratios_chart = FinancialAnalysis.create_financial_ratios_chart(
                    financial_ratios,
                    title=f"{selected_ticker} 財務比率",
                    height=400
                )
                st.plotly_chart(ratios_chart, use_container_width=True)
            
            # 財務データの詳細表示
            with st.expander("📋 財務データ詳細"):
                if income_statement is not None and not income_statement.empty:
                    st.markdown("**損益計算書**")
                    st.dataframe(income_statement, width='stretch', height=300)
                
                if balance_sheet is not None and not balance_sheet.empty:
                    st.markdown("**貸借対照表**")
                    st.dataframe(balance_sheet, width='stretch', height=300)
                
                if financial_ratios is not None and not financial_ratios.empty:
                    st.markdown("**財務比率**")
                    st.dataframe(financial_ratios, width='stretch', height=300)
    
    else:
        st.info("サイドバーから銘柄を選択してください")
        
        # 利用可能な銘柄の一覧表示
        st.markdown("### 📋 利用可能な銘柄")
        available_tickers = data_loader.get_available_tickers()
        
        # ページネーション
        items_per_page = 50
        total_pages = (len(available_tickers) + items_per_page - 1) // items_per_page
        
        if 'page' not in st.session_state:
            st.session_state.page = 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("前のページ", disabled=st.session_state.page == 0):
                st.session_state.page -= 1
        with col2:
            st.write(f"ページ {st.session_state.page + 1} / {total_pages}")
        with col3:
            if st.button("次のページ", disabled=st.session_state.page >= total_pages - 1):
                st.session_state.page += 1
        
        start_idx = st.session_state.page * items_per_page
        end_idx = min(start_idx + items_per_page, len(available_tickers))
        
        tickers_to_show = available_tickers[start_idx:end_idx]
        
        # 銘柄一覧を表示
        cols = st.columns(5)
        for i, ticker in enumerate(tickers_to_show):
            with cols[i % 5]:
                display_name = data_loader.get_ticker_display_name(ticker)
                if st.button(f"{ticker}\n{display_name[:10]}...", key=f"ticker_{ticker}"):
                    st.session_state.selected_ticker = ticker
                    st.rerun()

if __name__ == "__main__":
    main()
