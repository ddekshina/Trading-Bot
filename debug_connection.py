#!/usr/bin/env python3
"""
Debug script to test Binance API connection
"""

from binance.client import Client
import sys

def test_connection(api_key, api_secret):
    """Test different connection scenarios"""
    
    print("=== Testing Binance API Connection ===\n")
    
    # Test 1: Basic client creation
    print("1. Creating client...")
    try:
        client = Client(api_key, api_secret, testnet=True)
        print("   ✅ Client created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create client: {e}")
        return False
    
    # Test 2: System status (no authentication required)
    print("\n2. Testing system status...")
    try:
        status = client.get_system_status()
        print(f"   ✅ System status: {status}")
    except Exception as e:
        print(f"   ❌ System status failed: {e}")
    
    # Test 3: Server time (no authentication required)
    print("\n3. Testing server time...")
    try:
        server_time = client.get_server_time()
        print(f"   ✅ Server time: {server_time}")
    except Exception as e:
        print(f"   ❌ Server time failed: {e}")
    
    # Test 4: API key permissions (requires authentication)
    print("\n4. Testing API key permissions...")
    try:
        # Try to get account info (this requires API key authentication)
        account = client.get_account()
        print("   ✅ API key authentication successful")
        print(f"   Account permissions: {account.get('permissions', 'N/A')}")
        
        # Show balances
        balances = [b for b in account['balances'] if float(b['free']) > 0]
        if balances:
            print("   Available balances:")
            for balance in balances[:5]:  # Show first 5
                print(f"     {balance['asset']}: {balance['free']}")
        else:
            print("   No balances found - you may need to get test funds")
            
    except Exception as e:
        print(f"   ❌ API key authentication failed: {e}")
        print("\n   Possible issues:")
        print("   - API key permissions not enabled")
        print("   - IP restrictions blocking your connection")
        print("   - API key/secret incorrect")
        print("   - Wrong testnet environment")
        return False
    
    # Test 5: Try different endpoints
    print("\n5. Testing different endpoints...")
    
    # Test exchange info
    try:
        exchange_info = client.get_exchange_info()
        print(f"   ✅ Exchange info: {len(exchange_info['symbols'])} symbols available")
    except Exception as e:
        print(f"   ❌ Exchange info failed: {e}")
    
    # Test ticker
    try:
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
        print(f"   ✅ BTCUSDT ticker: {ticker['price']}")
    except Exception as e:
        print(f"   ❌ Ticker failed: {e}")
    
    print("\n=== Connection test complete ===")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python debug_connection.py <api_key> <api_secret>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    api_secret = sys.argv[2]
    
    # Hide part of the keys for security
    masked_key = api_key[:8] + "..." + api_key[-8:]
    masked_secret = api_secret[:8] + "..." + api_secret[-8:]
    print(f"Testing with API key: {masked_key}")
    print(f"Testing with API secret: {masked_secret}")
    
    test_connection(api_key, api_secret)