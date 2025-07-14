# Portfolio Optimization Backtesting Engine

This project loads historical stock data, simulates portfolio strategies, stores metrics in PostgreSQL, and visualizes performance using Streamlit.

## 📂 Features
- Load stock data from CSV
- Generate portfolio values
- Compute Sharpe Ratio, Return, Volatility
- Visualize with Streamlit dashboard

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Load data into PostgreSQL
python load_to_db.py

# Generate portfolio values
python generate_portfolios.py

# Launch dashboard
streamlit run streamlit_app.py
