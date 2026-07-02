import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("📈 Global Stock Market Dashboard")
st.markdown("Track stock prices using Yahoo Finance")

# -----------------------------
# Stock Suggestions
# -----------------------------
stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Meta": "META",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS"
}

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Stock Selection")

selected_stock = st.sidebar.selectbox(
    "Choose a Stock",
    list(stocks.keys())
)

ticker = stocks[selected_stock]

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max"]
)

# -----------------------------
# Download Data
# -----------------------------
try:
    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        st.warning("No stock data available.")
        st.stop()

    # Handle MultiIndex columns
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    # Latest values
    current_price = round(data["Close"].to_numpy()[-1], 2)
    open_price = round(data["Open"].to_numpy()[-1], 2)
    high_price = round(data["High"].to_numpy()[-1], 2)
    low_price = round(data["Low"].to_numpy()[-1], 2)

    # -----------------------------
    # Current Price Card
    # -----------------------------
    st.metric(
        label=f"{ticker} Current Price",
        value=f"${current_price}"
    )

    # -----------------------------
    # Stock Chart
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Closing Price"
        )
    )

    fig.update_layout(
        title=f"{ticker} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------
    # Metrics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Open", open_price)
    col2.metric("High", high_price)
    col3.metric("Low", low_price)

    # -----------------------------
    # Historical Data
    # -----------------------------
    st.subheader("Latest Stock Data")
    st.dataframe(
        data.tail(10),
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error: {str(e)}")
