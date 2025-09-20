"""
ニュース・センチメント分析コンポーネント

ニュースデータの感情分析と可視化機能を提供
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Optional, Dict, List
import numpy as np
import json
from datetime import datetime, timedelta


class NewsSentimentAnalysis:
    """ニュース・センチメント分析を表示するクラス"""
    
    @staticmethod
    def create_sentiment_overview_chart(
        news_analysis: pd.DataFrame,
        title: str = "センチメント概要",
        height: int = 400
    ) -> go.Figure:
        """
        センチメント概要の円グラフを作成
        
        Args:
            news_analysis: ニュース分析データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if news_analysis is None or news_analysis.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="ニュース分析データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        analysis = news_analysis.iloc[0]
        
        # センチメントデータを準備
        labels = ['ポジティブ', 'ニュートラル', 'ネガティブ']
        values = [
            analysis.get('positive_news', 0),
            analysis.get('neutral_news', 0),
            analysis.get('negative_news', 0)
        ]
        colors = ['#2ca02c', '#ff7f0e', '#d62728']
        
        # 円グラフを作成
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors,
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
    
    @staticmethod
    def create_sentiment_timeline_chart(
        news_data: pd.DataFrame,
        title: str = "センチメント推移",
        height: int = 500
    ) -> go.Figure:
        """
        センチメントの時系列推移を表示
        
        Args:
            news_data: ニュースデータのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if news_data is None or news_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="ニュースデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # ニュースデータを処理
        news_list = []
        for _, row in news_data.iterrows():
            if pd.notna(row['parsed_content']):
                content = row['parsed_content']
                news_list.append({
                    'date': pd.to_datetime(content.get('pubDate', '')),
                    'title': content.get('title', ''),
                    'summary': content.get('summary', ''),
                    'provider': content.get('provider', {}).get('displayName', ''),
                    'sentiment': 'neutral'  # デフォルトはニュートラル
                })
        
        if not news_list:
            fig = go.Figure()
            fig.add_annotation(
                text="有効なニュースデータがありません",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # 日付でソート
        news_df = pd.DataFrame(news_list)
        news_df = news_df.sort_values('date')
        
        # 日付ごとにグループ化してニュース数をカウント
        news_df['date_only'] = news_df['date'].dt.date
        daily_news = news_df.groupby('date_only').size().reset_index(name='news_count')
        
        # チャート作成
        fig = go.Figure()
        
        # ニュース数の棒グラフ
        fig.add_trace(go.Bar(
            x=daily_news['date_only'],
            y=daily_news['news_count'],
            name='ニュース数',
            marker_color='#1f77b4',
            opacity=0.8
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="日付",
            yaxis_title="ニュース数",
            template="plotly_white",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_news_source_chart(
        news_data: pd.DataFrame,
        title: str = "ニュースソース分析",
        height: int = 400
    ) -> go.Figure:
        """
        ニュースソースの分析チャートを作成
        
        Args:
            news_data: ニュースデータのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if news_data is None or news_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="ニュースデータが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # ニュースソースを抽出
        sources = []
        for _, row in news_data.iterrows():
            if pd.notna(row['parsed_content']):
                content = row['parsed_content']
                provider = content.get('provider', {})
                source_name = provider.get('displayName', 'Unknown')
                sources.append(source_name)
        
        if not sources:
            fig = go.Figure()
            fig.add_annotation(
                text="ニュースソースデータがありません",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        # ソース別のニュース数をカウント
        source_counts = pd.Series(sources).value_counts()
        
        # チャート作成
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=source_counts.index,
            y=source_counts.values,
            name='ニュース数',
            marker_color='#9467bd',
            opacity=0.8
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            xaxis_title="ニュースソース",
            yaxis_title="ニュース数",
            template="plotly_white",
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_sentiment_score_chart(
        news_analysis: pd.DataFrame,
        title: str = "センチメントスコア",
        height: int = 300
    ) -> go.Figure:
        """
        センチメントスコアの表示
        
        Args:
            news_analysis: ニュース分析データのDataFrame
            title: チャートのタイトル
            height: チャートの高さ
            
        Returns:
            PlotlyのFigureオブジェクト
        """
        if news_analysis is None or news_analysis.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="ニュース分析データが不足しています",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(title=title, height=height)
            return fig
        
        analysis = news_analysis.iloc[0]
        sentiment_score = analysis.get('sentiment_score', 0.0)
        confidence = analysis.get('confidence', 0.0)
        
        # センチメントスコアの色を決定
        if sentiment_score > 0.1:
            color = '#2ca02c'  # 緑（ポジティブ）
        elif sentiment_score < -0.1:
            color = '#d62728'  # 赤（ネガティブ）
        else:
            color = '#ff7f0e'  # オレンジ（ニュートラル）
        
        # ゲージチャートを作成
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = sentiment_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "センチメントスコア"},
            delta = {'reference': 0},
            gauge = {
                'axis': {'range': [-1, 1]},
                'bar': {'color': color},
                'steps': [
                    {'range': [-1, -0.1], 'color': "lightgray"},
                    {'range': [-0.1, 0.1], 'color': "gray"},
                    {'range': [0.1, 1], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0
                }
            }
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            font={'color': "darkblue", 'family': "Arial"}
        )
        
        return fig
    
    @staticmethod
    def display_news_summary(
        news_analysis: pd.DataFrame,
        news_data: pd.DataFrame
    ) -> None:
        """
        ニュースサマリー情報を表示
        
        Args:
            news_analysis: ニュース分析データのDataFrame
            news_data: ニュースデータのDataFrame
        """
        if news_analysis is None or news_analysis.empty:
            st.warning("ニュース分析データが不足しています")
            return
        
        analysis = news_analysis.iloc[0]
        
        # サマリー情報を表示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "総ニュース数",
                f"{analysis.get('total_news', 0)}件",
                help="収集されたニュースの総数"
            )
        
        with col2:
            st.metric(
                "ニュース頻度",
                analysis.get('news_frequency', '不明'),
                help="ニュースの更新頻度"
            )
        
        with col3:
            sentiment_score = analysis.get('sentiment_score', 0.0)
            sentiment_label = "ポジティブ" if sentiment_score > 0.1 else "ネガティブ" if sentiment_score < -0.1 else "ニュートラル"
            st.metric(
                "全体的なセンチメント",
                sentiment_label,
                f"スコア: {sentiment_score:.2f}"
            )
        
        with col4:
            st.metric(
                "信頼度",
                f"{analysis.get('confidence', 0.0):.1f}%",
                help="センチメント分析の信頼度"
            )
        
        # 詳細情報
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 センチメント分布")
            st.write(f"**ポジティブ:** {analysis.get('positive_news', 0)}件")
            st.write(f"**ニュートラル:** {analysis.get('neutral_news', 0)}件")
            st.write(f"**ネガティブ:** {analysis.get('negative_news', 0)}件")
            st.write(f"**ニュース多様性:** {analysis.get('news_diversity', 0.0):.2f}")
        
        with col2:
            st.markdown("#### 📅 最近のニュース")
            if news_data is not None and not news_data.empty:
                # 最新のニュースを表示
                recent_news = news_data.head(3)
                for _, row in recent_news.iterrows():
                    if pd.notna(row['parsed_content']):
                        content = row['parsed_content']
                        title = content.get('title', 'No Title')
                        pub_date = content.get('pubDate', '')
                        if pub_date:
                            try:
                                pub_date = pd.to_datetime(pub_date).strftime('%Y/%m/%d')
                            except:
                                pub_date = pub_date
                        st.write(f"**{pub_date}:** {title[:50]}...")
            else:
                st.write("最近のニュースデータがありません")
    
    @staticmethod
    def display_news_list(
        news_data: pd.DataFrame,
        max_news: int = 10
    ) -> None:
        """
        ニュース一覧を表示
        
        Args:
            news_data: ニュースデータのDataFrame
            max_news: 表示する最大ニュース数
        """
        if news_data is None or news_data.empty:
            st.warning("ニュースデータが不足しています")
            return
        
        st.markdown("#### 📰 ニュース一覧")
        
        # ニュースを日付順でソート
        news_list = []
        for _, row in news_data.iterrows():
            if pd.notna(row['parsed_content']):
                content = row['parsed_content']
                news_list.append({
                    'date': content.get('pubDate', ''),
                    'title': content.get('title', ''),
                    'summary': content.get('summary', ''),
                    'provider': content.get('provider', {}).get('displayName', ''),
                    'url': content.get('canonicalUrl', {}).get('url', '')
                })
        
        if not news_list:
            st.write("表示可能なニュースがありません")
            return
        
        # 日付でソート
        news_df = pd.DataFrame(news_list)
        news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce')
        news_df = news_df.sort_values('date', ascending=False)
        
        # 最大表示数まで表示
        for i, (_, news) in enumerate(news_df.head(max_news).iterrows()):
            with st.expander(f"📰 {news['title'][:60]}..."):
                st.write(f"**日付:** {news['date'].strftime('%Y年%m月%d日') if pd.notna(news['date']) else '不明'}")
                st.write(f"**ソース:** {news['provider']}")
                st.write(f"**要約:** {news['summary'][:200]}...")
                if news['url']:
                    st.write(f"**リンク:** [記事を読む]({news['url']})")
    
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
        
        if 'parsed_content' in df.columns:
            # 有効なニュース数をカウント
            valid_news = df['parsed_content'].apply(lambda x: len(x) > 0 if isinstance(x, dict) else False).sum()
            st.write(f"**有効なニュース数:** {valid_news}件")
