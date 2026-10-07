import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# Set konfigurasi halaman web
st.set_page_config(page_title="Blackbox X-Trade", layout="wide", page_icon="📈")

# Header & Judul Utama
st.title("⬛ Blackbox X-Trade")
st.markdown("**Professional XAUUSD Analysis, Orderbook & Geopolitics Dashboard**")
st.divider()

# Fungsi untuk mengambil data Emas dari Yahoo Finance
@st.cache_data(ttl=300) # Data di-cache selama 5 menit
def get_gold_data():
    # GC=F adalah kode untuk Gold Futures (mendekati pergerakan XAUUSD)
    gold = yf.Ticker("GC=F")
    df = gold.history(period="1mo", interval="1h")
    return df

df = get_gold_data()

# Membuat Layout Dua Kolom
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Live Chart (Timeframe 1H)")
    if not df.empty:
        # Membuat Candlestick chart yang interaktif menggunakan Plotly
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])
        
        fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Gagal mengambil data market dari server.")

with col2:
    st.subheader("⚡ Signal & Orderbook Tracker")
    current_price = df['Close'].iloc[-1] if not df.empty else 0
    st.metric(label="Current Gold Price (Est.)", value=f"${current_price:,.2f}")
    
    st.markdown("""
    ### 🔴 ACTIVE SETUP: SELL LIMIT
    - **Entry Zone:** $4,145 - $4,152
    - **Stop Loss (SL):** $4,165
    - **Take Profit (TP):** $4,110
    - **Status:** `WAITING`
    """)
    
    st.divider()
    st.markdown("#### 👥 Retail Sentiment")
    # Tampilan visual bar untuk sentimen ritel (Contoh data statis, nanti bisa dikonek ke API)
    st.progress(0.74, text="74% LONG (Retail Buyers)")
    st.progress(0.26, text="26% SHORT (Retail Sellers)")
    st.info("💡 **Institutional Bias:** Smart Money sedang SELL untuk menekan harga dan menyapu Stop Loss dari 74% buyer ritel.")

st.divider()

# Bagian Laporan Fundamental
st.subheader("📝 Market, News & Geopolitics Report")
st.markdown("""
**Update Sentimen Makro:**
- **DXY & Yield:** Dolar AS sangat kuat. Yield Obligasi 10-Tahun bertahan di atas 5.3%, menekan aset *non-yielding* seperti emas.
- **Geopolitik:** Ketegangan di Timur Tengah saat ini justru melambungkan harga Minyak. Minyak naik = Inflasi naik = Suku bunga ditahan tinggi. Efek ini menjadi **Bearish** untuk Emas.
- **Data Ekonomi:** Waspada rilis *FOMC Minutes*. Pastikan semua pending order aman sebelum news dirilis.
""")

st.caption("© 2026 Blackbox X-Trade. Dikembangkan dengan Streamlit & AI.")
