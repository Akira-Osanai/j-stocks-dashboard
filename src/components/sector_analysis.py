"""
セクター分析コンポーネント

業界別比較とセクター別パフォーマンス分析機能を提供
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional, Dict, List, Tuple
import numpy as np
from pathlib import Path
import json


class SectorAnalysis:
    """セクター分析を表示するクラス"""
    
    def __init__(self, data_dir: Path):
        """
        セクター分析の初期化
        
        Args:
            data_dir: データディレクトリのパス
        """
        self.data_dir = data_dir
    
    def load_sector_data(self) -> pd.DataFrame:
        """
        全銘柄のセクター情報を読み込み
        
        Returns:
            セクター情報のDataFrame
        """
        sector_data = []
        
        # 利用可能な銘柄を取得
        available_tickers = self._get_available_tickers()
        
        for ticker in available_tickers:
            try:
                company_info_path = self.data_dir / ticker / "company_info" / "company_info.csv"
                if company_info_path.exists():
                    df = pd.read_csv(company_info_path)
                    if not df.empty:
                        # 株価データも取得（オプション）
                        stock_data = self._load_stock_data(ticker)
                        latest_price = 0
                        price_change = 0
                        
                        if stock_data is not None and not stock_data.empty:
                            # 最新の株価情報を取得（列名の大文字小文字を確認）
                            close_column = 'Close' if 'Close' in stock_data.columns else 'close'
                            if close_column in stock_data.columns:
                                latest_price = stock_data[close_column].iloc[-1]
                                if len(stock_data) >= 2:
                                    price_change = ((stock_data[close_column].iloc[-1] - stock_data[close_column].iloc[-2]) / stock_data[close_column].iloc[-2]) * 100
                            else:
                                latest_price = 0
                                price_change = 0
                        
                        # 株価データがなくてもセクター情報は追加
                        sector_data.append({
                            'ticker': ticker,
                            'company_name': df['company_name'].iloc[0],
                            'sector': df['sector'].iloc[0],
                            'industry': df['industry'].iloc[0],
                            'sector_category': df['sector_category'].iloc[0],
                            'market_cap': df['market_cap'].iloc[0],
                            'market_cap_billion': df['market_cap_billion'].iloc[0],
                            'company_size': df['company_size'].iloc[0],
                            'current_price': latest_price,
                            'price_change': price_change,
                            'employees': df['employees'].iloc[0] if 'employees' in df.columns else 0
                        })
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")
                continue
        return pd.DataFrame(sector_data)
    
    def _get_available_tickers(self) -> List[str]:
        """利用可能な銘柄コードの一覧を取得"""
        try:
            tickers = []
            for item in self.data_dir.iterdir():
                if item.is_dir() and item.name.isdigit():
                    tickers.append(item.name)
            return sorted(tickers)
        except Exception as e:
            print(f"Error getting available tickers: {e}")
            return []
    
    def _load_stock_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """株価データを読み込み"""
        try:
            stock_data_path = self.data_dir / ticker / "stock_data" / "stock_data.csv"
            if stock_data_path.exists():
                df = pd.read_csv(stock_data_path)
                # 日付列の処理（Date列またはdate列）
                date_column = 'Date' if 'Date' in df.columns else 'date'
                if date_column in df.columns:
                    df[date_column] = pd.to_datetime(df[date_column])
                return df
            return None
        except Exception as e:
            print(f"Error loading stock data for {ticker}: {e}")
            return None
    
    def create_sector_overview_chart(
        self,
        sector_data: pd.DataFrame,
        title: str = "セクター別銘柄数",
        height: int = 500
    ) -> go.Figure:
        """
        セクター別銘柄数の円グラフを作成
        
        Args:
            sector_data: セクター情報のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if sector_data is None or sector_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="セクターデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # セクター別の銘柄数をカウント
        sector_counts = sector_data['sector'].value_counts()
        
        # 円グラフを作成
        fig = go.Figure(data=[go.Pie(
            labels=sector_counts.index,
            values=sector_counts.values,
            hole=0.4,
            textinfo='label+percent+value',
            textfont_size=12
        )])
        
        fig.update_layout(
            title=title,
            height=height,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.01
            )
        )
        
        return fig
    
    def create_sector_performance_chart(
        self,
        sector_data: pd.DataFrame,
        title: str = "セクター別パフォーマンス",
        height: int = 600
    ) -> go.Figure:
        """
        セクター別のパフォーマンス比較チャートを作成
        
        Args:
            sector_data: セクター情報のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if sector_data is None or sector_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="セクターデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # セクター別の平均価格変動率を計算
        sector_performance = sector_data.groupby('sector').agg({
            'price_change': 'mean',
            'ticker': 'count',
            'market_cap_billion': 'sum'
        }).reset_index()
        
        sector_performance.columns = ['sector', 'avg_price_change', 'company_count', 'total_market_cap']
        
        # サブプロットを作成
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('セクター別平均価格変動率', 'セクター別時価総額'),
            vertical_spacing=0.1
        )
        
        # 価格変動率の棒グラフ
        colors = ['green' if x > 0 else 'red' for x in sector_performance['avg_price_change']]
        fig.add_trace(
            go.Bar(
                x=sector_performance['sector'],
                y=sector_performance['avg_price_change'],
                name='平均価格変動率 (%)',
                marker_color=colors,
                text=sector_performance['avg_price_change'].round(2),
                textposition='auto'
            ),
            row=1, col=1
        )
        
        # 時価総額の棒グラフ
        fig.add_trace(
            go.Bar(
                x=sector_performance['sector'],
                y=sector_performance['total_market_cap'],
                name='時価総額 (十億円)',
                marker_color='#1f77b4',
                text=sector_performance['total_market_cap'].round(0),
                textposition='auto'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=title,
            height=height,
            showlegend=True,
            template="plotly_white"
        )
        
        # 軸ラベルを設定
        fig.update_xaxes(title_text="セクター", row=1, col=1)
        fig.update_xaxes(title_text="セクター", row=2, col=1)
        fig.update_yaxes(title_text="平均価格変動率 (%)", row=1, col=1)
        fig.update_yaxes(title_text="時価総額 (十億円)", row=2, col=1)
        
        return fig
    
    def create_industry_analysis_chart(
        self,
        sector_data: pd.DataFrame,
        selected_sector: str,
        title: str = "業界内分析",
        height: int = 500
    ) -> go.Figure:
        """
        選択されたセクター内の業界分析チャートを作成
        
        Args:
            sector_data: セクター情報のDataFrame
            selected_sector: 選択されたセクター
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if sector_data is None or sector_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="セクターデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 選択されたセクターのデータをフィルタリング
        sector_filtered = sector_data[sector_data['sector'] == selected_sector]
        
        if sector_filtered.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"{selected_sector}セクターのデータがありません",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 業界別の集計
        industry_analysis = sector_filtered.groupby('industry').agg({
            'ticker': 'count',
            'price_change': 'mean',
            'market_cap_billion': 'sum'
        }).reset_index()
        
        industry_analysis.columns = ['industry', 'company_count', 'avg_price_change', 'total_market_cap']
        
        # バブルチャートを作成
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=industry_analysis['avg_price_change'],
            y=industry_analysis['total_market_cap'],
            mode='markers+text',
            text=industry_analysis['industry'],
            textposition='top center',
            marker=dict(
                size=industry_analysis['company_count'] * 10,
                color=industry_analysis['avg_price_change'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="平均価格変動率 (%)")
            ),
            name='業界'
        ))
        
        fig.update_layout(
            title=f"{selected_sector} - {title}",
            height=height,
            xaxis_title="平均価格変動率 (%)",
            yaxis_title="時価総額 (十億円)",
            template="plotly_white"
        )
        
        return fig
    
    def create_company_comparison_chart(
        self,
        sector_data: pd.DataFrame,
        selected_sector: str,
        title: str = "銘柄比較",
        height: int = 600
    ) -> go.Figure:
        """
        セクター内の銘柄比較チャートを作成
        
        Args:
            sector_data: セクター情報のDataFrame
            selected_sector: 選択されたセクター
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if sector_data is None or sector_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="セクターデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 選択されたセクターのデータをフィルタリング
        sector_filtered = sector_data[sector_data['sector'] == selected_sector]
        
        if sector_filtered.empty:
            fig = go.Figure()
            fig.add_annotation(
                text=f"{selected_sector}セクターのデータがありません",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 時価総額でソート（上位20銘柄）
        top_companies = sector_filtered.nlargest(20, 'market_cap_billion')
        
        # バブルチャートを作成
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=top_companies['market_cap_billion'],
            y=top_companies['price_change'],
            mode='markers+text',
            text=top_companies['company_name'],
            textposition='top center',
            marker=dict(
                size=top_companies['employees'] / 1000,  # 従業員数をサイズに反映
                color=top_companies['price_change'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="価格変動率 (%)")
            ),
            name='銘柄'
        ))
        
        fig.update_layout(
            title=f"{selected_sector} - {title}",
            height=height,
            xaxis_title="時価総額 (十億円)",
            yaxis_title="価格変動率 (%)",
            template="plotly_white"
        )
        
        return fig
    
    def display_sector_summary(self, sector_data: pd.DataFrame) -> None:
        """
        セクターサマリー情報を表示
        
        Args:
            sector_data: セクター情報のDataFrame
        """
        if sector_data is None or sector_data.empty:
            st.warning("セクターデータが不足しています")
            return
        
        # 基本統計
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "総銘柄数",
                f"{len(sector_data)}銘柄",
                help="分析対象の銘柄数"
            )
        
        with col2:
            st.metric(
                "セクター数",
                f"{sector_data['sector'].nunique()}セクター",
                help="異なるセクターの数"
            )
        
        with col3:
            avg_change = sector_data['price_change'].mean()
            st.metric(
                "平均価格変動率",
                f"{avg_change:.2f}%",
                f"{'上昇' if avg_change > 0 else '下落'}"
            )
        
        with col4:
            total_market_cap = sector_data['market_cap_billion'].sum()
            st.metric(
                "総時価総額",
                f"{total_market_cap:,.0f}十億円",
                help="全銘柄の時価総額合計"
            )
        
        # セクター別の詳細
        st.markdown("#### 📊 セクター別詳細")
        sector_summary = sector_data.groupby('sector').agg({
            'ticker': 'count',
            'price_change': 'mean',
            'market_cap_billion': 'sum',
            'employees': 'sum'
        }).round(2)
        
        sector_summary.columns = ['銘柄数', '平均価格変動率(%)', '時価総額(十億円)', '総従業員数']
        sector_summary = sector_summary.sort_values('時価総額(十億円)', ascending=False)
        
        st.dataframe(sector_summary, use_container_width=True)
    
    def display_company_list(
        self,
        sector_data: pd.DataFrame,
        selected_sector: str,
        max_companies: int = 20
    ) -> None:
        """
        セクター内の銘柄一覧を表示
        
        Args:
            sector_data: セクター情報のDataFrame
            selected_sector: 選択されたセクター
            max_companies: 表示する最大銘柄数
        """
        if sector_data is None or sector_data.empty:
            st.warning("セクターデータが不足しています")
            return
        
        # 選択されたセクターのデータをフィルタリング
        sector_filtered = sector_data[sector_data['sector'] == selected_sector]
        
        if sector_filtered.empty:
            st.warning(f"{selected_sector}セクターのデータがありません")
            return
        
        st.markdown(f"#### 🏢 {selected_sector}セクターの銘柄一覧")
        
        # 時価総額でソート
        sector_filtered = sector_filtered.sort_values('market_cap_billion', ascending=False)
        
        # 表示用のデータを準備
        display_data = sector_filtered[['ticker', 'company_name', 'industry', 'market_cap_billion', 'price_change', 'employees']].copy()
        display_data.columns = ['銘柄コード', '会社名', '業界', '時価総額(十億円)', '価格変動率(%)', '従業員数']
        display_data = display_data.round(2)
        
        # 最大表示数まで表示
        st.dataframe(display_data.head(max_companies), use_container_width=True)
    
    def display_data_quality_warning(self, sector_data: pd.DataFrame) -> None:
        """
        データ品質の警告を表示
        
        Args:
            sector_data: セクター情報のDataFrame
        """
        if sector_data is None or sector_data.empty:
            st.warning("⚠️ セクターデータが存在しません")
            return
        
        # データの基本情報
        st.success(f"✅ セクターデータが利用可能です")
        st.write(f"**分析対象銘柄数:** {len(sector_data)}銘柄")
        st.write(f"**セクター数:** {sector_data['sector'].nunique()}セクター")
        st.write(f"**業界数:** {sector_data['industry'].nunique()}業界")
        
        # データの完全性チェック
        missing_data = sector_data.isnull().sum()
        if missing_data.any():
            st.warning("⚠️ 一部のデータに欠損値があります")
            st.write("欠損値の詳細:")
            st.write(missing_data[missing_data > 0])
