"""
日本株データローダー
CSVファイルから株価データを読み込むためのモジュール
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class StockDataLoader:
    """株価データを読み込むためのクラス"""
    
    def __init__(self, data_dir: str = "output"):
        """
        初期化
        
        Args:
            data_dir: データディレクトリのパス
        """
        self.data_dir = Path(data_dir)
        self._available_tickers = None
    
    def get_available_tickers(self) -> List[str]:
        """
        利用可能な銘柄コードのリストを取得
        
        Returns:
            銘柄コードのリスト
        """
        if self._available_tickers is None:
            ticker_dirs = [d.name for d in self.data_dir.iterdir() 
                          if d.is_dir() and d.name.isdigit()]
            self._available_tickers = sorted(ticker_dirs)
        return self._available_tickers
    
    def load_stock_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        指定された銘柄の株価データを読み込み
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            株価データのDataFrame、読み込みに失敗した場合はNone
        """
        try:
            file_path = self.data_dir / ticker / "stock_data" / "stock_data.csv"
            if not file_path.exists():
                return None
            
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            return df
        except Exception as e:
            print(f"Error loading stock data for {ticker}: {e}")
            return None
    
    def load_company_info(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        指定された銘柄の企業情報を読み込み
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            企業情報のDataFrame、読み込みに失敗した場合はNone
        """
        try:
            file_path = self.data_dir / ticker / "company_info" / "company_info.csv"
            if not file_path.exists():
                return None
            
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading company info for {ticker}: {e}")
            return None
    
    def load_technical_indicators(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        指定された銘柄のテクニカル指標を読み込み
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            テクニカル指標のDataFrame、読み込みに失敗した場合はNone
        """
        try:
            file_path = self.data_dir / ticker / "technical_data" / "technical_indicators.csv"
            if not file_path.exists():
                return None
            
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            return df
        except Exception as e:
            print(f"Error loading technical indicators for {ticker}: {e}")
            return None
    
    def load_financial_ratios(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        指定された銘柄の財務比率を読み込み
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            財務比率のDataFrame、読み込みに失敗した場合はNone
        """
        try:
            file_path = self.data_dir / ticker / "financial_data" / "financial_ratios.csv"
            if not file_path.exists():
                return None
            
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading financial ratios for {ticker}: {e}")
            return None
    
    def get_ticker_name(self, ticker: str) -> str:
        """
        銘柄コードから銘柄名を取得
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            銘柄名
        """
        company_info = self.load_company_info(ticker)
        if company_info is not None and not company_info.empty:
            return company_info.iloc[0].get('company_name', f'銘柄{ticker}')
        return f'銘柄{ticker}'
    
    def check_data_completeness(self, ticker: str) -> Dict[str, bool]:
        """
        銘柄のデータ完全性をチェック
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            各データタイプの存在フラグ
        """
        completeness = {
            'stock_data': False,
            'company_info': False,
            'technical_data': False,
            'financial_data': False
        }
        
        # 株価データのチェック
        stock_data = self.load_stock_data(ticker)
        if stock_data is not None and not stock_data.empty and len(stock_data) >= 2:
            completeness['stock_data'] = True
        
        # 企業情報のチェック
        company_info = self.load_company_info(ticker)
        if company_info is not None and not company_info.empty:
            completeness['company_info'] = True
        
        # テクニカル指標のチェック
        technical_data = self.load_technical_indicators(ticker)
        if technical_data is not None and not technical_data.empty:
            completeness['technical_data'] = True
        
        # 財務データのチェック
        financial_data = self.load_financial_ratios(ticker)
        if financial_data is not None and not financial_data.empty:
            completeness['financial_data'] = True
        
        return completeness
    
    def is_data_sufficient(self, ticker: str) -> bool:
        """
        銘柄のデータが十分かどうかを判定
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            データが十分な場合はTrue
        """
        completeness = self.check_data_completeness(ticker)
        # 最低限、株価データと企業情報があれば十分とする
        return completeness['stock_data'] and completeness['company_info']
    
    def get_ticker_display_name(self, ticker: str) -> str:
        """
        表示用の銘柄名を取得（データ不足の場合は記号を付加）
        
        Args:
            ticker: 銘柄コード
            
        Returns:
            表示用の銘柄名
        """
        company_name = self.get_ticker_name(ticker)
        if self.is_data_sufficient(ticker):
            return company_name
        else:
            return f"{company_name} ⚠️"

    def search_tickers(self, query: str) -> List[Tuple[str, str]]:
        """
        銘柄名またはコードで検索
        
        Args:
            query: 検索クエリ
            
        Returns:
            (銘柄コード, 表示用銘柄名)のタプルのリスト
        """
        results = []
        query_lower = query.lower()
        
        for ticker in self.get_available_tickers():
            try:
                company_info = self.load_company_info(ticker)
                if company_info is not None and not company_info.empty:
                    company_name = company_info.iloc[0].get('company_name', '')
                    if (query_lower in ticker.lower() or 
                        query_lower in company_name.lower()):
                        display_name = self.get_ticker_display_name(ticker)
                        results.append((ticker, display_name))
            except:
                continue
        
        return results
