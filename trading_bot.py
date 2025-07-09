#!/usr/bin/env python3
"""
Binance Futures (USDT-M) Testnet Trading Bot
Built for the assignment requirements with proper futures trading functionality
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, Optional, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('futures_trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BasicBot:
    """
    A basic futures trading bot for Binance Testnet (USDT-M)
    Implements the required BasicBot class structure from the assignment
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Initialize Binance client for futures trading
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet
        )
        
        logger.info(f"BasicBot initialized with testnet={testnet}")
        
    def validate_connection(self) -> bool:
        """
        Validate API connection and permissions for futures trading
        
        Returns:
            bool: True if connection is valid
        """
        try:
            # Test futures connectivity
            server_time = self.client.futures_time()
            logger.info(f"Futures server time: {server_time}")
            
            # Test futures account info
            account_info = self.client.futures_account()
            logger.info("Futures API connection validated successfully")
            
            # Show futures account balance
            logger.info(f"Total wallet balance: {account_info.get('totalWalletBalance', 0)} USDT")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False
    
    def get_futures_balance(self) -> Dict[str, Any]:
        """
        Get futures account balance information
        
        Returns:
            dict: Futures account balance information
        """
        try:
            account_info = self.client.futures_account()
            
            balance_info = {
                'totalWalletBalance': float(account_info.get('totalWalletBalance', 0)),
                'totalUnrealizedProfit': float(account_info.get('totalUnrealizedProfit', 0)),
                'totalMarginBalance': float(account_info.get('totalMarginBalance', 0)),
                'totalPositionInitialMargin': float(account_info.get('totalPositionInitialMargin', 0)),
                'totalOpenOrderInitialMargin': float(account_info.get('totalOpenOrderInitialMargin', 0)),
                'availableBalance': float(account_info.get('availableBalance', 0)),
                'maxWithdrawAmount': float(account_info.get('maxWithdrawAmount', 0))
            }
            
            # Get individual asset balances
            assets = {}
            for asset in account_info.get('assets', []):
                if float(asset['walletBalance']) > 0:
                    assets[asset['asset']] = {
                        'walletBalance': float(asset['walletBalance']),
                        'unrealizedProfit': float(asset['unrealizedProfit']),
                        'marginBalance': float(asset['marginBalance']),
                        'maintMargin': float(asset['maintMargin']),
                        'initialMargin': float(asset['initialMargin']),
                        'positionInitialMargin': float(asset['positionInitialMargin']),
                        'openOrderInitialMargin': float(asset['openOrderInitialMargin'])
                    }
            
            balance_info['assets'] = assets
            
            logger.info(f"Futures balance retrieved: {balance_info['totalWalletBalance']} USDT")
            return balance_info
            
        except Exception as e:
            logger.error(f"Error getting futures balance: {str(e)}")
            return {}
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get futures symbol information and filters
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            
        Returns:
            dict: Symbol information
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    logger.info(f"Futures symbol info for {symbol}: {symbol_info['status']}")
                    return symbol_info
                    
            logger.warning(f"Futures symbol {symbol} not found")
            return {}
            
        except Exception as e:
            logger.error(f"Error getting futures symbol info: {str(e)}")
            return {}
    
    def place_market_order(self, symbol: str, side: str, quantity: float, 
                          reduce_only: bool = False) -> Dict[str, Any]:
        """
        Place a futures market order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            reduce_only: Whether this is a reduce-only order
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing futures market order: {side} {quantity} {symbol}")
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
            }
            
            if reduce_only:
                order_params['reduceOnly'] = 'true'
            
            order = self.client.futures_create_order(**order_params)
            
            logger.info(f"Futures market order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing futures market order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing futures market order: {str(e)}")
            return {'error': str(e)}
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float,
                         reduce_only: bool = False) -> Dict[str, Any]:
        """
        Place a futures limit order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Order price
            reduce_only: Whether this is a reduce-only order
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing futures limit order: {side} {quantity} {symbol} at {price}")
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': 'GTC'
            }
            
            if reduce_only:
                order_params['reduceOnly'] = 'true'
            
            order = self.client.futures_create_order(**order_params)
            
            logger.info(f"Futures limit order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing futures limit order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing futures limit order: {str(e)}")
            return {'error': str(e)}
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float, 
                              reduce_only: bool = False) -> Dict[str, Any]:
        """
        Place a futures stop-limit order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            reduce_only: Whether this is a reduce-only order
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing futures stop-limit order: {side} {quantity} {symbol} at {price}, stop at {stop_price}")
            
            order_params = {
                'symbol': symbol,
                'side': side,
                'type': 'STOP',
                'quantity': quantity,
                'price': price,
                'stopPrice': stop_price,
                'timeInForce': 'GTC'
            }
            
            if reduce_only:
                order_params['reduceOnly'] = 'true'
            
            order = self.client.futures_create_order(**order_params)
            
            logger.info(f"Futures stop-limit order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing futures stop-limit order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing futures stop-limit order: {str(e)}")
            return {'error': str(e)}
    
    def place_oco_order(self, symbol: str, side: str, quantity: float,
                       price: float, stop_price: float, stop_limit_price: float) -> Dict[str, Any]:
        """
        Place an OCO (One-Cancels-Other) order - BONUS feature
        
        Args:
            symbol: Trading symbol
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit order price
            stop_price: Stop price
            stop_limit_price: Stop limit price
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing OCO order: {side} {quantity} {symbol}")
            
            # OCO orders need to be simulated with two separate orders for futures
            # This is a simplified implementation
            limit_order = self.place_limit_order(symbol, side, quantity, price)
            if 'error' in limit_order:
                return limit_order
                
            stop_order = self.place_stop_limit_order(symbol, side, quantity, stop_limit_price, stop_price)
            
            result = {
                'oco_simulation': True,
                'limit_order': limit_order,
                'stop_order': stop_order
            }
            
            logger.info(f"OCO order simulation completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error placing OCO order: {str(e)}")
            return {'error': str(e)}
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get futures order status
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            dict: Order status information
        """
        try:
            order_status = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Futures order status retrieved: {order_status}")
            return order_status
            
        except Exception as e:
            logger.error(f"Error getting futures order status: {str(e)}")
            return {'error': str(e)}
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel a futures order
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            dict: Cancel response
        """
        try:
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Futures order cancelled successfully: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error cancelling futures order: {str(e)}")
            return {'error': str(e)}
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current futures price for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            float: Current price
        """
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current futures price for {symbol}: {price}")
            return price
            
        except Exception as e:
            logger.error(f"Error getting current futures price: {str(e)}")
            return 0.0
    
    def get_positions(self) -> Dict[str, Any]:
        """
        Get current futures positions
        
        Returns:
            dict: Position information
        """
        try:
            positions = self.client.futures_position_information()
            
            # Filter out positions with zero size
            active_positions = {}
            for position in positions:
                if float(position['positionAmt']) != 0:
                    active_positions[position['symbol']] = {
                        'symbol': position['symbol'],
                        'positionAmt': float(position['positionAmt']),
                        'entryPrice': float(position['entryPrice']),
                        'markPrice': float(position['markPrice']),
                        'unRealizedProfit': float(position['unRealizedProfit']),
                        'percentage': float(position['percentage']),
                        'positionSide': position['positionSide']
                    }
            
            logger.info(f"Active positions retrieved: {len(active_positions)}")
            return active_positions
            
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return {}
    
    def set_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """
        Set leverage for a symbol
        
        Args:
            symbol: Trading symbol
            leverage: Leverage level (1-125)
            
        Returns:
            dict: Response
        """
        try:
            result = self.client.futures_change_leverage(
                symbol=symbol,
                leverage=leverage
            )
            
            logger.info(f"Leverage set for {symbol}: {leverage}x")
            return result
            
        except Exception as e:
            logger.error(f"Error setting leverage: {str(e)}")
            return {'error': str(e)}


def main():
    """
    Main function with enhanced command-line interface
    """
    parser = argparse.ArgumentParser(description='Binance Futures Trading Bot')
    parser.add_argument('--api-key', required=True, help='Binance API Key')
    parser.add_argument('--api-secret', required=True, help='Binance API Secret')
    parser.add_argument('--testnet', action='store_true', default=True, help='Use testnet (default: True)')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = BasicBot(args.api_key, args.api_secret, args.testnet)
    
    # Validate connection
    if not bot.validate_connection():
        logger.error("Failed to connect to Binance Futures API. Exiting.")
        print("\n❌ Connection failed. Please check:")
        print("1. Your API key and secret are correct")
        print("2. API key has futures trading permissions enabled")
        print("3. You're using the correct testnet environment")
        print("4. Your IP is not restricted")
        sys.exit(1)
    
    # Interactive CLI
    print("\n🚀 === Binance Futures Trading Bot ===")
    print("📊 Environment: TESTNET" if args.testnet else "LIVE")
    print("\n📋 Commands:")
    print("1. balance - Show futures account balance")
    print("2. positions - Show current positions")
    print("3. price <symbol> - Get current price")
    print("4. market <symbol> <side> <quantity> - Place market order")
    print("5. limit <symbol> <side> <quantity> <price> - Place limit order")
    print("6. stop <symbol> <side> <quantity> <price> <stop_price> - Place stop-limit order")
    print("7. oco <symbol> <side> <quantity> <price> <stop_price> <stop_limit_price> - Place OCO order")
    print("8. status <symbol> <order_id> - Get order status")
    print("9. cancel <symbol> <order_id> - Cancel order")
    print("10. leverage <symbol> <leverage> - Set leverage")
    print("11. quit - Exit bot")
    print()
    
    while True:
        try:
            command = input("💬 Enter command: ").strip().split()
            
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'quit':
                print("👋 Goodbye!")
                break
                
            elif cmd == 'balance':
                balance = bot.get_futures_balance()
                print(f"💰 Futures Balance: {json.dumps(balance, indent=2)}")
                
            elif cmd == 'positions':
                positions = bot.get_positions()
                if positions:
                    print(f"📍 Positions: {json.dumps(positions, indent=2)}")
                else:
                    print("📍 No active positions")
                
            elif cmd == 'price':
                if len(command) < 2:
                    print("❌ Usage: price <symbol>")
                    continue
                symbol = command[1].upper()
                price = bot.get_current_price(symbol)
                print(f"💲 Current price for {symbol}: {price}")
                
            elif cmd == 'market':
                if len(command) < 4:
                    print("❌ Usage: market <symbol> <side> <quantity>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                
                result = bot.place_market_order(symbol, side, quantity)
                if 'error' in result:
                    print(f"❌ Market order failed: {result['error']}")
                else:
                    print(f"✅ Market order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'limit':
                if len(command) < 5:
                    print("❌ Usage: limit <symbol> <side> <quantity> <price>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                price = float(command[4])
                
                result = bot.place_limit_order(symbol, side, quantity, price)
                if 'error' in result:
                    print(f"❌ Limit order failed: {result['error']}")
                else:
                    print(f"✅ Limit order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'stop':
                if len(command) < 6:
                    print("❌ Usage: stop <symbol> <side> <quantity> <price> <stop_price>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                price = float(command[4])
                stop_price = float(command[5])
                
                result = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                if 'error' in result:
                    print(f"❌ Stop-limit order failed: {result['error']}")
                else:
                    print(f"✅ Stop-limit order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'oco':
                if len(command) < 7:
                    print("❌ Usage: oco <symbol> <side> <quantity> <price> <stop_price> <stop_limit_price>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                price = float(command[4])
                stop_price = float(command[5])
                stop_limit_price = float(command[6])
                
                result = bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
                if 'error' in result:
                    print(f"❌ OCO order failed: {result['error']}")
                else:
                    print(f"✅ OCO order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'status':
                if len(command) < 3:
                    print("❌ Usage: status <symbol> <order_id>")
                    continue
                symbol = command[1].upper()
                order_id = int(command[2])
                
                result = bot.get_order_status(symbol, order_id)
                if 'error' in result:
                    print(f"❌ Order status failed: {result['error']}")
                else:
                    print(f"📊 Order status: {json.dumps(result, indent=2)}")
                
            elif cmd == 'cancel':
                if len(command) < 3:
                    print("❌ Usage: cancel <symbol> <order_id>")
                    continue
                symbol = command[1].upper()
                order_id = int(command[2])
                
                result = bot.cancel_order(symbol, order_id)
                if 'error' in result:
                    print(f"❌ Cancel failed: {result['error']}")
                else:
                    print(f"✅ Cancel result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'leverage':
                if len(command) < 3:
                    print("❌ Usage: leverage <symbol> <leverage>")
                    continue
                symbol = command[1].upper()
                leverage = int(command[2])
                
                result = bot.set_leverage(symbol, leverage)
                if 'error' in result:
                    print(f"❌ Leverage setting failed: {result['error']}")
                else:
                    print(f"✅ Leverage set: {json.dumps(result, indent=2)}")
                
            else:
                print("❌ Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()