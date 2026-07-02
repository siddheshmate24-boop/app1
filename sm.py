import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Global Stock Market Dashboard")
st.markdown("Track stock prices using Yahoo Finance")

# Stock Suggestions
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

# Sidebar
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

# Download Data
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

    current_price = round(float(data["Close"].iloc[-1]), 2)

    st.metric(
        label="Current Price",
        value=f"${current_price}"
    )

    # Chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price"
        )
    )

    fig.update_layout(
        title=f"{ticker} Closing Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Open",
        round(float(data["Open"].iloc[-1]), 2)
    )

    col2.metric(
        "High",
        round(float(data["High"].iloc[-1]), 2)
    )

    col3.metric(
        "Low",
        round(float(data["Low"].iloc[-1]), 2)
    )

    st.subheader("Latest Stock Data")
    st.dataframe(data.tail(10))

except Exception as e:
    st.error(f"Error: {e}")
