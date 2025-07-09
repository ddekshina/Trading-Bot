#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
A simplified trading bot for educational purposes using Binance Futures Testnet
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
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BasicBot:
    """
    A basic trading bot for Binance Futures Testnet
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
        
        # Initialize Binance client
        self.client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet
        )
        
        # Set base URL for testnet
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com'
        
        logger.info(f"Bot initialized with testnet={testnet}")
        
    def validate_connection(self) -> bool:
        """
        Validate API connection and permissions
        
        Returns:
            bool: True if connection is valid
        """
        try:
            # Test connectivity
            status = self.client.get_system_status()
            logger.info(f"System status: {status}")
            
            # Get account info to validate permissions
            account_info = self.client.futures_account()
            logger.info("API connection validated successfully")
            logger.info(f"Account balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            
            return True
            
        except Exception as e:
            logger.error(f"Connection validation failed: {str(e)}")
            return False
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance information
        
        Returns:
            dict: Account balance information
        """
        try:
            account_info = self.client.futures_account()
            balance_info = {
                'total_balance': account_info.get('totalWalletBalance', '0'),
                'available_balance': account_info.get('availableBalance', '0'),
                'total_unrealized_pnl': account_info.get('totalUnrealizedProfit', '0')
            }
            
            logger.info(f"Account balance retrieved: {balance_info}")
            return balance_info
            
        except Exception as e:
            logger.error(f"Error getting account balance: {str(e)}")
            return {}
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get symbol information and filters
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            
        Returns:
            dict: Symbol information
        """
        try:
            exchange_info = self.client.futures_exchange_info()
            
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] == symbol:
                    logger.info(f"Symbol info for {symbol}: {symbol_info['status']}")
                    return symbol_info
                    
            logger.warning(f"Symbol {symbol} not found")
            return {}
            
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}")
            return {}
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing market order: {side} {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"Market order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing market order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing market order: {str(e)}")
            return {'error': str(e)}
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Place a limit order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Order price
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing limit order: {side} {quantity} {symbol} at {price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  # Good Till Canceled
            )
            
            logger.info(f"Limit order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing limit order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing limit order: {str(e)}")
            return {'error': str(e)}
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float) -> Dict[str, Any]:
        """
        Place a stop-limit order (Bonus feature)
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            
        Returns:
            dict: Order response
        """
        try:
            logger.info(f"Placing stop-limit order: {side} {quantity} {symbol} at {price}, stop at {stop_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce='GTC'
            )
            
            logger.info(f"Stop-limit order placed successfully: {order}")
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing stop-limit order: {e}")
            return {'error': str(e)}
        except Exception as e:
            logger.error(f"Error placing stop-limit order: {str(e)}")
            return {'error': str(e)}
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order status
        
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
            
            logger.info(f"Order status retrieved: {order_status}")
            return order_status
            
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            return {'error': str(e)}
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order
        
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
            
            logger.info(f"Order cancelled successfully: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return {'error': str(e)}
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            float: Current price
        """
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
            
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            return 0.0


def main():
    """
    Main function with command-line interface
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
        logger.error("Failed to connect to Binance API. Exiting.")
        sys.exit(1)
    
    # Interactive CLI
    print("\n=== Binance Futures Trading Bot ===")
    print("Commands:")
    print("1. balance - Show account balance")
    print("2. price <symbol> - Get current price")
    print("3. market <symbol> <side> <quantity> - Place market order")
    print("4. limit <symbol> <side> <quantity> <price> - Place limit order")
    print("5. stop <symbol> <side> <quantity> <price> <stop_price> - Place stop-limit order")
    print("6. status <symbol> <order_id> - Get order status")
    print("7. cancel <symbol> <order_id> - Cancel order")
    print("8. quit - Exit bot")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().split()
            
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'quit':
                print("Goodbye!")
                break
                
            elif cmd == 'balance':
                balance = bot.get_account_balance()
                print(f"Balance: {json.dumps(balance, indent=2)}")
                
            elif cmd == 'price':
                if len(command) < 2:
                    print("Usage: price <symbol>")
                    continue
                symbol = command[1].upper()
                price = bot.get_current_price(symbol)
                print(f"Current price for {symbol}: {price}")
                
            elif cmd == 'market':
                if len(command) < 4:
                    print("Usage: market <symbol> <side> <quantity>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                
                result = bot.place_market_order(symbol, side, quantity)
                print(f"Market order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'limit':
                if len(command) < 5:
                    print("Usage: limit <symbol> <side> <quantity> <price>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                price = float(command[4])
                
                result = bot.place_limit_order(symbol, side, quantity, price)
                print(f"Limit order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'stop':
                if len(command) < 6:
                    print("Usage: stop <symbol> <side> <quantity> <price> <stop_price>")
                    continue
                symbol = command[1].upper()
                side = command[2].upper()
                quantity = float(command[3])
                price = float(command[4])
                stop_price = float(command[5])
                
                result = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print(f"Stop-limit order result: {json.dumps(result, indent=2)}")
                
            elif cmd == 'status':
                if len(command) < 3:
                    print("Usage: status <symbol> <order_id>")
                    continue
                symbol = command[1].upper()
                order_id = int(command[2])
                
                result = bot.get_order_status(symbol, order_id)
                print(f"Order status: {json.dumps(result, indent=2)}")
                
            elif cmd == 'cancel':
                if len(command) < 3:
                    print("Usage: cancel <symbol> <order_id>")
                    continue
                symbol = command[1].upper()
                order_id = int(command[2])
                
                result = bot.cancel_order(symbol, order_id)
                print(f"Cancel result: {json.dumps(result, indent=2)}")
                
            else:
                print("Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()