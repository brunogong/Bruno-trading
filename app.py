"""
TRADING TERMINAL PRO - Versione Completa
✅ Timeframe selezionabile
✅ Tutti gli asset principali
✅ Testo leggibile
✅ Design professionale
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz

# Configurazione pagina
st.set_page_config(
    page_title="Trading Terminal Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS MIGLIORATO - Testo più leggibile
st.markdown("""
<style>
    /* Reset e font */
    .stApp {
        background-color: #0d1117;
    }
    
    /* Testo principale - BIANCO per leggibilità */
    p, li, span, div:not(.stMarkdown) {
        color: #ffffff !important;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #1a1f2e, #0d1117);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 5px solid #00ff00;
        box-shadow: 0 4px 12px rgba(0,255,0,0.1);
    }
    
    .header h1 {
        color: #00ff00 !important;
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }
    
    .header p {
        color: #cccccc !important;
        font-size: 14px;
        margin-top: 5px;
    }
    
    /* Price Card */
    .price-card {
        background: #000000;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #00ff00;
        margin: 20px 0;
        box-shadow: 0 0 20px rgba(0,255,0,0.2);
    }
    
    .price-value {
        font-size: 56px;
        color: #00ff00 !important;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        line-height: 1.2;
    }
    
    .signal-buy {
        color: #00ff00 !important;
        font-size: 28px;
        font-weight: bold;
        background: rgba(0,255,0,0.1);
        padding: 5px 20px;
        border-radius: 30px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    .signal-sell {
        color: #ff4444 !important;
        font-size: 28px;
        font-weight: bold;
        background: rgba(255,68,68,0.1);
        padding: 5px 20px;
        border-radius: 30px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* Metric Cards - Migliorato contrasto */
    .metric-card {
        background: #1a1f2e;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #333;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #00ff00;
    }
    
    .metric-label {
        color: #aaaaaa !important;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #00ff00 !important;
        font-size: 28px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    /* Level Cards */
    .level-card {
        background: #1a1f2e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #333;
    }
    
    .level-label {
        color: #aaaaaa !important;
        font-size: 12px;
        margin-bottom: 5px;
    }
    
    .entry-value {
        color: #00ccff !important;
        font-size: 20px;
        font-weight: bold;
    }
    
    .tp-value {
        color: #00ff00 !important;
        font-size: 20px;
        font-weight: bold;
    }
    
    .sl-value {
        color: #ff4444 !important;
        font-size: 20px;
        font-weight: bold;
    }
    
    /* Sidebar - Migliorato */
    .css-1d391kg, .css-1wrcr25 {
        background-color: #1a1f2e;
    }
    
    .stSelectbox label, .stNumberInput label, .stSlider label {
        color: #00ff00 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        height: 55px;
        background: linear-gradient(90deg, #00ff00, #00cc00);
        color: #000000 !important;
        font-weight: bold;
        font-size: 18px;
        border-radius: 30px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,255,0,0.3);
        margin: 20px 0;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0,255,0,0.4);
    }
    
    /* Info text */
    .info-text {
        color: #cccccc !important;
        font-size: 14px;
        margin: 10px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666666 !important;
        font-size: 12px;
        padding: 20px;
        border-top: 1px solid #333;
        margin-top: 40px;
    }
    
    /* DataFrame */
    .dataframe {
        color: #ffffff !important;
    }
    
    .dataframe th {
        color: #00ff00 !important;
        background-color: #1a1f2e !important;
    }
    
    .dataframe td {
        color: #ffffff !important;
        background-color: #0d1117 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>📊 TRADING TERMINAL PRO</h1>
    <p>Analisi Multi-Asset in Tempo Reale | 10+ Asset • 4 Timeframe • Money Management</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Controlli
with st.sidebar:
    st.markdown("### ⚙️ CONTROLLI AVANZATI")
    st.markdown("---")
    
    # ASSET - Completi
    st.markdown("#### 📈 SELEZIONA ASSET")
    asset_categories = {
        "💵 FOREX": {
            "EUR/USD": "EURUSD=X",
            "GBP/USD": "GBPUSD=X",
            "USD/JPY": "USDJPY=X",
            "AUD/USD": "AUDUSD=X",
            "USD/CAD": "USDCAD=X",
            "NZD/USD": "NZDUSD=X",
            "USD/CHF": "USDCHF=X",
            "EUR/GBP": "EURGBP=X"
        },
        "🏅 COMMODITIES": {
            "XAU/USD (Oro)": "GC=F",
            "XAG/USD (Argento)": "SI=F",
            "WTI Crude Oil": "CL=F",
            "Brent Oil": "BZ=F",
            "Natural Gas": "NG=F",
            "Copper": "HG=F"
        },
        "₿ CRYPTO": {
            "BTC/USD (Bitcoin)": "BTC-USD",
            "ETH/USD (Ethereum)": "ETH-USD",
            "BNB/USD": "BNB-USD",
            "SOL/USD": "SOL-USD",
            "ADA/USD": "ADA-USD",
            "DOGE/USD": "DOGE-USD"
        },
        "📊 INDICI": {
            "S&P 500": "^GSPC",
            "Dow Jones": "^DJI",
            "NASDAQ": "^IXIC",
            "DAX (Germania)": "^GDAXI",
            "FTSE (UK)": "^FTSE",
            "Nikkei 225": "^N225",
            "Hang Seng": "^HSI"
        }
    }
    
    # Crea un dizionario piatto per la selezione
    all_assets = {}
    for category, assets in asset_categories.items():
        all_assets.update(assets)
    
    selected_asset = st.selectbox(
        "Asset",
        options=list(all_assets.keys()),
        index=0
    )
    
    # TIMEFRAME - Multipli
    st.markdown("#### ⏱️ TIMEFRAME")
    timeframe = st.selectbox(
        "Timeframe",
        options=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1wk"],
        index=4  # default 1h
    )
    
    # PERIODO
    st.markdown("#### 📅 PERIODO")
    period_map = {
        "1d": "5d",
        "5d": "1mo",
        "1mo": "3mo",
        "3mo": "6mo",
        "6mo": "1y"
    }
    period_options = list(period_map.keys())
    selected_period = st.selectbox(
        "Periodo storico",
        options=period_options,
        index=2  # default 1mo
    )
    
    # MONEY MANAGEMENT
    st.markdown("#### 💰 MONEY MANAGEMENT")
    capitale = st.number_input("Capitale (€)", min_value=100, max_value=1000000, value=1000, step=100)
    rischio = st.slider("Rischio % per trade", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    
    # Pulsante analisi
    analyze_btn = st.button("🚀 ANALIZZA ORA", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-text">
        📌 <b>INFO:</b><br>
        • Dati in tempo reale da Yahoo Finance<br>
        • RSI e ATR calcolati automaticamente<br>
        • Livelli Fibonacci 0.382<br>
        • Money management integrato
    </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT
if analyze_btn:
    with st.spinner("📥 Scaricamento dati in corso..."):
        try:
            symbol = all_assets[selected_asset]
            
            # Download dati
            data = yf.download(
                symbol,
                period=selected_period,
                interval=timeframe,
                auto_adjust=True,
                progress=False
            )
            
            if data.empty:
                st.error("❌ Nessun dato disponibile per questo asset/timeframe")
                st.stop()
            
            # Prezzo attuale
            if isinstance(data['Close'], pd.DataFrame):
                current_price = float(data['Close'].iloc[-1, 0])
                high_20 = float(data['High'].tail(20).max().iloc[0])
                low_20 = float(data['Low'].tail(20).min().iloc[0])
                volume = float(data['Volume'].iloc[-1, 0]) if 'Volume' in data.columns else 0
            else:
                current_price = float(data['Close'].iloc[-1])
                high_20 = float(data['High'].tail(20).max())
                low_20 = float(data['Low'].tail(20).min())
                volume = float(data['Volume'].iloc[-1]) if 'Volume' in data.columns else 0
            
            # Calcolo RSI
            close_series = data['Close'].iloc[:,0] if isinstance(data['Close'], pd.DataFrame) else data['Close']
            delta = close_series.diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0
            
            # Calcolo ATR
            high_series = data['High'].iloc[:,0] if isinstance(data['High'], pd.DataFrame) else data['High']
            low_series = data['Low'].iloc[:,0] if isinstance(data['Low'], pd.DataFrame) else data['Low']
            close_series_atr = data['Close'].iloc[:,0] if isinstance(data['Close'], pd.DataFrame) else data['Close']
            
            high_low = high_series - low_series
            high_close = abs(high_series - close_series_atr.shift(1))
            low_close = abs(low_series - close_series_atr.shift(1))
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = float(tr.tail(14).mean())
            
            # Genera segnale
            if current_rsi > 50:
                signal_class = "signal-buy"
                entry = low_20 + (high_20 - low_20) * 0.382
                sl = entry - (atr * 1.5)
                tp = entry + (atr * 2)
            else:
                signal_class = "signal-sell"
                entry = high_20 - (high_20 - low_20) * 0.382
                sl = entry + (atr * 1.5)
                tp = entry - (atr * 2)
            
            # Calcolo lotti
            if any(x in selected_asset for x in ['Oro', 'Argento', 'BTC', 'ETH']):
                multiplier = 100
            elif any(x in selected_asset for x in ['JPY']):
                multiplier = 1000
            else:
                multiplier = 100000
            
            dist_sl = abs(entry - sl)
            risk_amount = capitale * (rischio / 100)
            lotti = max(0.01, round(risk_amount / (dist_sl * multiplier), 2)) if dist_sl > 0 else 0.01
            
            # R/R Ratio
            rr_ratio = abs((tp - entry) / (sl - entry)) if sl != entry else 1
            
            # METRICHE PRINCIPALI
            st.markdown("### 📊 METRICHE PRINCIPALI")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RSI (14)</div>
                    <div class="metric-value">{current_rsi:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">ATR (14)</div>
                    <div class="metric-value">{atr:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">VOLUME</div>
                    <div class="metric-value">{volume:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RANGE 20gg</div>
                    <div class="metric-value">{(high_20-low_20):.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # PRICE CARD
            st.markdown(f"""
            <div class="price-card">
                <div class="{signal_class}">{'BUY' if current_rsi > 50 else 'SELL'}</div>
                <div class="price-value">{current_price:,.4f}</div>
                <div style="color: #cccccc !important; margin-top: 10px;">
                    {selected_asset} | {timeframe} | Aggiornato: {datetime.now().strftime('%H:%M:%S')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # LIVELLI TRADING
            st.markdown("### 🎯 LIVELLI OPERATIVI")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">ENTRY</div>
                    <div class="entry-value">{entry:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">TAKE PROFIT</div>
                    <div class="tp-value">{tp:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">STOP LOSS</div>
                    <div class="sl-value">{sl:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # MONEY MANAGEMENT
            st.markdown("### 💰 MONEY MANAGEMENT")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">LOTTI CONSIGLIATI</div>
                    <div class="metric-value">{lotti:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RISCHIO €</div>
                    <div class="metric-value" style="color: #ff4444 !important;">€{lotti * dist_sl * multiplier:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">R/R RATIO</div>
                    <div class="metric-value">{rr_ratio:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # GRAFICO
            st.markdown("### 📈 GRAFICO ANALISI")
            
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3]
            )
            
            # Candele
            dates = data.index[-100:] if len(data) > 100 else data.index
            
            opens = data['Open'].iloc[-100:].values if len(data) > 100 else data['Open'].values
            highs = data['High'].iloc[-100:].values if len(data) > 100 else data['High'].values
            lows = data['Low'].iloc[-100:].values if len(data) > 100 else data['Low'].values
            closes = data['Close'].iloc[-100:].values if len(data) > 100 else data['Close'].values
            
            fig.add_trace(go.Candlestick(
                x=dates,
                open=opens if not isinstance(opens[0], pd.Series) else [x[0] for x in opens],
                high=highs if not isinstance(highs[0], pd.Series) else [x[0] for x in highs],
                low=lows if not isinstance(lows[0], pd.Series) else [x[0] for x in lows],
                close=closes if not isinstance(closes[0], pd.Series) else [x[0] for x in closes],
                name='Prezzo',
                increasing_line_color='#00ff00',
                decreasing_line_color='#ff4444'
            ), row=1, col=1)
            
            # Linee di livello
            fig.add_hline(y=entry, line_color='cyan', line_width=2, 
                         annotation_text=f'Entry {entry:.2f}', row=1, col=1)
            fig.add_hline(y=tp, line_color='lime', line_dash='dash', 
                         annotation_text=f'TP {tp:.2f}', row=1, col=1)
            fig.add_hline(y=sl, line_color='red', line_dash='dash', 
                         annotation_text=f'SL {sl:.2f}', row=1, col=1)
            
            # Volume
            if 'Volume' in data.columns:
                vol_data = data['Volume'].iloc[-100:].values if len(data) > 100 else data['Volume'].values
                if isinstance(vol_data[0], pd.Series):
                    vol_data = [x[0] for x in vol_data]
                
                fig.add_trace(go.Bar(
                    x=dates,
                    y=vol_data,
                    name='Volume',
                    marker_color='#00ff00'
                ), row=2, col=1)
            
            fig.update_layout(
                template='plotly_dark',
                height=600,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='#0d1117',
                plot_bgcolor='#0d1117'
            )
            
            fig.update_xaxes(gridcolor='#333', gridwidth=1)
            fig.update_yaxes(gridcolor='#333', gridwidth=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # SUPPORTO E RESISTENZA
            st.markdown("### 📊 LIVELLI DI SUPPORTO/RESISTENZA")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">SUPPORTO</div>
                    <div class="entry-value">{low_20:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">RESISTENZA</div>
                    <div class="tp-value">{high_20:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # INFO ASSET
            st.markdown("### ℹ️ INFO ASSET")
            st.markdown(f"""
            <div style="background: #1a1f2e; padding: 15px; border-radius: 10px; border: 1px solid #333;">
                <p><b>📌 Asset:</b> {selected_asset}</p>
                <p><b>⏱️ Timeframe:</b> {timeframe}</p>
                <p><b>📅 Periodo:</b> {selected_period}</p>
                <p><b>💰 Capitale:</b> €{capitale:,.0f}</p>
                <p><b>⚠️ Rischio:</b> {rischio}%</p>
                <p><b>📊 Range 20 periodi:</b> {low_20:,.4f} - {high_20:,.4f}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Errore durante l'analisi: {str(e)}")
            st.exception(e)

else:
    # Schermata iniziale
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px; color: #cccccc;">
        <h2 style="color: #00ff00;">👋 Benvenuto su Trading Terminal Pro</h2>
        <p style="font-size: 18px; margin: 20px 0;">
            Seleziona un asset e i parametri dal menu a sinistra, poi clicca su ANALIZZA ORA
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; margin: 40px 0;">
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">📈 30+</h3>
                <p>Asset disponibili</p>
            </div>
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">⏱️ 8</h3>
                <p>Timeframe</p>
            </div>
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">⚡ Realtime</h3>
                <p>Dati live</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ Disclaimer: Questo è un tool informativo, non un consiglio finanziario. I dati possono subire ritardi.</p>
    <p>© 2024 Trading Terminal Pro | Dati forniti da Yahoo Finance</p>
</div>
""", unsafe_allow_html=True)

