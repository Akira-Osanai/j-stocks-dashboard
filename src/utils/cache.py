"""
キャッシュユーティリティ
パフォーマンス最適化のためのキャッシュ機能を提供
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import time
import hashlib
import json

class DataCache:
    """データキャッシュ管理クラス"""
    
    def __init__(self, cache_ttl: int = 3600):
        """
        キャッシュマネージャーを初期化
        
        Args:
            cache_ttl: キャッシュの有効期限（秒）
        """
        self.cache_ttl = cache_ttl
        self._init_cache()
    
    def _init_cache(self):
        """キャッシュを初期化"""
        if 'data_cache' not in st.session_state:
            st.session_state.data_cache = {}
        if 'cache_timestamps' not in st.session_state:
            st.session_state.cache_timestamps = {}
    
    def _generate_cache_key(self, ticker: str, data_type: str, **kwargs) -> str:
        """
        キャッシュキーを生成
        
        Args:
            ticker: 銘柄コード
            data_type: データタイプ
            **kwargs: その他のパラメータ
            
        Returns:
            キャッシュキー
        """
        key_data = {
            'ticker': ticker,
            'data_type': data_type,
            **kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """
        キャッシュが有効かチェック
        
        Args:
            cache_key: キャッシュキー
            
        Returns:
            キャッシュが有効かどうか
        """
        if cache_key not in st.session_state.cache_timestamps:
            return False
        
        cache_time = st.session_state.cache_timestamps[cache_key]
        current_time = time.time()
        
        return (current_time - cache_time) < self.cache_ttl
    
    def get(self, ticker: str, data_type: str, **kwargs) -> Optional[Any]:
        """
        キャッシュからデータを取得
        
        Args:
            ticker: 銘柄コード
            data_type: データタイプ
            **kwargs: その他のパラメータ
            
        Returns:
            キャッシュされたデータ（存在しない場合はNone）
        """
        cache_key = self._generate_cache_key(ticker, data_type, **kwargs)
        
        if not self._is_cache_valid(cache_key):
            return None
        
        return st.session_state.data_cache.get(cache_key)
    
    def set(self, ticker: str, data_type: str, data: Any, **kwargs) -> None:
        """
        データをキャッシュに保存
        
        Args:
            ticker: 銘柄コード
            data_type: データタイプ
            data: 保存するデータ
            **kwargs: その他のパラメータ
        """
        cache_key = self._generate_cache_key(ticker, data_type, **kwargs)
        
        st.session_state.data_cache[cache_key] = data
        st.session_state.cache_timestamps[cache_key] = time.time()
    
    def clear(self, ticker: Optional[str] = None, data_type: Optional[str] = None) -> None:
        """
        キャッシュをクリア
        
        Args:
            ticker: 特定の銘柄のキャッシュをクリア（Noneの場合は全銘柄）
            data_type: 特定のデータタイプのキャッシュをクリア（Noneの場合は全データタイプ）
        """
        if ticker is None and data_type is None:
            # 全キャッシュをクリア
            st.session_state.data_cache = {}
            st.session_state.cache_timestamps = {}
        else:
            # 特定の条件に一致するキャッシュをクリア
            keys_to_remove = []
            for cache_key in st.session_state.data_cache.keys():
                # キャッシュキーから元のデータを復元（簡易版）
                if ticker and ticker not in cache_key:
                    continue
                if data_type and data_type not in cache_key:
                    continue
                keys_to_remove.append(cache_key)
            
            for key in keys_to_remove:
                st.session_state.data_cache.pop(key, None)
                st.session_state.cache_timestamps.pop(key, None)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        キャッシュの統計情報を取得
        
        Returns:
            キャッシュの統計情報
        """
        total_cached = len(st.session_state.data_cache)
        valid_cached = sum(1 for key in st.session_state.data_cache.keys() 
                          if self._is_cache_valid(key))
        
        return {
            'total_cached': total_cached,
            'valid_cached': valid_cached,
            'expired_cached': total_cached - valid_cached,
            'cache_ttl': self.cache_ttl
        }

# グローバルキャッシュインスタンス
@st.cache_resource
def get_data_cache() -> DataCache:
    """データキャッシュのシングルトンインスタンスを取得"""
    return DataCache(cache_ttl=3600)  # 1時間のキャッシュ

