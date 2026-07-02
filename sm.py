import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# -------------------------
# Custom Styling
# -------------------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.big-font {
    font-size:40px !important;
    font-weight:bold;
    color:#1e3a8a;
}
.stock-card {
    padding:20px;
    border-radius:15px;
    background-color:white;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="big-font">📈 Global Stock Market Dashboard</p>',
    unsafe_allow_html=True
)

st.write("Track real-time stock prices using Yahoo Finance")

# -------------------------
# Suggested Stocks
# -------------------------
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

st.sidebar.title("📌 Suggested Stocks")

for company, ticker in popular_stocks.items():
    st.sidebar.write(f"• {company} ({ticker})")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
)

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1d", "5d", "1mo", "6mo", "1y", "5y", "max"]
)

# -------------------------
# Fetch Data
# -------------------------
try:
    stock = yf.Ticker(ticker)

    info = stock.info

    current_price = info.get(
        "currentPrice",
        info.get("regularMarketPrice", "N/A")
    )

    company_name = info.get(
        "longName",
        ticker
    )

    st.markdown(
        f"""
        <div class="stock-card">
        <h2>{company_name}</h2>
        <h3>Current Price: ${current_price}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    data = stock.history(period=period)

    if not data.empty:

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

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Open",
            round(data["Open"].iloc[-1], 2)
        )

        col2.metric(
            "High",
            round(data["High"].iloc[-1], 2)
        )

        col3.metric(
            "Low",
            round(data["Low"].iloc[-1], 2)
        )

        st.subheader("Company Summary")

        summary = info.get(
            "longBusinessSummary",
            "No company description available."
        )

        st.write(summary)

    else:
        st.warning("No data available.")

except Exception as e:
    st.error(f"Error: {e}")
