import finnhub
import json
import os
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
CACHE_FILE = "stock_price_cache.json"
CACHE_TTL_SECONDS = 24 * 60 * 60  # 24 hours

def get_live_stock_price(stock_ticker: str) -> Dict[str, Any]:
    # Load existing cache (if any)
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cache = json.load(f)
        except (json.JSONDecodeError, OSError):
            # If file is corrupted, start fresh
            cache = {}

    # Check if we have a valid cached entry for this stock
    if stock_ticker in cache:
        entry = cache[stock_ticker]
        cached_time = entry.get("timestamp", 0)
        if time.time() - cached_time < CACHE_TTL_SECONDS:
            # Return cached data (it's still fresh)
            return entry.get("data", {})

    # Fetch fresh data from FinHub
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    try:
        quote = finnhub_client.quote(stock_ticker)
        print(f"Fetched fresh quote for {stock_ticker}: {quote}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch quote from FinHub: {e}")

    # Update cache entry for this stock
    cache[stock_ticker] = {
        "timestamp": time.time(),
        "data": quote
    }

    # Write entire cache back to file
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except OSError as e:
        print(f"Warning: could not write cache file: {e}")

    return quote