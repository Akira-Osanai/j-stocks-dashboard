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
        selected_ticker = st.selectbox(
            "銘柄を選択してください",
            options=available_tickers,
            index=0 if not hasattr(st.session_state, 'selected_ticker') else 
                  available_tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in available_tickers else 0
        )
        
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
                price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
                price_change_pct = (price_change / stock_data['Close'].iloc[-2]) * 100
                st.metric(
                    "前日比", 
                    f"¥{price_change:+,.0f}",
                    f"{price_change_pct:+.2f}%"
                )
            
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
                    use_container_width=True,
                    height=400
                )
        
        else:
            st.error(f"銘柄 {selected_ticker} のデータが見つかりませんでした")
    
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
                company_name = data_loader.get_ticker_name(ticker)
                if st.button(f"{ticker}\n{company_name[:10]}...", key=f"ticker_{ticker}"):
                    st.session_state.selected_ticker = ticker
                    st.rerun()

if __name__ == "__main__":
    main()
