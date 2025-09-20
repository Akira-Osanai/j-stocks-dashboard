"""
配当分析コンポーネント

配当データの可視化と分析機能を提供
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional, Dict, List
import numpy as np


class DividendAnalysis:
    """配当分析を表示するクラス"""
    
    @staticmethod
    def create_dividend_timeline_chart(
        df: pd.DataFrame,
        title: str = "配当履歴",
        height: int = 500
    ) -> go.Figure:
        """
        配当履歴のタイムライン表示
        
        Args:
            df: 配当データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if df is None or df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="配当データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # データを年でグループ化して集計
        df['year'] = df['date'].dt.year
        yearly_dividends = df.groupby('year')['dividend'].sum().reset_index()
        yearly_dividends = yearly_dividends.sort_values('year')
        
        # チャート作成
        fig = go.Figure()
        
        # 配当額の棒グラフ
        fig.add_trace(go.Bar(
            x=yearly_dividends['year'],
            y=yearly_dividends['dividend'],
            name='年間配当額',
            marker_color='#1f77b4',
            opacity=0.8
        ))
        
        # 配当トレンド（移動平均）
        if len(yearly_dividends) >= 3:
            # 3年移動平均を計算
            yearly_dividends['trend'] = yearly_dividends['dividend'].rolling(window=3, center=True).mean()
            
            fig.add_trace(go.Scatter(
                x=yearly_dividends['year'],
                y=yearly_dividends['trend'],
                mode='lines+markers',
                name='配当トレンド（3年移動平均）',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8)
            ))
        else:
            # データが少ない場合は単純な線グラフ
            fig.add_trace(go.Scatter(
                x=yearly_dividends['year'],
                y=yearly_dividends['dividend'],
                mode='lines+markers',
                name='配当トレンド',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="配当額 (円)",
            template="plotly_white",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_dividend_yield_chart(
        dividend_data: pd.DataFrame,
        stock_data: pd.DataFrame,
        title: str = "配当利回り推移",
        height: int = 500
    ) -> go.Figure:
        """
        配当利回りの推移を表示
        
        Args:
            dividend_data: 配当データのDataFrame
            stock_data: 株価データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if dividend_data is None or dividend_data.empty or stock_data is None or stock_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="配当または株価データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 年次配当額を計算
        dividend_data['year'] = dividend_data['date'].dt.year
        yearly_dividends = dividend_data.groupby('year')['dividend'].sum().reset_index()
        
        # 年次平均株価を計算
        stock_data['year'] = stock_data['Date'].dt.year
        yearly_prices = stock_data.groupby('year')['Close'].mean().reset_index()
        
        # データをマージ
        merged_data = pd.merge(yearly_dividends, yearly_prices, on='year', how='inner')
        merged_data['dividend_yield'] = (merged_data['dividend'] / merged_data['Close']) * 100
        merged_data = merged_data.sort_values('year')
        
        # チャート作成
        fig = go.Figure()
        
        # 配当利回りの線グラフ
        fig.add_trace(go.Scatter(
            x=merged_data['year'],
            y=merged_data['dividend_yield'],
            mode='lines+markers',
            name='配当利回り (%)',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="配当利回り (%)",
            template="plotly_white",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_dividend_growth_chart(
        df: pd.DataFrame,
        title: str = "配当成長率",
        height: int = 400
    ) -> go.Figure:
        """
        配当成長率の推移を表示
        
        Args:
            df: 配当データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if df is None or df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="配当データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 年次配当額を計算
        df['year'] = df['date'].dt.year
        yearly_dividends = df.groupby('year')['dividend'].sum().reset_index()
        yearly_dividends = yearly_dividends.sort_values('year')
        
        # 配当成長率を計算
        yearly_dividends['dividend_growth'] = yearly_dividends['dividend'].pct_change() * 100
        yearly_dividends = yearly_dividends.dropna()
        
        if yearly_dividends.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="配当成長率を計算するデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # チャート作成
        fig = go.Figure()
        
        # 配当成長率の棒グラフ
        colors = ['green' if x > 0 else 'red' for x in yearly_dividends['dividend_growth']]
        fig.add_trace(go.Bar(
            x=yearly_dividends['year'],
            y=yearly_dividends['dividend_growth'],
            name='年次配当成長率 (%)',
            marker_color=colors,
            opacity=0.8
        ))
        
        # 累積成長率の線グラフ
        yearly_dividends['cumulative_growth'] = ((yearly_dividends['dividend'] / yearly_dividends['dividend'].iloc[0]) - 1) * 100
        fig.add_trace(go.Scatter(
            x=yearly_dividends['year'],
            y=yearly_dividends['cumulative_growth'],
            mode='lines+markers',
            name='累積配当成長率 (%)',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        # ゼロライン
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        # 二軸の設定
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="年次配当成長率 (%)",
            yaxis2=dict(
                title="累積配当成長率 (%)",
                overlaying="y",
                side="right"
            ),
            template="plotly_white",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_dividend_consistency_chart(
        df: pd.DataFrame,
        title: str = "配当の一貫性",
        height: int = 400
    ) -> go.Figure:
        """
        配当の一貫性を表示
        
        Args:
            df: 配当データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if df is None or df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="配当データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 年次配当回数を計算
        df['year'] = df['date'].dt.year
        yearly_counts = df.groupby('year').size().reset_index(name='dividend_count')
        yearly_counts = yearly_counts.sort_values('year')
        
        # チャート作成
        fig = go.Figure()
        
        # 配当回数の棒グラフ
        fig.add_trace(go.Bar(
            x=yearly_counts['year'],
            y=yearly_counts['dividend_count'],
            name='年間配当回数',
            marker_color='#9467bd',
            opacity=0.8
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="配当回数",
            template="plotly_white",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def display_dividend_summary(
        dividend_analysis: pd.DataFrame,
        dividend_data: pd.DataFrame
    ) -> None:
        """
        配当サマリー情報を表示
        
        Args:
            dividend_analysis: 配当分析データのDataFrame
            dividend_data: 配当データのDataFrame
        """
        if dividend_analysis is None or dividend_analysis.empty:
            st.warning("配当分析データが不足しています")
            return
        
        analysis = dividend_analysis.iloc[0]
        
        # サマリー情報を表示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "配当利回り",
                f"{analysis.get('dividend_yield', 0):.2f}%",
                help="現在の配当利回り"
            )
        
        with col2:
            st.metric(
                "配当頻度",
                analysis.get('dividend_frequency', '不明'),
                help="配当の支払い頻度"
            )
        
        with col3:
            st.metric(
                "配当成長率",
                f"{analysis.get('dividend_growth_rate', 0):.2f}%",
                help="過去の配当成長率"
            )
        
        with col4:
            st.metric(
                "配当一貫性",
                f"{analysis.get('dividend_consistency', 0):.1f}%",
                help="配当の一貫性スコア"
            )
        
        # 詳細情報
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 配当統計")
            st.write(f"**総配当額:** ¥{analysis.get('total_dividends', 0):,.0f}")
            st.write(f"**平均配当額:** ¥{analysis.get('average_dividend', 0):,.2f}")
            st.write(f"**配当回数:** {analysis.get('dividend_count', 0)}回")
        
        with col2:
            st.markdown("#### 📅 配当履歴")
            if dividend_data is not None and not dividend_data.empty:
                latest_dividend = dividend_data['date'].max()
                st.write(f"**最新配当日:** {latest_dividend.strftime('%Y年%m月%d日')}")
                
                # 直近5回の配当
                recent_dividends = dividend_data.tail(5).sort_values('date', ascending=False)
                st.write("**直近5回の配当:**")
                for _, row in recent_dividends.iterrows():
                    st.write(f"- {row['date'].strftime('%Y/%m/%d')}: ¥{row['dividend']:,.2f}")
            else:
                st.write("配当履歴データがありません")
    
    @staticmethod
    def display_data_quality_warning(df: pd.DataFrame, data_type: str) -> None:
        """
        データ品質の警告を表示
        
        Args:
            df: データのDataFrame
            data_type: データの種類
        """
        if df is None or df.empty:
            st.warning(f"⚠️ {data_type}のデータが存在しません")
            return
        
        # データの基本情報
        st.success(f"✅ {data_type}のデータが利用可能です")
        st.write(f"**データ件数:** {len(df)}件")
        
        if 'date' in df.columns:
            date_range = f"{df['date'].min().strftime('%Y/%m/%d')} - {df['date'].max().strftime('%Y/%m/%d')}"
            st.write(f"**期間:** {date_range}")
