"""
財務分析コンポーネント
損益計算書、貸借対照表、キャッシュフロー計算書の可視化
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any
import streamlit as st


class FinancialAnalysis:
    """財務分析を表示するクラス"""
    
    @staticmethod
    def create_income_statement_chart(
        df: pd.DataFrame,
        title: str = "損益計算書",
        height: int = 600
    ) -> go.Figure:
        """
        損益計算書の可視化
        
        Args:
            df: 損益計算書のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        # 主要な財務指標を選択
        key_metrics = [
            'Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income'
        ]
        
        # データが存在する指標のみを抽出
        available_metrics = [col for col in key_metrics if col in df.columns]
        
        if not available_metrics:
            fig = go.Figure()
            fig.add_annotation(
                text="データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # データを転置して年次データを整理
        # 各年（列）を年として扱い、指標を行として扱う
        years = []
        for col in df.columns:
            if col not in ['ticker'] and not pd.isna(df[col].iloc[0]):
                years.append(col)
        
        if not years:
            fig = go.Figure()
            fig.add_annotation(
                text="年次データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # チャート作成
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        for i, metric in enumerate(available_metrics):
            values = []
            valid_years = []
            
            for year in years:
                value = df[metric].iloc[0] if not pd.isna(df[metric].iloc[0]) else None
                if value is not None and not pd.isna(value):
                    values.append(value / 1e9)  # 十億円単位に変換
                    valid_years.append(year)
            
            if values:
                fig.add_trace(go.Scatter(
                    x=valid_years,
                    y=values,
                    mode='lines+markers',
                    name=metric,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="金額 (十億円)",
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
    def create_balance_sheet_chart(
        df: pd.DataFrame,
        title: str = "貸借対照表",
        height: int = 600
    ) -> go.Figure:
        """
        貸借対照表の可視化
        
        Args:
            df: 貸借対照表のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        # 主要な資産・負債・資本項目を選択
        key_metrics = [
            'Total Assets', 'Total Liabilities', 'Stockholders Equity',
            'Cash And Cash Equivalents', 'Total Debt'
        ]
        
        # データが存在する指標のみを抽出
        available_metrics = [col for col in key_metrics if col in df.columns]
        
        if not available_metrics:
            fig = go.Figure()
            fig.add_annotation(
                text="データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 年次データの準備
        years = []
        for col in df.columns:
            if col not in ['ticker'] and not pd.isna(df[col].iloc[0]):
                years.append(col)
        
        if not years:
            fig = go.Figure()
            fig.add_annotation(
                text="年次データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # チャート作成
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        for i, metric in enumerate(available_metrics):
            values = []
            valid_years = []
            
            for year in years:
                value = df[metric].iloc[0] if not pd.isna(df[metric].iloc[0]) else None
                if value is not None and not pd.isna(value):
                    values.append(value / 1e9)  # 十億円単位に変換
                    valid_years.append(year)
            
            if values:
                fig.add_trace(go.Scatter(
                    x=valid_years,
                    y=values,
                    mode='lines+markers',
                    name=metric,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="金額 (十億円)",
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
    def create_cashflow_chart(
        df: pd.DataFrame,
        title: str = "キャッシュフロー計算書",
        height: int = 600
    ) -> go.Figure:
        """
        キャッシュフロー計算書の可視化
        
        Args:
            df: キャッシュフロー計算書のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        # 主要なキャッシュフロー項目を選択
        key_metrics = [
            'Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow',
            'Free Cash Flow'
        ]
        
        # データが存在する指標のみを抽出
        available_metrics = [col for col in key_metrics if col in df.columns]
        
        if not available_metrics:
            fig = go.Figure()
            fig.add_annotation(
                text="データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 年次データの準備
        years = []
        for col in df.columns:
            if col not in ['ticker'] and not pd.isna(df[col].iloc[0]):
                years.append(col)
        
        if not years:
            fig = go.Figure()
            fig.add_annotation(
                text="年次データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # チャート作成
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        for i, metric in enumerate(available_metrics):
            values = []
            valid_years = []
            
            for year in years:
                value = df[metric].iloc[0] if not pd.isna(df[metric].iloc[0]) else None
                if value is not None and not pd.isna(value):
                    values.append(value / 1e9)  # 十億円単位に変換
                    valid_years.append(year)
            
            if values:
                fig.add_trace(go.Scatter(
                    x=valid_years,
                    y=values,
                    mode='lines+markers',
                    name=metric,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="年度",
            yaxis_title="金額 (十億円)",
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
    def create_financial_ratios_chart(
        df: pd.DataFrame,
        title: str = "財務比率",
        height: int = 400
    ) -> go.Figure:
        """
        財務比率の可視化
        
        Args:
            df: 財務比率のDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if df is None or df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="財務比率データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 主要な財務比率を選択
        key_ratios = [
            'pe_ratio', 'price_to_book', 'gross_margin', 'operating_margin',
            'profit_margin', 'return_on_assets', 'return_on_equity',
            'current_ratio', 'debt_to_equity'
        ]
        
        # データが存在する比率のみを抽出
        available_ratios = df[df['ratio'].isin(key_ratios)]
        
        if available_ratios.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="利用可能な財務比率データがありません",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # バーチャートを作成
        fig = go.Figure()
        
        ratios = available_ratios['ratio'].tolist()
        values = available_ratios['value'].tolist()
        
        # NaNでない値のみをプロット
        valid_ratios = []
        valid_values = []
        for ratio, value in zip(ratios, values):
            if not pd.isna(value) and value != 0:
                valid_ratios.append(ratio)
                valid_values.append(value)
        
        if not valid_values:
            fig.add_annotation(
                text="すべての財務比率データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
        else:
            fig.add_trace(go.Bar(
                x=valid_ratios,
                y=valid_values,
                name="財務比率",
                marker_color='#1f77b4'
            ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="財務比率",
            yaxis_title="値",
            template="plotly_white",
            xaxis_tickangle=-45
        )
        
        return fig
    
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
        
        # NaNの割合を計算
        nan_count = df.isnull().sum().sum()
        total_count = df.size
        nan_percentage = (nan_count / total_count) * 100
        
        if nan_percentage > 50:
            st.error(f"⚠️ {data_type}のデータの{nan_percentage:.1f}%が不足しています")
        elif nan_percentage > 20:
            st.warning(f"⚠️ {data_type}のデータの{nan_percentage:.1f}%が不足しています")
        else:
            st.success(f"✅ {data_type}のデータ品質は良好です（不足率: {nan_percentage:.1f}%）")
