# Trading Bot - Binance Futures Trading Bot

A comprehensive Binance Futures (USDT-M) trading bot with testnet support for safe trading practice and live trading capabilities.

## Features

- **Futures Trading**: Full support for Binance USDT-M futures trading
- **Multiple Order Types**: Market, Limit, Stop-Limit, and OCO orders
- **Testnet Support**: Safe testing environment with paper trading
- **Position Management**: Real-time position tracking and management
- **Leverage Control**: Adjustable leverage settings (1-125x)
- **Interactive CLI**: User-friendly command-line interface
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Prerequisites

- Python 3.7 or higher
- Binance account with API access
- API key with futures trading permissions

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Trading-Bot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Binance API Setup

### 1. Create Binance Account

1. Go to [Binance](https://www.binance.com) and create an account
2. Complete KYC verification for full access

### 2. Generate API Keys

1. Go to **Account** → **API Management**
2. Click **Create API** and choose **System Generated**
3. Enter a label for your API key
4. Complete security verification (2FA)
5. **Important**: Save your API Key and Secret Key securely

### 3. Configure API Permissions

Enable the following permissions for your API key:
- ✅ **Enable Reading**
- ✅ **Enable Futures** (Essential for futures trading)
- ✅ **Enable Spot & Margin Trading** (Optional)
- ❌ **Enable Withdrawals** (Not recommended for trading bots)

### 4. IP Whitelist (Recommended)

1. In API Management, click **Edit restrictions**
2. Add your current IP address to the whitelist
3. This enhances security by restricting API access to your IP

## Testnet Setup (Recommended for Beginners)

### 1. Create Testnet Account

1. Go to [Binance Testnet](https://testnet.binancefuture.com/)
2. Login with your main Binance account
3. The testnet provides a safe environment with virtual funds

### 2. Generate Testnet API Keys

1. In the testnet interface, go to **API Keys**
2. Create new API keys specifically for testnet
3. Enable futures trading permissions
4. Note: Testnet API keys are different from mainnet keys

### 3. Get Test Funds

1. In the testnet, you'll receive virtual USDT for testing
2. Use the **Get Test Funds** feature if you need more virtual balance

## Configuration

### 1. Environment Variables (Recommended)

Create a `.env` file in the project root:

```bash
# Testnet API Keys
BINANCE_TESTNET_API_KEY=your_testnet_api_key_here
BINANCE_TESTNET_API_SECRET=your_testnet_api_secret_here

# Mainnet API Keys (for live trading)
BINANCE_API_KEY=your_mainnet_api_key_here
BINANCE_API_SECRET=your_mainnet_api_secret_here
```

### 2. Test Your Connection

Use the debug script to verify your API connection:

```bash
python debug_connection.py YOUR_API_KEY YOUR_API_SECRET
```

This will test:
- Basic client creation
- System status
- Server time
- API key authentication
- Account permissions
- Available balances

## Usage

### 1. Run the Bot

**For Testnet (Recommended):**
```bash
python trading_bot.py --api-key YOUR_TESTNET_API_KEY --api-secret YOUR_TESTNET_API_SECRET --testnet
```

**For Live Trading:**
```bash
python trading_bot.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET
```

### 2. Available Commands

Once the bot is running, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `balance` | Show futures account balance | `balance` |
| `positions` | Show current positions | `positions` |
| `price <symbol>` | Get current price | `price BTCUSDT` |
| `market <symbol> <side> <quantity>` | Place market order | `market BTCUSDT BUY 0.001` |
| `limit <symbol> <side> <quantity> <price>` | Place limit order | `limit BTCUSDT BUY 0.001 50000` |
| `stop <symbol> <side> <quantity> <price> <stop_price>` | Place stop-limit order | `stop BTCUSDT SELL 0.001 45000 44000` |
| `oco <symbol> <side> <qty> <price> <stop> <stop_limit>` | Place OCO order | `oco BTCUSDT SELL 0.001 52000 48000 47500` |
| `status <symbol> <order_id>` | Get order status | `status BTCUSDT 123456` |
| `cancel <symbol> <order_id>` | Cancel order | `cancel BTCUSDT 123456` |
| `leverage <symbol> <leverage>` | Set leverage | `leverage BTCUSDT 10` |
| `quit` | Exit bot | `quit` |

### 3. Example Trading Session

```bash
💬 Enter command: balance
💰 Futures Balance: {
  "totalWalletBalance": 1000.0,
  "availableBalance": 1000.0,
  ...
}

💬 Enter command: price BTCUSDT
💲 Current price for BTCUSDT: 50000.0

💬 Enter command: leverage BTCUSDT 10
✅ Leverage set: {"leverage": 10, "symbol": "BTCUSDT"}

💬 Enter command: market BTCUSDT BUY 0.001
✅ Market order result: {
  "orderId": 123456,
  "symbol": "BTCUSDT",
  "status": "FILLED",
  ...
}

💬 Enter command: positions
📍 Positions: {
  "BTCUSDT": {
    "positionAmt": 0.001,
    "entryPrice": 50000.0,
    "unRealizedProfit": 0.0,
    ...
  }
}
```

## Troubleshooting

### Common Issues

1. **APIError(code=-2015): Invalid API-key, IP, or permissions**
   - Check your API key and secret are correct
   - Ensure futures trading is enabled in API permissions
   - Verify your IP is not restricted
   - Make sure you're using the correct testnet/mainnet environment

2. **Connection timeouts**
   - Check your internet connection
   - Verify Binance API is not down
   - Try again after a few minutes

3. **Insufficient balance errors**
   - Check your account balance with the `balance` command
   - For testnet, use the "Get Test Funds" feature
   - Reduce your order size

4. **Symbol not found**
   - Ensure you're using the correct symbol format (e.g., `BTCUSDT`, not `BTC/USDT`)
   - Check if the symbol is available for futures trading

### Debug Mode

For detailed debugging, check the log files:
- `futures_trading_bot.log` - Main bot logs
- `trading_bot.log` - Legacy spot trading logs

### Getting Help

1. Check the Binance API documentation
2. Verify your API key permissions
3. Test with small amounts first
4. Use testnet before live trading

## Security Best Practices

1. **Never share your API keys** - Keep them secure and private
2. **Use IP whitelisting** - Restrict API access to your IP address
3. **Disable withdrawal permissions** - Only enable necessary permissions
4. **Start with testnet** - Always test your strategies safely first
5. **Use environment variables** - Don't hardcode API keys in your code
6. **Regular key rotation** - Periodically regenerate your API keys

## Risk Disclaimer

⚠️ **Important**: Trading cryptocurrencies involves significant financial risk. This bot is for educational purposes. Always:

- Start with small amounts
- Test thoroughly on testnet first
- Never invest more than you can afford to lose
- Understand the risks of leveraged trading
- Monitor your positions regularly

## License

This project is for educational purposes. Please ensure compliance with local regulations and Binance terms of service.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the log files for error messages
3. Test your API connection with the debug script
4. Ensure proper API permissions are set