class LazyDataLoader:
    """遅延読み込みデータローダー"""
    
    def __init__(self, data_loader, cache: DataCache):
        """
        遅延読み込みローダーを初期化
        
        Args:
            data_loader: 元のデータローダー
            cache: データキャッシュ
        """
        self.data_loader = data_loader
        self.cache = cache
    
    def load_stock_data(self, ticker: str, **kwargs) -> Optional[pd.DataFrame]:
        """株価データを遅延読み込み"""
        cached_data = self.cache.get(ticker, "stock_data", **kwargs)
        
        if cached_data is not None:
            return cached_data
        
        data = self.data_loader.load_stock_data(ticker)
        if data is not None:
            self.cache.set(ticker, "stock_data", data, **kwargs)
        
        return data
    
    def load_company_info(self, ticker: str, **kwargs) -> Optional[pd.DataFrame]:
        """企業情報を遅延読み込み"""
        cached_data = self.cache.get(ticker, "company_info", **kwargs)
        
        if cached_data is not None:
            return cached_data
        
        data = self.data_loader.load_company_info(ticker)
        if data is not None:
            self.cache.set(ticker, "company_info", data, **kwargs)
        
        return data
    
    def load_financial_data(self, ticker: str, data_type: str, **kwargs) -> Optional[pd.DataFrame]:
        """財務データを遅延読み込み"""
        cached_data = self.cache.get(ticker, f"financial_{data_type}", **kwargs)
        
        if cached_data is not None:
            return cached_data
        
        # データタイプに応じて適切なメソッドを呼び出し
        if data_type == "income_statement":
            data = self.data_loader.load_income_statement(ticker)
        elif data_type == "balance_sheet":
            data = self.data_loader.load_balance_sheet(ticker)
        elif data_type == "cashflow":
            data = self.data_loader.load_cashflow(ticker)
        elif data_type == "financial_ratios":
            data = self.data_loader.load_financial_ratios(ticker)
        else:
            return None
        
        if data is not None:
            self.cache.set(ticker, f"financial_{data_type}", data, **kwargs)
        
        return data
    
    def load_dividend_data(self, ticker: str, **kwargs) -> Optional[pd.DataFrame]:
        """配当データを遅延読み込み"""
        cached_data = self.cache.get(ticker, "dividend_data", **kwargs)
        
        if cached_data is not None:
            return cached_data
        
        data = self.data_loader.load_dividend_data(ticker)
        if data is not None:
            self.cache.set(ticker, "dividend_data", data, **kwargs)
        
        return data
    
    def load_news_data(self, ticker: str, **kwargs) -> Optional[pd.DataFrame]:
        """ニュースデータを遅延読み込み"""
        cached_data = self.cache.get(ticker, "news_data", **kwargs)
        
        if cached_data is not None:
            return cached_data
        
        data = self.data_loader.load_news_data(ticker)
        if data is not None:
            self.cache.set(ticker, "news_data", data, **kwargs)
        
        return data

class OptimizedSectorLoader:
    """最適化されたセクターローダー"""
    
    def __init__(self, data_loader, cache: DataCache):
        """
        最適化されたセクターローダーを初期化
        
        Args:
            data_loader: 元のデータローダー
            cache: データキャッシュ
        """
        self.data_loader = data_loader
        self.cache = cache
        self._sector_data_cache = None
        self._last_sector_load_time = 0
        self._sector_cache_ttl = 1800  # 30分
    
    def load_sector_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        セクターデータを最適化して読み込み
        
        Args:
            force_reload: 強制再読み込み
            
        Returns:
            セクターデータのDataFrame
        """
        current_time = time.time()
        
        # キャッシュが有効で、強制再読み込みでない場合はキャッシュを返す
        if (not force_reload and 
            self._sector_data_cache is not None and 
            (current_time - self._last_sector_load_time) < self._sector_cache_ttl):
            return self._sector_data_cache
        
        # セクターデータを読み込み
        sector_data = []
        available_tickers = self.data_loader.get_available_tickers()
        
        # バッチ処理でデータを読み込み
        batch_size = 50
        for i in range(0, len(available_tickers), batch_size):
            batch_tickers = available_tickers[i:i + batch_size]
            
            for ticker in batch_tickers:
                try:
                    # 企業情報のみを読み込み（株価データは必要に応じて）
                    company_info_path = self.data_loader.data_dir / ticker / "company_info" / "company_info.csv"
                    if company_info_path.exists():
                        df = pd.read_csv(company_info_path)
                        if not df.empty:
                            # 株価データは必要に応じてのみ読み込み
                            latest_price = 0
                            price_change = 0
                            
                            # 株価データのキャッシュをチェック
                            stock_data = self.cache.get(ticker, "stock_data")
                            if stock_data is None:
                                stock_data = self.data_loader.load_stock_data(ticker)
                                if stock_data is not None:
                                    self.cache.set(ticker, "stock_data", stock_data)
                            
                            if stock_data is not None and not stock_data.empty:
                                close_column = 'Close' if 'Close' in stock_data.columns else 'close'
                                if close_column in stock_data.columns:
                                    latest_price = stock_data[close_column].iloc[-1]
                                    if len(stock_data) >= 2:
                                        price_change = ((stock_data[close_column].iloc[-1] - stock_data[close_column].iloc[-2]) / stock_data[close_column].iloc[-2]) * 100
                            
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
        
        self._sector_data_cache = pd.DataFrame(sector_data)
        self._last_sector_load_time = current_time
        
        return self._sector_data_cache
