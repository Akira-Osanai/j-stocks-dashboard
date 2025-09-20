"""
パフォーマンスベンチマークスクリプト
最適化前後のパフォーマンスを比較
"""

import time
import sys
from pathlib import Path
import pandas as pd

# パスを追加
sys.path.append(str(Path(__file__).parent / "src"))

from data.loader import StockDataLoader
from utils.cache import get_data_cache, LazyDataLoader, OptimizedSectorLoader

def benchmark_original_loader():
    """元のデータローダーのベンチマーク"""
    print("🔍 元のデータローダーのベンチマークを実行中...")
    
    data_loader = StockDataLoader()
    available_tickers = data_loader.get_available_tickers()[:10]  # 最初の10銘柄でテスト
    
    results = {}
    
    # 株価データ読み込み
    start_time = time.time()
    for ticker in available_tickers:
        data_loader.load_stock_data(ticker)
    results['stock_data'] = time.time() - start_time
    
    # 企業情報読み込み
    start_time = time.time()
    for ticker in available_tickers:
        data_loader.load_company_info(ticker)
    results['company_info'] = time.time() - start_time
    
    # 財務データ読み込み
    start_time = time.time()
    for ticker in available_tickers:
        data_loader.load_income_statement(ticker)
        data_loader.load_balance_sheet(ticker)
        data_loader.load_cashflow(ticker)
        data_loader.load_financial_ratios(ticker)
    results['financial_data'] = time.time() - start_time
    
    # セクターデータ読み込み
    start_time = time.time()
    from components.sector_analysis import SectorAnalysis
    sector_analyzer = SectorAnalysis(data_loader.data_dir)
    sector_analyzer.load_sector_data()
    results['sector_data'] = time.time() - start_time
    
    return results

def benchmark_optimized_loader():
    """最適化されたデータローダーのベンチマーク"""
    print("⚡ 最適化されたデータローダーのベンチマークを実行中...")
    
    data_loader = StockDataLoader()
    cache = get_data_cache()
    lazy_loader = LazyDataLoader(data_loader, cache)
    sector_loader = OptimizedSectorLoader(data_loader, cache)
    
    available_tickers = data_loader.get_available_tickers()[:10]  # 最初の10銘柄でテスト
    
    results = {}
    
    # 株価データ読み込み（1回目）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_stock_data(ticker)
    results['stock_data_first'] = time.time() - start_time
    
    # 株価データ読み込み（2回目 - キャッシュから）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_stock_data(ticker)
    results['stock_data_cached'] = time.time() - start_time
    
    # 企業情報読み込み（1回目）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_company_info(ticker)
    results['company_info_first'] = time.time() - start_time
    
    # 企業情報読み込み（2回目 - キャッシュから）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_company_info(ticker)
    results['company_info_cached'] = time.time() - start_time
    
    # 財務データ読み込み（1回目）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_financial_data(ticker, "income_statement")
        lazy_loader.load_financial_data(ticker, "balance_sheet")
        lazy_loader.load_financial_data(ticker, "cashflow")
        lazy_loader.load_financial_data(ticker, "financial_ratios")
    results['financial_data_first'] = time.time() - start_time
    
    # 財務データ読み込み（2回目 - キャッシュから）
    start_time = time.time()
    for ticker in available_tickers:
        lazy_loader.load_financial_data(ticker, "income_statement")
        lazy_loader.load_financial_data(ticker, "balance_sheet")
        lazy_loader.load_financial_data(ticker, "cashflow")
        lazy_loader.load_financial_data(ticker, "financial_ratios")
    results['financial_data_cached'] = time.time() - start_time
    
    # セクターデータ読み込み（1回目）
    start_time = time.time()
    sector_loader.load_sector_data()
    results['sector_data_first'] = time.time() - start_time
    
    # セクターデータ読み込み（2回目 - キャッシュから）
    start_time = time.time()
    sector_loader.load_sector_data()
    results['sector_data_cached'] = time.time() - start_time
    
    return results

def print_comparison(original_results, optimized_results):
    """結果を比較表示"""
    print("\n" + "="*60)
    print("📊 パフォーマンス比較結果")
    print("="*60)
    
    print(f"{'データタイプ':<20} {'元版(秒)':<12} {'最適化版(秒)':<15} {'改善率':<10}")
    print("-"*60)
    
    comparisons = [
        ('株価データ', 'stock_data', 'stock_data_first'),
        ('企業情報', 'company_info', 'company_info_first'),
        ('財務データ', 'financial_data', 'financial_data_first'),
        ('セクターデータ', 'sector_data', 'sector_data_first'),
    ]
    
    for name, original_key, optimized_key in comparisons:
        original_time = original_results.get(original_key, 0)
        optimized_time = optimized_results.get(optimized_key, 0)
        
        if original_time > 0 and optimized_time > 0:
            improvement = ((original_time - optimized_time) / original_time) * 100
            print(f"{name:<20} {original_time:<12.3f} {optimized_time:<15.3f} {improvement:>8.1f}%")
        else:
            print(f"{name:<20} {original_time:<12.3f} {optimized_time:<15.3f} {'N/A':>8}")
    
    print("\n" + "="*60)
    print("🚀 キャッシュ効果")
    print("="*60)
    
    cache_comparisons = [
        ('株価データ', 'stock_data_first', 'stock_data_cached'),
        ('企業情報', 'company_info_first', 'company_info_cached'),
        ('財務データ', 'financial_data_first', 'financial_data_cached'),
        ('セクターデータ', 'sector_data_first', 'sector_data_cached'),
    ]
    
    for name, first_key, cached_key in cache_comparisons:
        first_time = optimized_results.get(first_key, 0)
        cached_time = optimized_results.get(cached_key, 0)
        
        if first_time > 0 and cached_time > 0:
            speedup = first_time / cached_time if cached_time > 0 else 0
            print(f"{name:<20} 初回: {first_time:.3f}秒, キャッシュ: {cached_time:.3f}秒, 高速化: {speedup:.1f}x")
        else:
            print(f"{name:<20} 初回: {first_time:.3f}秒, キャッシュ: {cached_time:.3f}秒, 高速化: N/A")
    
    # キャッシュ統計
    cache = get_data_cache()
    stats = cache.get_cache_stats()
    print(f"\n📈 キャッシュ統計:")
    print(f"   有効キャッシュ: {stats['valid_cached']}件")
    print(f"   期限切れキャッシュ: {stats['expired_cached']}件")
    print(f"   キャッシュ有効期限: {stats['cache_ttl']}秒")

def main():
    """メイン関数"""
    print("🎯 日本株ダッシュボード パフォーマンスベンチマーク")
    print("="*60)
    
    try:
        # 元のデータローダーのベンチマーク
        original_results = benchmark_original_loader()
        
        # 最適化されたデータローダーのベンチマーク
        optimized_results = benchmark_optimized_loader()
        
        # 結果を比較表示
        print_comparison(original_results, optimized_results)
        
        print("\n✅ ベンチマーク完了!")
        
    except Exception as e:
        print(f"❌ ベンチマーク実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
