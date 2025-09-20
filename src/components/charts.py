"""
株価チャートコンポーネント
Plotlyを使用したインタラクティブな株価チャート
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Any
import streamlit as st


class StockChart:
    """株価チャートを表示するクラス"""
    
    @staticmethod
    def create_candlestick_chart(
        df: pd.DataFrame,
        title: str = "株価チャート",
        height: int = 600,
        show_volume: bool = True
    ) -> go.Figure:
        """
        ローソク足チャートを作成
        
        Args:
            df: 株価データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            show_volume: 出来高を表示するかどうか
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if show_volume:
            # 出来高付きのローソク足チャート
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(title, '出来高'),
                row_heights=[0.7, 0.3]
            )
            
            # ローソク足
            fig.add_trace(
                go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="株価",
                    increasing_line_color='#26a69a',
                    decreasing_line_color='#ef5350'
                ),
                row=1, col=1
            )
            
            # 出来高
            colors = ['#26a69a' if close >= open else '#ef5350' 
                     for close, open in zip(df['Close'], df['Open'])]
            
            fig.add_trace(
                go.Bar(
                    x=df['Date'],
                    y=df['Volume'],
                    name="出来高",
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )
        else:
            # 出来高なしのローソク足チャート
            fig = go.Figure()
            fig.add_trace(
                go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="株価",
                    increasing_line_color='#26a69a',
                    decreasing_line_color='#ef5350'
                )
            )
        
        # レイアウト設定
        fig.update_layout(
            title=title,
            height=height,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            template="plotly_white",
            hovermode='x unified'
        )
        
        # 軸ラベル設定
        if show_volume:
            fig.update_xaxes(title_text="日付", row=2, col=1)
            fig.update_yaxes(title_text="株価 (円)", row=1, col=1)
            fig.update_yaxes(title_text="出来高", row=2, col=1)
        else:
            fig.update_xaxes(title_text="日付")
            fig.update_yaxes(title_text="株価 (円)")
        
        return fig
    
    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        title: str = "株価推移",
        height: int = 400,
        columns: List[str] = None
    ) -> go.Figure:
        """
        線グラフを作成
        
        Args:
            df: 株価データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            columns: 表示する列のリスト（デフォルトは['Close']）
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if columns is None:
            columns = ['Close']
        
        fig = go.Figure()
        
        for col in columns:
            if col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df['Date'],
                        y=df[col],
                        mode='lines',
                        name=col,
                        line=dict(width=2)
                    )
                )
        
        fig.update_layout(
            title=title,
            height=height,
            template="plotly_white",
            hovermode='x unified',
            xaxis_title="日付",
            yaxis_title="価格 (円)"
        )
        
        return fig
    
    @staticmethod
    def create_technical_indicators_chart(
        df: pd.DataFrame,
        title: str = "テクニカル指標",
        height: int = 600
    ) -> go.Figure:
        """
        テクニカル指標チャートを作成
        
        Args:
            df: テクニカル指標データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=("株価と移動平均", "RSI", "MACD"),
            row_heights=[0.5, 0.25, 0.25]
        )
        
        # 株価と移動平均
        if 'Close' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['Close'], name="終値", line=dict(color='blue')),
                row=1, col=1
            )
        
        # 移動平均線
        for ma in ['SMA_20', 'SMA_50', 'SMA_200']:
            if ma in df.columns:
                fig.add_trace(
                    go.Scatter(x=df['Date'], y=df[ma], name=ma, line=dict(dash='dash')),
                    row=1, col=1
                )
        
        # RSI
        if 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['RSI'], name="RSI", line=dict(color='purple')),
                row=2, col=1
            )
            # RSIの70と30のライン
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'MACD' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['MACD'], name="MACD", line=dict(color='blue')),
                row=3, col=1
            )
        if 'MACD_Signal' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['Date'], y=df['MACD_Signal'], name="MACD Signal", line=dict(color='red')),
                row=3, col=1
            )
        if 'MACD_Histogram' in df.columns:
            fig.add_trace(
                go.Bar(x=df['Date'], y=df['MACD_Histogram'], name="MACD Histogram", opacity=0.6),
                row=3, col=1
            )
        
        fig.update_layout(
            title=title,
            height=height,
            template="plotly_white",
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_volume_chart(
        df: pd.DataFrame,
        title: str = "出来高チャート",
        height: int = 400
    ) -> go.Figure:
        """
        出来高チャートを作成
        
        Args:
            df: 株価データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        colors = ['#26a69a' if close >= open else '#ef5350' 
                 for close, open in zip(df['Close'], df['Open'])]
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name="出来高",
                marker_color=colors,
                opacity=0.7
            )
        )
        
        fig.update_layout(
            title=title,
            height=height,
            template="plotly_white",
            xaxis_title="日付",
            yaxis_title="出来高"
        )
        
        return fig
