import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Global Stock Market Dashboard")

popular_stocks = {
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

selected = st.sidebar.selectbox(
    "Select Stock",
    list(popular_stocks.keys())
)

ticker = popular_stocks[selected]

period = st.sidebar.selectbox(
    "Select Period",
    ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"]
)

try:

    data = yf.download(
        ticker,
        period=period,
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        st.error("No stock data found.")
        st.stop()

    current_price = round(
        float(data["Close"].iloc[-1]),
        2
    )

    st.metric(
        "Current Price",
        f"${current_price}"
    )

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
        title=f"{ticker} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

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

    st.subheader("Recent Data")

    st.dataframe(
        data.tail(10)
    )

except Exception as e:
    st.error(f"Application Error: {str(e)}")
