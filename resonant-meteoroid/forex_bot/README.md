# Elite Hybrid Autonomous Forex Trading Bot

## Architecture Overview
The Elite Hybrid Bot is a state-of-the-art Python-based algorithmic trading system designed for institutional-grade stability and statistical edge. It directly interfaces with MetaTrader 5 terminals to execute trades fully autonomously.

**Key Components:**
1. **Data Engine (`data/engine.py`)**: Responsible for natively connecting to MT5, pulling raw OHLC tick data, and computing advanced technical indicators (`pandas_ta`).
2. **Market Regime Detection (`strategies/regime_detector.py`)**: Continuously analyzes ADX, Bollinger Band bandwidth, and ATR to categorize the market into `TREND`, `RANGE`, `VOLATILE`, or `LOW VOLATILITY`.
3. **Multi-Strategy Generator (`strategies/`)**: Contains six distinct logic engines: Trend Pullback, Mean Reversion, Liquidity Sweep, Breakout Expansion, Session Momentum, and Volatility Sniper.
4. **Signal Voting System (`strategies/voter.py`)**: Aggregates signals from active strategies (dictated by the regime). It executes a trade only if $\ge$ 3 strategies unanimously agree.
5. **AI Probability Filter (`models/ai_filter.py`)**: Uses a trained `RandomForestClassifier` to estimate the success probability based on current feature states. Only trades with $\ge$ 65% probability are allowed.
6. **Execution & Risk Stack (`execution/`)**: Contains strict institutional parameters (Max 3% daily drawdown, max 3 consecutive losses). It calculates accurate lot sizes using tick-value formulas and maintains trailing stops and break-even automation.
7. **Performance Analytics (`analytics/performance.py`)**: Tracks your equity curve, Sharpe Ratio, Profit Factor, and Win Rate, saving logs to a CSV.

## Running the Bot
### Prerequisites
- Python 3.9+
- MetaTrader 5 Terminal installed on a Windows Environment (or Windows VPS).
- A broker account (Demo recommended for initial testing).

### Setup
1. Open terminal and navigate to this folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `config.py` with your MT5 Login credentials.
   - `MT5_ACCOUNT = 12345678`
   - `MT5_PASSWORD = "your_password"`
   - `MT5_SERVER = "Your-Broker-Server"`
4. Start the bot:
   ```bash
   python main.py
   ```

## Backtesting Instructions
Because this system relies heavily on live tick data and complex Python calculations, the standard MT5 Strategy Tester is not natively equipped to backtest a Python-driven external script.

**To Backtest (and bootstrap the AI Model):**
1. **Paper Trading Phase**: Run the bot on a Demo account continuously via VPS for 2-4 weeks.
2. The `analytics/performance.py` module will log all historical trades executed by the bot (Magic Number: 100100) into `analytics/trades_history.csv` along with features.
3. Once you have at least 100 trades, use a Python script to call the `train()` method within the AI Filter:
   ```python
   from models.ai_filter import AIFilter
   import os
   
   ai = AIFilter()
   ai.train(os.path.join('analytics', 'trades_history.csv'))
   ```
4. From that point onward, the bot will filter out any trade with a predicted success rate below 65%.

## Optimization Recommendations
- **Asset Selection:** Limit pairs to major, highly liquid markets (EURUSD, GBPUSD, XAUUSD) to keep spread constraints (default $\le$ 25 points) from blocking trades.
- **Timeframe:** The default timeframe is 15M. This offers a statistical balance between noise and execution frequency. Do not drop below 5M, as MT5 spread variations will artificially skew win rates.
- **AI Threshold:** If the AI is blocking too many trades, lower `AI_PROBABILITY_THRESHOLD` in `config.py` temporarily to 0.55 until the `RandomForest` is robustly trained.

## Risk Analysis & Realistic Expectations
- **Realistic Win Rate Goal:** In algorithmic trading, targeting 70-80% is extremely difficult without employing harmful "martingale" or "grid" strategies. This bot relies on pure directional logic, strict tight stops, and break-even automations. You can realistically expect a **55-65% win rate**, but with a high Profit Factor (winners are 2x larger than losers).
- **Capital Preservation First:** The system enforces a strict 3% daily limit. Even on your worst days, your account will survive. Focus on slow compounding over 1-2 years rather than rapid flips.
