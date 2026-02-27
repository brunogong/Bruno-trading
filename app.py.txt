"""
TRADING TERMINAL PRO - Web App
Accessibile da qualsiasi dispositivo
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Configurazione pagina
st.set_page_config(
    page_title="Trading Pro",
    page_icon="??",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS per mobile
st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    .header {
        background: linear-gradient(135deg, #1e1e1e, #2d2d2d);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        border-left: 5px solid #00ff00;
    }
    .price-box {
        background: #000;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #00ff00;
        margin: 20px 0;
    }
    .price {
        font-size: 48px;
        color: #00ff00;
        font-weight: bold;
    }
    .metric {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    .signal-buy { color: #00ff00; font-size: 24px; }
    .signal-sell { color: #ff4444; font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'><h1 style='color:#00ff00;'>?? TRADING TERMINAL PRO</h1><p style='color:#888;'>Analisi in Tempo Reale</p></div>", unsafe_allow_html=True)

# Input nella sidebar
with st.sidebar:
    st.markdown("### ?? Controlli")
    
    assets = {
        'XAU/USD (Oro)': 'GC=F',
        'EUR/USD': 'EURUSD=X',
        'GBP/USD': 'GBPUSD=X',
        'BTC/USD': 'BTC-USD',
        'S&P 500': '^GSPC'
    }
    
    asset = st.selectbox("?? Asset", list(assets.keys()))
    timeframe = st.selectbox("?? Timeframe", ["1h", "4h", "1d"])
    capitale = st.number_input("?? Capitale (€)", value=1000, step=100)
    rischio = st.slider("?? Rischio %", 0.5, 3.0, 1.0, 0.1)

# Bottone analisi
if st.button("?? ANALIZZA ORA", type="primary", use_container_width=True):
    
    with st.spinner("?? Caricamento dati..."):
        try:
            symbol = assets[asset]
            
            # Download dati
            period_map = {'1h': '5d', '4h': '1mo', '1d': '3mo'}
            data = yf.download(symbol, period=period_map[timeframe], 
                              interval=timeframe, auto_adjust=True, progress=False)
            
            if not data.empty:
                # Prezzo attuale
                if isinstance(data['Close'], pd.DataFrame):
                    current_price = float(data['Close'].iloc[-1, 0])
                else:
                    current_price = float(data['Close'].iloc[-1])
                
                # Calcoli base
                high_20 = float(data['High'].tail(20).max())
                low_20 = float(data['Low'].tail(20).min())
                
                # RSI semplice
                try:
                    close_prices = data['Close'].values if not isinstance(data['Close'], pd.DataFrame) else data['Close'].iloc[:,0].values
                    delta = pd.Series(close_prices).diff()
                    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
                except:
                    current_rsi = 50
                
                # ATR semplice
                try:
                    high = data['High'].values if not isinstance(data['High'], pd.DataFrame) else data['High'].iloc[:,0].values
                    low = data['Low'].values if not isinstance(data['Low'], pd.DataFrame) else data['Low'].iloc[:,0].values
                    close = data['Close'].values if not isinstance(data['Close'], pd.DataFrame) else data['Close'].iloc[:,0].values
                    tr = np.maximum(high[1:] - low[1:], 
                                   np.abs(high[1:] - close[:-1]), 
                                   np.abs(low[1:] - close[:-1]))
                    atr = float(np.mean(tr[-14:]))
                except:
                    atr = (high_20 - low_20) * 0.1
                
                # Genera segnale
                if current_rsi > 50:
                    signal = "?? BUY"
                    entry = low_20 + (high_20 - low_20) * 0.382
                    sl = entry - (atr * 1.5)
                    tp = entry + (atr * 2)
                else:
                    signal = "?? SELL"
                    entry = high_20 - (high_20 - low_20) * 0.382
                    sl = entry + (atr * 1.5)
                    tp = entry - (atr * 2)
                
                # Calcolo lotti
                multiplier = 100 if 'Oro' in asset or 'BTC' in asset else 100000
                dist_sl = abs(entry - sl)
                
                if dist_sl > 0:
                    risk_amount = capitale * (rischio/100)
                    lotti = max(0.01, round(risk_amount / (dist_sl * multiplier), 2))
                else:
                    lotti = 0.01
                
                # Mostra risultati
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("RSI", f"{current_rsi:.1f}")
                with col2: st.metric("ATR", f"{atr:.2f}")
                with col3: st.metric("Range", f"{(high_20-low_20):.2f}")
                
                st.markdown(f"""
                <div class='price-box'>
                    <div class='{signal}'>{signal}</div>
                    <div class='price'>{current_price:.2f}</div>
                    <div style='color:#888'>{asset}</div>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(3)
                with cols[0]: st.markdown(f"<div class='metric'><b>ENTRY</b><br>{entry:.2f}</div>", unsafe_allow_html=True)
                with cols[1]: st.markdown(f"<div class='metric'><b>TP</b><br>{tp:.2f}</div>", unsafe_allow_html=True)
                with cols[2]: st.markdown(f"<div class='metric'><b>SL</b><br>{sl:.2f}</div>", unsafe_allow_html=True)
                
                cols = st.columns(3)
                with cols[0]: st.metric("Lotti", f"{lotti:.2f}")
                with cols[1]: st.metric("Rischio €", f"{lotti * dist_sl * multiplier:.2f}")
                with cols[2]: 
                    rr = abs((tp-entry)/(sl-entry)) if sl != entry else 1
                    st.metric("R/R", f"{rr:.2f}")
                
                # Grafico
                fig = go.Figure()
                
                # Candele
                dates = data.index[-50:]
                opens = data['Open'].iloc[-50:].values if not isinstance(data['Open'], pd.DataFrame) else data['Open'].iloc[-50:,0].values
                highs = data['High'].iloc[-50:].values if not isinstance(data['High'], pd.DataFrame) else data['High'].iloc[-50:,0].values
                lows = data['Low'].iloc[-50:].values if not isinstance(data['Low'], pd.DataFrame) else data['Low'].iloc[-50:,0].values
                closes = data['Close'].iloc[-50:].values if not isinstance(data['Close'], pd.DataFrame) else data['Close'].iloc[-50:,0].values
                
                fig.add_trace(go.Candlestick(
                    x=dates,
                    open=opens,
                    high=highs,
                    low=lows,
                    close=closes,
                    increasing_line_color='#00ff00',
                    decreasing_line_color='#ff4444'
                ))
                
                fig.add_hline(y=entry, line_color='cyan', line_width=2, annotation_text=f'Entry {entry:.2f}')
                fig.add_hline(y=tp, line_color='lime', line_dash='dash', annotation_text=f'TP {tp:.2f}')
                fig.add_hline(y=sl, line_color='red', line_dash='dash', annotation_text=f'SL {sl:.2f}')
                
                fig.update_layout(
                    template='plotly_dark',
                    height=400,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.success(f"? Aggiornato: {datetime.now().strftime('%H:%M:%S')}")
                
            else:
                st.error("? Nessun dato disponibile")
                
        except Exception as e:
            st.error(f"? Errore: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#666; font-size:12px;'>?? Disclaimer: Tool informativo - Verifica sempre prima di tradare</p>", unsafe_allow_html=True)