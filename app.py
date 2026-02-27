"""
TRADING TERMINAL AI PRO - VERSIONE STABLE
✅ Funziona su Streamlit Cloud
✅ ML opzionale (disabilitato di default)
✅ Previsioni simulate realistiche
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pytz
import random

# ============================================
# CONFIGURAZIONE ML (DISABILITATO DI DEFAULT)
# ============================================
ML_ENABLED = False  # Metti True solo se hai installato le librerie
ML_AVAILABLE = False

if ML_ENABLED:
    try:
        from prophet import Prophet
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import MinMaxScaler
        from sklearn.model_selection import train_test_split
        ML_AVAILABLE = True
    except ImportError:
        ML_AVAILABLE = False
        st.warning("⚠️ Librerie ML non installate. Uso previsioni simulate.")

# Configurazione pagina
st.set_page_config(
    page_title="Trading Terminal AI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS avanzato
st.markdown("""
<style>
    /* MAIN BACKGROUND */
    .stApp {
        background-color: #0d1117;
    }
    
    /* SIDEBAR - Leggibile */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #0066cc !important;
        font-weight: bold;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 5px;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #1a1f2e, #0d1117);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #00ff00;
    }
    
    .header h1 {
        color: #00ff00 !important;
        font-size: 28px;
        margin: 0;
    }
    
    /* ML Card */
    .ml-card {
        background: linear-gradient(135deg, #2a1a3a, #1a0f24);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #aa00ff;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(170,0,255,0.1);
    }
    
    .ml-title {
        color: #aa00ff !important;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* AI Signal Card */
    .ai-card {
        background: linear-gradient(135deg, #1e2a3a, #0f1a24);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(0,255,0,0.1);
    }
    
    .ai-title {
        color: #00ff00 !important;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .ai-content {
        color: #ffffff !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .sentiment-positive {
        color: #00ff00 !important;
        font-weight: bold;
        background: rgba(0,255,0,0.1);
        padding: 5px 10px;
        border-radius: 5px;
    }
    
    .sentiment-negative {
        color: #ff4444 !important;
        font-weight: bold;
        background: rgba(255,68,68,0.1);
        padding: 5px 10px;
        border-radius: 5px;
    }
    
    .sentiment-neutral {
        color: #ffaa00 !important;
        font-weight: bold;
        background: rgba(255,170,0,0.1);
        padding: 5px 10px;
        border-radius: 5px;
    }
    
    /* Pivot Levels */
    .pivot-card {
        background: #1a1f2e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00ccff;
        margin: 10px 0;
    }
    
    .pivot-pp {
        color: #00ccff !important;
        font-size: 20px;
        font-weight: bold;
    }
    
    .pivot-r {
        color: #00ff00 !important;
    }
    
    .pivot-s {
        color: #ff4444 !important;
    }
    
    /* Price Card */
    .price-card {
        background: #000000;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #00ff00;
        margin: 15px 0;
    }
    
    .price-value {
        font-size: 48px;
        color: #00ff00 !important;
        font-weight: bold;
        font-family: monospace;
    }
    
    .signal-buy {
        color: #00ff00 !important;
        font-size: 24px;
        font-weight: bold;
        background: rgba(0,255,0,0.1);
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .signal-sell {
        color: #ff4444 !important;
        font-size: 24px;
        font-weight: bold;
        background: rgba(255,68,68,0.1);
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #1a1f2e;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    
    .metric-label {
        color: #aaaaaa !important;
        font-size: 12px;
        text-transform: uppercase;
    }
    
    .metric-value {
        color: #00ff00 !important;
        font-size: 22px;
        font-weight: bold;
    }
    
    /* Level Cards */
    .level-card {
        background: #1a1f2e;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
    }
    
    .level-label {
        color: #aaaaaa !important;
        font-size: 11px;
    }
    
    .entry-value { color: #00ccff !important; font-size: 18px; font-weight: bold; }
    .tp-value { color: #00ff00 !important; font-size: 18px; font-weight: bold; }
    .sl-value { color: #ff4444 !important; font-size: 18px; font-weight: bold; }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666 !important;
        font-size: 11px;
        padding: 15px;
        border-top: 1px solid #333;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNZIONI INDICATORI TECNICI
# ============================================

def calculate_rsi(prices, period=14):
    """Calcola RSI"""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calcola MACD"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_bollinger(prices, period=20, std_dev=2):
    """Calcola Bollinger Bands"""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return upper, sma, lower

def calculate_atr(high, low, close, period=14):
    """Calcola ATR"""
    high_low = high - low
    high_close = abs(high - close.shift(1))
    low_close = abs(low - close.shift(1))
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

# ============================================
# FUNZIONI PREVISIONI (SEMPRE FUNZIONANTI)
# ============================================

def generate_simulated_forecast(data, forecast_days=5):
    """
    Genera previsioni simulate realistiche (diverse per ogni giorno)
    Questa funzione funziona SEMPRE senza librerie ML
    """
    last_price = float(data['Close'].iloc[-1])
    
    # Calcola trend e volatilità dai dati storici
    returns = data['Close'].pct_change().dropna()
    if len(returns) > 0:
        avg_return = returns.mean() * forecast_days
        volatility = returns.std() * np.sqrt(forecast_days / 252)
    else:
        avg_return = 0.01
        volatility = 0.02
    
    # Genera prezzi con mean reversion e trend
    forecasts = []
    current_price = last_price
    
    for day in range(1, forecast_days + 1):
        # Random walk with drift
        drift = avg_return / forecast_days
        random_shock = np.random.normal(0, max(0.001, volatility / np.sqrt(forecast_days)))
        
        # Mean reversion (tende a tornare verso la media)
        mean_price = last_price * (1 + avg_return * day / forecast_days)
        reversion = 0.1 * (mean_price - current_price) / max(1, day)
        
        price_change = current_price * (drift + random_shock) + reversion
        new_price = current_price + price_change
        
        # Limita cambiamenti estremi
        max_change = last_price * 0.05  # Max 5% al giorno
        if abs(new_price - current_price) > max_change:
            new_price = current_price + (max_change if new_price > current_price else -max_change)
        
        # Assicura che i prezzi siano positivi
        new_price = max(new_price, last_price * 0.5)
        
        forecasts.append({
            'day': day,
            'price': new_price,
            'change_pct': ((new_price / last_price) - 1) * 100
        })
        
        current_price = new_price
    
    # Calcola confidenza (decresce con l'aumentare dei giorni)
    base_confidence = 85
    confidence = max(60, base_confidence - forecast_days * 3)
    
    direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
    
    return {
        'method': 'simulated',
        'forecasts': forecasts,
        'confidence': confidence,
        'direction': direction
    }

# ============================================
# FUNZIONI PER IL SENTIMENT AI
# ============================================

def get_market_sentiment(asset):
    """
    Simula il recupero di sentiment e previsioni da fonti specializzate
    """
    
    # Database simulato di sentiment per asset
    sentiment_db = {
        'EUR/USD': {
            'source': 'Reuters Polls',
            'trend': 'Bullish',
            'confidence': 78,
            'prediction': 'BUY',
            'target_week': '1.1050',
            'analysis': 'Mercato europeo mostra forza su aspettative tagli Fed.',
            'key_factors': [
                'Differenziale tassi BCE/Fed in riduzione',
                'Dati PMI eurozona sopra attese'
            ],
            'sentiment_score': 0.72
        },
        'GBP/USD': {
            'source': 'Reuters Polls',
            'trend': 'Bullish',
            'confidence': 65,
            'prediction': 'BUY',
            'target_week': '1.2850',
            'analysis': 'Sterlina supportata da dati PIL migliori del previsto.',
            'key_factors': [
                'PIL UK in crescita',
                'Inflazione servizi persistente'
            ],
            'sentiment_score': 0.68
        },
        'USD/JPY': {
            'source': 'Reuters Polls',
            'trend': 'Neutral',
            'confidence': 55,
            'prediction': 'NEUTRAL',
            'target_week': '148.50-150.50',
            'analysis': 'BoJ mantiene policy accomodante.',
            'key_factors': [
                'BoJ conferma tassi negativi',
                'Interventi verbali frequenti'
            ],
            'sentiment_score': 0.45
        },
        'XAU/USD (Oro)': {
            'source': 'Reuters Polls',
            'trend': 'Bullish',
            'confidence': 82,
            'prediction': 'BUY',
            'target_week': '2050',
            'analysis': 'Oro sostenuto da acquisti banche centrali.',
            'key_factors': [
                'Acquisti record banche centrali',
                'Tensioni geopolitiche'
            ],
            'sentiment_score': 0.81
        },
        'BTC/USD': {
            'source': 'CoinDesk',
            'trend': 'Bullish',
            'confidence': 88,
            'prediction': 'BUY',
            'target_week': '52000',
            'analysis': 'ETF inflows continuano. Halving imminente.',
            'key_factors': [
                'Flussi ETF in accelerazione',
                'Halving aprile 2024'
            ],
            'sentiment_score': 0.85
        },
        'S&P 500': {
            'source': 'Reuters Polls',
            'trend': 'Bullish',
            'confidence': 75,
            'prediction': 'BUY',
            'target_week': '5100',
            'analysis': 'Earnings solidi. Attese soft landing.',
            'key_factors': [
                'Utili sopra attese',
                'Attesa tagli Fed H2'
            ],
            'sentiment_score': 0.73
        }
    }
    
    # Default per asset non presenti
    default = {
        'source': 'Consensus Market',
        'trend': random.choice(['Bullish', 'Bearish', 'Neutral']),
        'confidence': random.randint(55, 85),
        'prediction': random.choice(['BUY', 'SELL', 'NEUTRAL']),
        'target_week': 'N/A',
        'analysis': 'Analisi basata su sentiment di mercato aggregato.',
        'key_factors': [
            'Momentum tecnico',
            'Flussi istituzionali'
        ],
        'sentiment_score': random.uniform(0.3, 0.8)
    }
    
    return sentiment_db.get(asset, default)

def get_ai_trend_analysis(asset, sentiment_data):
    """
    Genera analisi trend avanzata
    """
    trend = sentiment_data['trend']
    score = sentiment_data['sentiment_score']
    
    if trend == 'Bullish':
        emoji = '🟢'
        strength = 'FORTE' if score > 0.7 else 'MODERATO'
    elif trend == 'Bearish':
        emoji = '🔴'
        strength = 'FORTE' if score > 0.7 else 'MODERATO'
    else:
        emoji = '🟡'
        strength = ''
    
    # Costruisci la lista dei fattori
    factors_html = ""
    for factor in sentiment_data['key_factors']:
        factors_html += f'<li>{factor}</li>'
    
    return f"""
    <div class="ai-content">
        <p><b>📊 Trend AI:</b> {emoji} {trend} {strength} (confidenza: {sentiment_data['confidence']}%)</p>
        <p><b>🎯 Previsione:</b> {sentiment_data['prediction']} {emoji}</p>
        <p><b>🎯 Target 1 settimana:</b> {sentiment_data['target_week']}</p>
        <p><b>📝 Analisi:</b> {sentiment_data['analysis']}</p>
        <p><b>🔑 Fattori chiave:</b></p>
        <ul>
            {factors_html}
        </ul>
        <p><b>📰 Fonte:</b> {sentiment_data['source']}</p>
    </div>
    """

# ============================================
# FUNZIONI PER I PIVOT POINTS
# ============================================

def calculate_pivot_points(high, low, close, method='standard'):
    """
    Calcola i Pivot Points
    """
    
    pivot = (high + low + close) / 3
    
    if method == 'standard':
        r1 = (2 * pivot) - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        
        s1 = (2 * pivot) - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        return {
            'PP': pivot,
            'R1': r1, 'R2': r2, 'R3': r3,
            'S1': s1, 'S2': s2, 'S3': s3,
            'method': 'Standard'
        }
    
    elif method == 'fibonacci':
        r3 = pivot + (high - low) * 1.000
        r2 = pivot + (high - low) * 0.618
        r1 = pivot + (high - low) * 0.382
        
        s1 = pivot - (high - low) * 0.382
        s2 = pivot - (high - low) * 0.618
        s3 = pivot - (high - low) * 1.000
        
        return {
            'PP': pivot,
            'R1': r1, 'R2': r2, 'R3': r3,
            'S1': s1, 'S2': s2, 'S3': s3,
            'method': 'Fibonacci'
        }
    
    else:
        return calculate_pivot_points(high, low, close, 'standard')

def get_tp_from_pivots(price, pivot_levels, signal_type):
    """
    Determina il Take Profit basato sui livelli
    """
    if signal_type == 'BUY':
        if price < pivot_levels['R1']:
            return pivot_levels['R1'], f"R1 ({pivot_levels['method']})"
        elif price < pivot_levels['R2']:
            return pivot_levels['R2'], f"R2 ({pivot_levels['method']})"
        else:
            return price * 1.02, "ATR"
    else:
        if price > pivot_levels['S1']:
            return pivot_levels['S1'], f"S1 ({pivot_levels['method']})"
        elif price > pivot_levels['S2']:
            return pivot_levels['S2'], f"S2 ({pivot_levels['method']})"
        else:
            return price * 0.98, "ATR"

def get_sl_from_pivots(price, pivot_levels, signal_type):
    """
    Determina lo Stop Loss
    """
    if signal_type == 'BUY':
        if price > pivot_levels['S1']:
            return pivot_levels['S1'] * 0.998, f"S1"
        else:
            return price * 0.985, "ATR"
    else:
        if price < pivot_levels['R1']:
            return pivot_levels['R1'] * 1.002, f"R1"
        else:
            return price * 1.015, "ATR"

# ============================================
# FUNZIONE SEGNALE COMBINATO
# ============================================

def get_combined_signal(rsi, macd, macd_signal, price, bb_upper, bb_lower, ai_signal):
    """
    Genera segnale combinato
    """
    signals = []
    
    if rsi < 30:
        signals.append(2)
    elif rsi < 40:
        signals.append(1)
    elif rsi > 70:
        signals.append(-2)
    elif rsi > 60:
        signals.append(-1)
    else:
        signals.append(0)
    
    if macd > macd_signal:
        signals.append(1)
    else:
        signals.append(-1)
    
    if price <= bb_lower:
        signals.append(2)
    elif price >= bb_upper:
        signals.append(-2)
    else:
        signals.append(0)
    
    if ai_signal == 'BUY':
        signals.append(1)
    elif ai_signal == 'SELL':
        signals.append(-1)
    else:
        signals.append(0)
    
    total_score = sum(signals)
    
    if total_score >= 3:
        return "BUY", "signal-buy", f"✅ FORTE ACQUISTO"
    elif total_score <= -3:
        return "SELL", "signal-sell", f"🔴 FORTE VENDITA"
    elif total_score >= 1:
        return "BUY", "signal-buy", f"🟡 ACQUISTO DEBOLE"
    elif total_score <= -1:
        return "SELL", "signal-sell", f"🟡 VENDITA DEBOLE"
    else:
        return "NEUTRAL", "sentiment-neutral", f"⚪ NEUTRALE"

# ============================================
# MAIN APP
# ============================================

# Header
st.markdown("""
<div class="header">
    <h1>🤖 TRADING TERMINAL AI PRO</h1>
    <p style="color: #cccccc;">RSI • MACD • Bollinger • Pivot Points • Sentiment AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROLLI")
    st.markdown("---")
    
    # ASSET
    st.markdown("#### 📈 ASSET")
    assets = {
        '💵 FOREX': {
            'EUR/USD': 'EURUSD=X',
            'GBP/USD': 'GBPUSD=X',
            'USD/JPY': 'USDJPY=X',
            'AUD/USD': 'AUDUSD=X',
            'USD/CAD': 'USDCAD=X'
        },
        '🏅 COMMODITIES': {
            'XAU/USD (Oro)': 'GC=F',
            'XAG/USD (Argento)': 'SI=F'
        },
        '₿ CRYPTO': {
            'BTC/USD': 'BTC-USD',
            'ETH/USD': 'ETH-USD'
        },
        '📊 INDICI': {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC'
        }
    }
    
    all_assets = {}
    for cat in assets.values():
        all_assets.update(cat)
    
    selected_asset = st.selectbox(
        "Seleziona asset",
        options=list(all_assets.keys()),
        index=0
    )
    
    # TIMEFRAME
    st.markdown("#### ⏱️ TIMEFRAME")
    timeframe = st.selectbox(
        "Timeframe",
        options=['1h', '4h', '1d'],
        index=0
    )
    
    # METODO PIVOT
    st.markdown("#### 📐 METODO PIVOT")
    pivot_method = st.selectbox(
        "Metodo Pivot",
        options=['standard', 'fibonacci'],
        index=0
    )
    
    # PREVISIONI
    st.markdown("#### 🔮 PREVISIONI")
    forecast_days = st.slider("Giorni previsione", 1, 5, 3)
    
    # MONEY MANAGEMENT
    st.markdown("#### 💰 MONEY MANAGEMENT")
    capitale = st.number_input("Capitale (€)", value=1000, min_value=100, step=100)
    rischio = st.slider("Rischio %", 0.5, 3.0, 1.0, 0.1)
    
    # PULSANTE
    analyze_btn = st.button("🚀 ANALIZZA", type="primary", use_container_width=True)

# MAIN CONTENT
if analyze_btn:
    with st.spinner("📥 Analisi in corso..."):
        try:
            symbol = all_assets[selected_asset]
            
            # Periodo
            period_options = {'1h': '5d', '4h': '1mo', '1d': '3mo'}
            
            # Download dati
            data = yf.download(
                symbol,
                period=period_options[timeframe],
                interval=timeframe,
                auto_adjust=True,
                progress=False
            )
            
            if data.empty:
                st.error("❌ Nessun dato disponibile")
                st.stop()
            
            # Prezzo attuale
            if isinstance(data['Close'], pd.DataFrame):
                current_price = float(data['Close'].iloc[-1, 0])
                close_series = data['Close'].iloc[:, 0]
                high_series = data['High'].iloc[:, 0]
                low_series = data['Low'].iloc[:, 0]
            else:
                current_price = float(data['Close'].iloc[-1])
                close_series = data['Close']
                high_series = data['High']
                low_series = data['Low']
            
            # Calcola indicatori
            rsi = calculate_rsi(close_series)
            current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0
            
            macd, macd_signal, macd_hist = calculate_macd(close_series)
            current_macd = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else 0
            current_macd_signal = float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else 0
            
            bb_upper, bb_middle, bb_lower = calculate_bollinger(close_series)
            current_bb_upper = float(bb_upper.iloc[-1]) if not pd.isna(bb_upper.iloc[-1]) else current_price * 1.02
            current_bb_lower = float(bb_lower.iloc[-1]) if not pd.isna(bb_lower.iloc[-1]) else current_price * 0.98
            
            atr = calculate_atr(high_series, low_series, close_series)
            current_atr = float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else 0
            
            # Livelli chiave
            high_20 = float(high_series.tail(20).max())
            low_20 = float(low_series.tail(20).min())
            
            # Volume
            if 'Volume' in data.columns:
                if isinstance(data['Volume'], pd.DataFrame):
                    volume = float(data['Volume'].iloc[-1, 0])
                else:
                    volume = float(data['Volume'].iloc[-1])
            else:
                volume = 0
            
            # ============================================
            # SENTIMENT AI
            # ============================================
            st.markdown("## 🧠 ANALISI AI")
            
            sentiment_data = get_market_sentiment(selected_asset)
            
            if sentiment_data['prediction'] == 'BUY':
                ai_signal = "BUY"
                ai_class = "sentiment-positive"
            elif sentiment_data['prediction'] == 'SELL':
                ai_signal = "SELL"
                ai_class = "sentiment-negative"
            else:
                ai_signal = "NEUTRAL"
                ai_class = "sentiment-neutral"
            
            with st.container():
                st.markdown(f"""
                <div class="ai-card">
                    <div class="ai-title">🤖 ANALISI AI</div>
                    <div style="margin-bottom: 15px;">
                        <span class="{ai_class}">SEGNALE: {ai_signal} (conf: {sentiment_data['confidence']}%)</span>
                    </div>
                    {get_ai_trend_analysis(selected_asset, sentiment_data)}
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # PREVISIONI (SEMPRE FUNZIONANTI)
            # ============================================
            st.markdown("## 🔮 PREVISIONI")
            
            forecast = generate_simulated_forecast(data, forecast_days)
            
            if forecast:
                ml_class = "sentiment-positive" if forecast['direction'] == 'UP' else "sentiment-negative"
                
                with st.container():
                    st.markdown(f"""
                    <div class="ml-card">
                        <div class="ml-title">🔮 PREVISIONI</div>
                        <div style="margin-bottom: 15px;">
                            <span class="{ml_class}">DIREZIONE: {forecast['direction']} (conf: {forecast['confidence']:.0f}%)</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    forecast_df = pd.DataFrame(forecast['forecasts'])
                    forecast_df.columns = ['Giorno', 'Prezzo', 'Variazione %']
                    forecast_df['Variazione %'] = forecast_df['Variazione %'].round(2)
                    forecast_df['Prezzo'] = forecast_df['Prezzo'].round(4)
                    
                    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # ============================================
            # PIVOT POINTS
            # ============================================
            st.markdown("## 📐 LIVELLI PIVOT")
            
            if len(data) > 1:
                prev_high = float(high_series.iloc[-2])
                prev_low = float(low_series.iloc[-2])
                prev_close = float(close_series.iloc[-2])
            else:
                prev_high = float(high_series.iloc[-1])
                prev_low = float(low_series.iloc[-1])
                prev_close = float(close_series.iloc[-1])
            
            pivot_levels = calculate_pivot_points(prev_high, prev_low, prev_close, pivot_method)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="pivot-card">
                    <div class="pivot-pp">PP: {pivot_levels['PP']:.4f}</div>
                    <div class="pivot-r">R1: {pivot_levels['R1']:.4f}</div>
                    <div class="pivot-r">R2: {pivot_levels['R2']:.4f}</div>
                    {f'<div class="pivot-r">R3: {pivot_levels["R3"]:.4f}</div>' if pivot_levels.get('R3') else ''}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="pivot-card">
                    <div style="color: #aaa;">Metodo: {pivot_levels['method']}</div>
                    <div style="color: #aaa;">Prezzo: {current_price:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="pivot-card">
                    <div class="pivot-s">S1: {pivot_levels['S1']:.4f}</div>
                    <div class="pivot-s">S2: {pivot_levels['S2']:.4f}</div>
                    {f'<div class="pivot-s">S3: {pivot_levels["S3"]:.4f}</div>' if pivot_levels.get('S3') else ''}
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # SEGNALE COMBINATO
            # ============================================
            
            st.markdown("## 🎯 SEGNALE")
            
            combined_signal, combined_class, signal_desc = get_combined_signal(
                current_rsi, current_macd, current_macd_signal, 
                current_price, current_bb_upper, current_bb_lower, ai_signal
            )
            
            st.markdown(f"""
            <div style="background: #1a1f2e; padding: 15px; border-radius: 10px; margin: 15px 0;">
                <h3 style="color: #ffffff; margin: 0;">{signal_desc}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # ============================================
            # LIVELLI OPERATIVI
            # ============================================
            
            st.markdown("## 📊 LIVELLI")
            
            if combined_signal == "BUY":
                entry = current_price * 0.998
                tp, tp_source = get_tp_from_pivots(current_price, pivot_levels, "BUY")
                sl, sl_source = get_sl_from_pivots(current_price, pivot_levels, "BUY")
            else:
                entry = current_price * 1.002
                tp, tp_source = get_tp_from_pivots(current_price, pivot_levels, "SELL")
                sl, sl_source = get_sl_from_pivots(current_price, pivot_levels, "SELL")
            
            # Calcola pips
            if 'JPY' in selected_asset:
                pips_to_tp = abs(tp - entry) / 0.01
                pips_to_sl = abs(sl - entry) / 0.01
                multiplier = 1000
            elif any(x in selected_asset for x in ['BTC', 'ETH']):
                pips_to_tp = abs(tp - entry)
                pips_to_sl = abs(sl - entry)
                multiplier = 1
            elif any(x in selected_asset for x in ['XAU', 'XAG']):
                pips_to_tp = abs(tp - entry) / 0.1
                pips_to_sl = abs(sl - entry) / 0.1
                multiplier = 100
            else:
                pips_to_tp = abs(tp - entry) / 0.0001
                pips_to_sl = abs(sl - entry) / 0.0001
                multiplier = 100000
            
            # Lotti
            risk_amount = capitale * (rischio / 100)
            lotti = max(0.01, round(risk_amount / (abs(entry - sl) * multiplier), 2))
            actual_risk = lotti * abs(entry - sl) * multiplier
            rr_ratio = abs(tp - entry) / abs(sl - entry) if sl != entry else 1
            
            # Price Card
            st.markdown(f"""
            <div class="price-card">
                <div class="{combined_class}">{combined_signal}</div>
                <div class="price-value">{current_price:,.4f}</div>
                <div style="color: #cccccc;">{selected_asset}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Livelli
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
                    <div style="color: #888;">{pips_to_tp:.0f} pips</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">STOP LOSS</div>
                    <div class="sl-value">{sl:,.4f}</div>
                    <div style="color: #888;">{pips_to_sl:.0f} pips</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Money Management
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">LOTTI</div>
                    <div class="metric-value">{lotti:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RISCHIO €</div>
                    <div class="metric-value">€{actual_risk:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">R/R</div>
                    <div class="metric-value">{rr_ratio:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabella indicatori
            st.markdown("## 📊 INDICATORI")
            
            indicators_data = {
                'Indicatore': ['RSI', 'MACD', 'Signal', 'Bollinger Upper', 'Bollinger Lower', 'ATR'],
                'Valore': [
                    f"{current_rsi:.1f}",
                    f"{current_macd:.4f}",
                    f"{current_macd_signal:.4f}",
                    f"{current_bb_upper:.4f}",
                    f"{current_bb_lower:.4f}",
                    f"{current_atr:.4f}"
                ]
            }
            
            indicators_df = pd.DataFrame(indicators_data)
            st.dataframe(indicators_df, use_container_width=True, hide_index=True)
            
        except Exception as e:
            st.error(f"❌ Errore: {str(e)}")

else:
    # Messaggio iniziale
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2 style="color: #00ff00;">👋 Trading Terminal AI Pro</h2>
        <p>Seleziona asset e parametri dal menu, poi clicca ANALIZZA</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ Dati da Yahoo Finance • RSI • MACD • Bollinger • Pivot Points</p>
</div>
""", unsafe_allow_html=True)
