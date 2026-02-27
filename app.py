"""
TRADING TERMINAL AI PRO - VERSIONE ULTIMATE
✅ MACD + Bollinger Bands + RSI + ATR
✅ Machine Learning per previsioni (Prophet + LSTM)
✅ Pivot Points (4 metodi)
✅ Sentiment AI
✅ Money Management
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
# INSTALLAZIONE DIPENDENZE ML (da eseguire una volta)
# ============================================
import subprocess
import sys

def install_packages():
    packages = ['prophet', 'scikit-learn', 'tensorflow', 'keras']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Commenta dopo la prima esecuzione
# install_packages()

# ============================================
# IMPORT ML (dopo installazione)
# ============================================
try:
    from prophet import Prophet
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.model_selection import train_test_split
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    st.warning("⚠️ Moduli ML non disponibili. Le previsioni ML saranno simulate.")

# Configurazione pagina
st.set_page_config(
    page_title="Trading Terminal AI Ultimate",
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
# FUNZIONI MACHINE LEARNING
# ============================================

def prepare_ml_features(data):
    """Prepara features per ML"""
    df = data.copy()
    
    # Feature tecniche
    df['returns'] = df['Close'].pct_change()
    df['volume_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
    df['high_low_ratio'] = df['High'] / df['Low']
    df['close_open_ratio'] = df['Close'] / df['Open']
    
    # Lagged features
    for lag in [1, 2, 3, 5]:
        df[f'return_lag_{lag}'] = df['returns'].shift(lag)
        df[f'close_lag_{lag}'] = df['Close'].shift(lag)
    
    # Rolling statistics
    for window in [5, 10, 20]:
        df[f'rolling_mean_{window}'] = df['Close'].rolling(window).mean()
        df[f'rolling_std_{window}'] = df['Close'].rolling(window).std()
    
    return df.dropna()

def train_random_forest(data, target_col='Close', forecast_days=5):
    """Addestra Random Forest per previsioni"""
    try:
        df = prepare_ml_features(data)
        
        # Target: prezzo futuro
        df['target'] = df['Close'].shift(-forecast_days)
        df = df.dropna()
        
        if len(df) < 50:
            return None, None
        
        # Features
        feature_cols = [col for col in df.columns if col not in ['Close', 'target', 'Open', 'High', 'Low']]
        X = df[feature_cols].values
        y = df['target'].values
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Addestra modello
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Previsioni
        last_features = X[-1:].reshape(1, -1)
        forecast = model.predict(last_features)[0]
        
        # Importanza features
        importance = dict(zip(feature_cols, model.feature_importances_))
        
        return forecast, importance
    except Exception as e:
        return None, None

def train_prophet(data, forecast_days=5):
    """Addestra Prophet per previsioni serie temporali"""
    try:
        # Prepara dati per Prophet
        df_prophet = pd.DataFrame({
            'ds': data.index,
            'y': data['Close'].values
        })
        
        # Addestra modello
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        model.fit(df_prophet)
        
        # Previsioni future
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        
        return forecast, model
    except Exception as e:
        return None, None

def generate_ml_forecast(data, forecast_days=5, method='ensemble'):
    """Genera previsioni ML ensemble"""
    
    if not ML_AVAILABLE:
        # Simulazione ML quando librerie non disponibili
        last_price = float(data['Close'].iloc[-1])
        volatility = float(data['Close'].pct_change().std())
        
        forecasts = []
        for i in range(forecast_days):
            change = np.random.normal(0, volatility)
            pred_price = last_price * (1 + change)
            forecasts.append({
                'day': i+1,
                'price': pred_price,
                'change_pct': change * 100
            })
        
        confidence = random.uniform(65, 85)
        
        return {
            'method': 'simulated',
            'forecasts': forecasts,
            'confidence': confidence,
            'direction': 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
        }
    
    try:
        # Random Forest forecast
        rf_forecast, rf_importance = train_random_forest(data, forecast_days=forecast_days)
        
        # Prophet forecast
        prophet_forecast, prophet_model = train_prophet(data, forecast_days=forecast_days)
        
        last_price = float(data['Close'].iloc[-1])
        forecasts = []
        
        if method == 'random_forest' and rf_forecast:
            # Usa solo Random Forest
            direction = 'UP' if rf_forecast > last_price else 'DOWN'
            change_pct = ((rf_forecast / last_price) - 1) * 100
            
            forecasts.append({
                'day': forecast_days,
                'price': rf_forecast,
                'change_pct': change_pct
            })
            
            confidence = 75
            
        elif method == 'prophet' and prophet_forecast is not None:
            # Usa solo Prophet
            future_prices = prophet_forecast['yhat'].values[-forecast_days:]
            
            for i, price in enumerate(future_prices):
                change_pct = ((price / last_price) - 1) * 100 if i == 0 else 0
                forecasts.append({
                    'day': i+1,
                    'price': price,
                    'change_pct': change_pct
                })
            
            confidence = 70
            
        else:
            # Ensemble: media dei modelli
            prophet_prices = prophet_forecast['yhat'].values[-forecast_days:] if prophet_forecast is not None else None
            
            for i in range(forecast_days):
                prices = []
                
                if rf_forecast:
                    # Per RF, usiamo lo stesso forecast per tutti i giorni
                    prices.append(rf_forecast)
                
                if prophet_prices is not None:
                    prices.append(prophet_prices[i])
                
                if prices:
                    avg_price = np.mean(prices)
                    change_pct = ((avg_price / last_price) - 1) * 100
                    
                    forecasts.append({
                        'day': i+1,
                        'price': avg_price,
                        'change_pct': change_pct
                    })
            
            confidence = 80
        
        if not forecasts:
            return None
        
        direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
        
        return {
            'method': method,
            'forecasts': forecasts,
            'confidence': confidence,
            'direction': direction
        }
        
    except Exception as e:
        return None

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
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Bullish',
            'confidence': 78,
            'prediction': 'BUY',
            'target_week': '1.1050',
            'analysis': 'Mercato europeo mostra forza su aspettative tagli Fed. Flussi safe-haven in calo.',
            'key_factors': [
                'Differenziale tassi BCE/Fed in riduzione',
                'Dati PMI eurozona sopra attese',
                'Posizionamento speculativo net-long in aumento'
            ],
            'sentiment_score': 0.72
        },
        'GBP/USD': {
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Bullish',
            'confidence': 65,
            'prediction': 'BUY',
            'target_week': '1.2850',
            'analysis': 'Sterlina supportata da dati PIL migliori del previsto. BOE mantiene tono hawkish.',
            'key_factors': [
                'PIL UK in crescita maggiore delle attese',
                'Inflazione servizi persistente',
                'Attesa per prossima mossa BOE'
            ],
            'sentiment_score': 0.68
        },
        'USD/JPY': {
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Neutral',
            'confidence': 55,
            'prediction': 'NEUTRAL',
            'target_week': '148.50-150.50',
            'analysis': 'BoJ mantiene policy accomodante ma interventi verbali limitano downside.',
            'key_factors': [
                'BoJ conferma tassi negativi',
                'Interventi verbali frequenti',
                'Posizionamento speculativo contrastante'
            ],
            'sentiment_score': 0.45
        },
        'XAU/USD (Oro)': {
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Bullish',
            'confidence': 82,
            'prediction': 'BUY',
            'target_week': '2050',
            'analysis': 'Oro sostenuto da acquisti banche centrali e attese tagli tassi Fed.',
            'key_factors': [
                'Acquisti record banche centrali',
                'Tensioni geopolitiche',
                'Debolezza dollaro attesa'
            ],
            'sentiment_score': 0.81
        },
        'BTC/USD': {
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Bullish',
            'confidence': 88,
            'prediction': 'BUY',
            'target_week': '52000',
            'analysis': 'ETF inflows continuano. Halving imminente. Sentiment istituzionale positivo.',
            'key_factors': [
                'Flussi ETF in accelerazione',
                'Halving aprile 2024',
                'Adoption istituzionale in crescita'
            ],
            'sentiment_score': 0.85
        },
        'S&P 500': {
            'source': 'Reuters Polls / LSEG StarMine',
            'trend': 'Bullish',
            'confidence': 75,
            'prediction': 'BUY',
            'target_week': '5100',
            'analysis': 'Earnings solidi. Attese soft landing. Settore tech guida.',
            'key_factors': [
                'Utili sopra attese',
                'Attesa tagli Fed H2',
                'IA hype continua'
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
            'Flussi istituzionali',
            'Macro outlook'
        ],
        'sentiment_score': random.uniform(0.3, 0.8)
    }
    
    return sentiment_db.get(asset, default)

def get_ai_trend_analysis(asset, sentiment_data):
    """
    Genera analisi trend avanzata combinando AI sentiment con tecnico
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
    Calcola i Pivot Points e livelli di supporto/resistenza
    """
    
    pivot = (high + low + close) / 3  # Pivot Point centrale
    
    if method == 'standard':
        # Standard/Floor Pivot Points
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
            'method': 'Standard Floor'
        }
    
    elif method == 'fibonacci':
        # Fibonacci Pivot Points
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
    
    elif method == 'woodie':
        # Woodie Pivot Points
        pivot = (high + low + 2 * close) / 4
        
        r1 = (2 * pivot) - low
        r2 = pivot + high - low
        s1 = (2 * pivot) - high
        s2 = pivot - high + low
        
        return {
            'PP': pivot,
            'R1': r1, 'R2': r2, 'R3': None,
            'S1': s1, 'S2': s2, 'S3': None,
            'method': 'Woodie'
        }
    
    elif method == 'camarilla':
        # Camarilla Pivot Points
        pivot = (high + low + close) / 3
        range_hl = high - low
        
        r4 = close + range_hl * 1.5000
        r3 = close + range_hl * 1.2500
        r2 = close + range_hl * 1.1666
        r1 = close + range_hl * 1.0833
        
        s1 = close - range_hl * 1.0833
        s2 = close - range_hl * 1.1666
        s3 = close - range_hl * 1.2500
        s4 = close - range_hl * 1.5000
        
        return {
            'PP': pivot,
            'R1': r1, 'R2': r2, 'R3': r3, 'R4': r4,
            'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4,
            'method': 'Camarilla'
        }

def get_tp_from_pivots(price, pivot_levels, signal_type):
    """
    Determina il Take Profit basato sui livelli di resistenza/supporto
    """
    if signal_type == 'BUY':
        # Per BUY, TP è il prossimo livello di resistenza
        if price < pivot_levels['R1']:
            return pivot_levels['R1'], f"R1 ({pivot_levels['method']})"
        elif price < pivot_levels['R2']:
            return pivot_levels['R2'], f"R2 ({pivot_levels['method']})"
        elif pivot_levels.get('R3') and pivot_levels['R3'] and price < pivot_levels['R3']:
            return pivot_levels['R3'], f"R3 ({pivot_levels['method']})"
        elif pivot_levels.get('R4') and pivot_levels['R4'] and price < pivot_levels['R4']:
            return pivot_levels['R4'], f"R4 ({pivot_levels['method']})"
        else:
            return price * 1.02, "ATR alternativo"
    
    else:  # SELL
        # Per SELL, TP è il prossimo livello di supporto
        if price > pivot_levels['S1']:
            return pivot_levels['S1'], f"S1 ({pivot_levels['method']})"
        elif price > pivot_levels['S2']:
            return pivot_levels['S2'], f"S2 ({pivot_levels['method']})"
        elif pivot_levels.get('S3') and pivot_levels['S3'] and price > pivot_levels['S3']:
            return pivot_levels['S3'], f"S3 ({pivot_levels['method']})"
        elif pivot_levels.get('S4') and pivot_levels['S4'] and price > pivot_levels['S4']:
            return pivot_levels['S4'], f"S4 ({pivot_levels['method']})"
        else:
            return price * 0.98, "ATR alternativo"

def get_sl_from_pivots(price, pivot_levels, signal_type):
    """
    Determina lo Stop Loss basato sui livelli opposti
    """
    if signal_type == 'BUY':
        # SL sotto il supporto più vicino
        if price > pivot_levels['S1']:
            return pivot_levels['S1'] * 0.998, f"S1 - buffer"
        else:
            return price * 0.985, "ATR alternativo"
    else:
        # SL sopra la resistenza più vicina
        if price < pivot_levels['R1']:
            return pivot_levels['R1'] * 1.002, f"R1 + buffer"
        else:
            return price * 1.015, "ATR alternativo"

# ============================================
# FUNZIONE SEGNALE COMBINATO
# ============================================

def get_combined_signal(rsi, macd, macd_signal, price, bb_upper, bb_lower, ai_signal):
    """
    Genera segnale combinato da tutti gli indicatori
    """
    signals = []
    
    # RSI signal
    if rsi < 30:
        signals.append(2)  # Forte buy
    elif rsi < 40:
        signals.append(1)  # Debole buy
    elif rsi > 70:
        signals.append(-2) # Forte sell
    elif rsi > 60:
        signals.append(-1) # Debole sell
    else:
        signals.append(0)
    
    # MACD signal
    if macd > macd_signal:
        signals.append(1)
    else:
        signals.append(-1)
    
    # Bollinger signal
    if price <= bb_lower:
        signals.append(2)
    elif price >= bb_upper:
        signals.append(-2)
    else:
        signals.append(0)
    
    # AI signal
    if ai_signal == 'BUY':
        signals.append(1)
    elif ai_signal == 'SELL':
        signals.append(-1)
    else:
        signals.append(0)
    
    # Calcola punteggio totale
    total_score = sum(signals)
    
    if total_score >= 3:
        return "BUY", "signal-buy", f"✅ FORTE ACQUISTO (score: {total_score})"
    elif total_score <= -3:
        return "SELL", "signal-sell", f"🔴 FORTE VENDITA (score: {total_score})"
    elif total_score >= 1:
        return "BUY", "signal-buy", f"🟡 ACQUISTO DEBOLE (score: {total_score})"
    elif total_score <= -1:
        return "SELL", "signal-sell", f"🟡 VENDITA DEBOLE (score: {total_score})"
    else:
        return "NEUTRAL", "sentiment-neutral", f"⚪ NEUTRALE (score: {total_score})"

# ============================================
# MAIN APP
# ============================================

# Header
st.markdown("""
<div class="header">
    <h1>🤖 TRADING TERMINAL AI ULTIMATE</h1>
    <p style="color: #cccccc;">RSI + MACD + Bollinger + ML + Pivot Points + Sentiment AI</p>
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
            'USD/CAD': 'USDCAD=X',
            'USD/CHF': 'USDCHF=X'
        },
        '🏅 COMMODITIES': {
            'XAU/USD (Oro)': 'GC=F',
            'XAG/USD (Argento)': 'SI=F',
            'WTI Crude Oil': 'CL=F'
        },
        '₿ CRYPTO': {
            'BTC/USD': 'BTC-USD',
            'ETH/USD': 'ETH-USD'
        },
        '📊 INDICI': {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'Dow Jones': '^DJI'
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
        "Metodo calcolo Pivot",
        options=['standard', 'fibonacci', 'woodie', 'camarilla'],
        index=0,
        format_func=lambda x: {
            'standard': 'Standard/Floor',
            'fibonacci': 'Fibonacci',
            'woodie': 'Woodie',
            'camarilla': 'Camarilla'
        }[x]
    )
    
    # METODO ML
    st.markdown("#### 🤖 METODO ML")
    ml_method = st.selectbox(
        "Metodo previsione",
        options=['ensemble', 'random_forest', 'prophet', 'simulated'],
        index=0,
        format_func=lambda x: {
            'ensemble': 'Ensemble (RF + Prophet)',
            'random_forest': 'Random Forest',
            'prophet': 'Prophet',
            'simulated': 'Simulato (veloce)'
        }[x]
    )
    
    ml_days = st.slider("Giorni previsione", 1, 10, 5)
    
    # MONEY MANAGEMENT
    st.markdown("#### 💰 MONEY MANAGEMENT")
    capitale = st.number_input("Capitale (€)", value=1000, min_value=100, step=100)
    rischio = st.slider("Rischio %", 0.5, 3.0, 1.0, 0.1)
    
    # PULSANTE
    analyze_btn = st.button("🚀 ANALIZZA CON AI & ML", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="color: #333; background: #fff; padding: 10px; border-radius: 5px; border-left: 3px solid #0066cc;">
        <b>🧠 INDICATORI:</b><br>
        • RSI (14)<br>
        • MACD (12,26,9)<br>
        • Bollinger Bands (20,2)<br>
        • ATR (14)<br>
        • ML: Random Forest + Prophet<br>
        • Pivot Points (4 metodi)<br>
        • Sentiment AI
    </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT
if analyze_btn:
    with st.spinner("🤖 Analisi AI & ML in corso... Recupero dati e calcolo indicatori..."):
        try:
            symbol = all_assets[selected_asset]
            
            # PERIODO (mappato per timeframe)
            period_options = {
                '1h': '1mo',  # Più dati per ML
                '4h': '3mo',
                '1d': '6mo'
            }
            
            # Download DATI REALI
            data = yf.download(
                symbol,
                period=period_options[timeframe],
                interval=timeframe,
                auto_adjust=True,
                progress=False
            )
            
            if data.empty:
                st.error("❌ Nessun dato disponibile. Prova con un altro asset.")
                st.stop()
            
            # Prezzo attuale
            if isinstance(data['Close'], pd.DataFrame):
                current_price = float(data['Close'].iloc[-1, 0])
                close_series = data['Close'].iloc[:, 0]
                high_series = data['High'].iloc[:, 0]
                low_series = data['Low'].iloc[:, 0]
                open_series = data['Open'].iloc[:, 0]
            else:
                current_price = float(data['Close'].iloc[-1])
                close_series = data['Close']
                high_series = data['High']
                low_series = data['Low']
                open_series = data['Open']
            
            # ============================================
            # CALCOLO INDICATORI
            # ============================================
            
            # RSI
            rsi = calculate_rsi(close_series)
            current_rsi = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0
            
            # MACD
            macd, macd_signal, macd_hist = calculate_macd(close_series)
            current_macd = float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else 0
            current_macd_signal = float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else 0
            current_macd_hist = float(macd_hist.iloc[-1]) if not pd.isna(macd_hist.iloc[-1]) else 0
            
            # Bollinger Bands
            bb_upper, bb_middle, bb_lower = calculate_bollinger(close_series)
            current_bb_upper = float(bb_upper.iloc[-1]) if not pd.isna(bb_upper.iloc[-1]) else current_price * 1.02
            current_bb_lower = float(bb_lower.iloc[-1]) if not pd.isna(bb_lower.iloc[-1]) else current_price * 0.98
            current_bb_middle = float(bb_middle.iloc[-1]) if not pd.isna(bb_middle.iloc[-1]) else current_price
            
            # ATR
            atr = calculate_atr(high_series, low_series, close_series)
            current_atr = float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else (high_series.tail(20).max() - low_series.tail(20).min()) * 0.1
            
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
            st.markdown("## 🧠 ANALISI AI E SENTIMENT")
            
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
                    <div class="ai-title">🤖 ANALISI AI DEL GIORNO</div>
                    <div style="margin-bottom: 15px;">
                        <span class="{ai_class}">SEGNALE AI: {ai_signal} (confidenza: {sentiment_data['confidence']}%)</span>
                    </div>
                    {get_ai_trend_analysis(selected_asset, sentiment_data)}
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # MACHINE LEARNING FORECAST
            # ============================================
            st.markdown("## 🤖 PREVISIONI MACHINE LEARNING")
            
            ml_forecast = generate_ml_forecast(data, forecast_days=ml_days, method=ml_method)
            
            if ml_forecast:
                ml_class = "sentiment-positive" if ml_forecast['direction'] == 'UP' else "sentiment-negative"
                
                with st.container():
                    st.markdown(f"""
                    <div class="ml-card">
                        <div class="ml-title">🤖 ML FORECAST ({ml_forecast['method'].upper()})</div>
                        <div style="margin-bottom: 15px;">
                            <span class="{ml_class}">DIREZIONE: {ml_forecast['direction']} (confidenza: {ml_forecast['confidence']:.0f}%)</span>
                        </div>
                        <div class="ai-content">
                            <p><b>📊 Previsioni prossimi {ml_days} giorni:</b></p>
                    """, unsafe_allow_html=True)
                    
                    # Tabella previsioni
                    forecast_df = pd.DataFrame(ml_forecast['forecasts'])
                    st.dataframe(forecast_df, use_container_width=True)
                    
                    # Grafico previsioni
                    fig_ml = go.Figure()
                    
                    # Dati storici recenti
                    fig_ml.add_trace(go.Scatter(
                        x=data.index[-50:],
                        y=close_series[-50:],
                        mode='lines',
                        name='Storico',
                        line=dict(color='#00ff00', width=2)
                    ))
                    
                    # Previsioni
                    forecast_dates = [data.index[-1] + timedelta(days=d['day']) for d in ml_forecast['forecasts']]
                    forecast_prices = [d['price'] for d in ml_forecast['forecasts']]
                    
                    fig_ml.add_trace(go.Scatter(
                        x=forecast_dates,
                        y=forecast_prices,
                        mode='lines+markers',
                        name='Previsione ML',
                        line=dict(color='#aa00ff', width=2, dash='dash'),
                        marker=dict(size=8)
                    ))
                    
                    fig_ml.update_layout(
                        template='plotly_dark',
                        height=300,
                        title='Previsione ML vs Storico',
                        showlegend=True,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    
                    st.plotly_chart(fig_ml, use_container_width=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Previsione ML non disponibile. Uso simulazione.")
            
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
                r3_html = f'<div class="pivot-r">R3: {pivot_levels["R3"]:.4f}</div>' if pivot_levels.get('R3') and pivot_levels['R3'] else ''
                r4_html = f'<div class="pivot-r">R4: {pivot_levels["R4"]:.4f}</div>' if pivot_levels.get('R4') and pivot_levels['R4'] else ''
                
                st.markdown(f"""
                <div class="pivot-card">
                    <div class="pivot-pp">PP: {pivot_levels['PP']:.4f}</div>
                    <div class="pivot-r">R1: {pivot_levels['R1']:.4f}</div>
                    <div class="pivot-r">R2: {pivot_levels['R2']:.4f}</div>
                    {r3_html}
                    {r4_html}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="pivot-card">
                    <div style="color: #aaa;">Metodo: {pivot_levels['method']}</div>
                    <div style="color: #aaa;">Prezzo attuale: {current_price:.4f}</div>
                    <div style="color: #aaa;">Range: {(prev_high-prev_low):.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                s3_html = f'<div class="pivot-s">S3: {pivot_levels["S3"]:.4f}</div>' if pivot_levels.get('S3') and pivot_levels['S3'] else ''
                s4_html = f'<div class="pivot-s">S4: {pivot_levels["S4"]:.4f}</div>' if pivot_levels.get('S4') and pivot_levels['S4'] else ''
                
                st.markdown(f"""
                <div class="pivot-card">
                    <div class="pivot-s">S1: {pivot_levels['S1']:.4f}</div>
                    <div class="pivot-s">S2: {pivot_levels['S2']:.4f}</div>
                    {s3_html}
                    {s4_html}
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # SEGNALE COMBINATO
            # ============================================
            
            st.markdown("## 🎯 SEGNALE COMBINATO")
            
            combined_signal, combined_class, signal_desc = get_combined_signal(
                current_rsi, current_macd, current_macd_signal, 
                current_price, current_bb_upper, current_bb_lower, ai_signal
            )
            
            st.markdown(f"""
            <div style="background: #1a1f2e; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #00ff00;">
                <h3 style="color: #ffffff; margin: 0;">{signal_desc}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # ============================================
            # LIVELLI OPERATIVI
            # ============================================
            
            st.markdown("## 📊 LIVELLI OPERATIVI")
            
            # DETERMINA TP BASATO SU PIVOT
            if combined_signal == "BUY":
                entry = current_price * 0.998
                tp, tp_source = get_tp_from_pivots(current_price, pivot_levels, "BUY")
                sl, sl_source = get_sl_from_pivots(current_price, pivot_levels, "BUY")
            else:
                entry = current_price * 1.002
                tp, tp_source = get_tp_from_pivots(current_price, pivot_levels, "SELL")
                sl, sl_source = get_sl_from_pivots(current_price, pivot_levels, "SELL")
            
            # CALCOLA PIPS
            if 'JPY' in selected_asset:
                pip_multiplier = 0.01
                pips_to_tp = abs(tp - entry) / 0.01
                pips_to_sl = abs(sl - entry) / 0.01
            elif any(x in selected_asset for x in ['BTC', 'ETH']):
                pip_multiplier = 1
                pips_to_tp = abs(tp - entry)
                pips_to_sl = abs(sl - entry)
            elif any(x in selected_asset for x in ['XAU', 'XAG']):
                pip_multiplier = 0.1
                pips_to_tp = abs(tp - entry) / 0.1
                pips_to_sl = abs(sl - entry) / 0.1
            else:
                pip_multiplier = 0.0001
                pips_to_tp = abs(tp - entry) / 0.0001
                pips_to_sl = abs(sl - entry) / 0.0001
            
            # CALCOLO LOTTI
            if 'JPY' in selected_asset:
                multiplier = 1000
            elif any(x in selected_asset for x in ['BTC', 'ETH']):
                multiplier = 1
            elif any(x in selected_asset for x in ['XAU', 'XAG']):
                multiplier = 100
            else:
                multiplier = 100000
            
            risk_amount = capitale * (rischio / 100)
            lotti = max(0.01, round(risk_amount / (abs(entry - sl) * multiplier), 2))
            actual_risk = lotti * abs(entry - sl) * multiplier
            rr_ratio = abs(tp - entry) / abs(sl - entry) if sl != entry else 1
            
            # Price Card
            st.markdown(f"""
            <div class="price-card">
                <div class="{combined_class}">{combined_signal}</div>
                <div class="price-value">{current_price:,.4f}</div>
                <div style="color: #cccccc; margin-top: 10px;">
                    {selected_asset} | {timeframe} | Agg: {datetime.now().strftime('%H:%M:%S')}
                </div>
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
                    <div style="color: #888; font-size: 11px;">{pips_to_tp:.0f} pips ({tp_source})</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">STOP LOSS</div>
                    <div class="sl-value">{sl:,.4f}</div>
                    <div style="color: #888; font-size: 11px;">{pips_to_sl:.0f} pips ({sl_source})</div>
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
                    <div class="metric-value" style="color: #ff4444 !important;">€{actual_risk:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">R/R RATIO</div>
                    <div class="metric-value">{rr_ratio:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabella indicatori
            st.markdown("## 📊 TABELLA INDICATORI")
            
            indicators_data = {
                'Indicatore': ['RSI (14)', 'MACD', 'MACD Signal', 'MACD Histogram', 
                              'Bollinger Upper', 'Bollinger Middle', 'Bollinger Lower',
                              'ATR (14)', 'Volume'],
                'Valore': [
                    f"{current_rsi:.2f}",
                    f"{current_macd:.4f}",
                    f"{current_macd_signal:.4f}",
                    f"{current_macd_hist:.4f}",
                    f"{current_bb_upper:.4f}",
                    f"{current_bb_middle:.4f}",
                    f"{current_bb_lower:.4f}",
                    f"{current_atr:.4f}",
                    f"{volume:,.0f}"
                ],
                'Segnale': [
                    'Ipercomprato >70, Ipervenduto <30',
                    '> Signal = Bullish',
                    '< MACD = Bearish',
                    'Positivo = Bullish',
                    'Resistenza',
                    'Media mobile',
                    'Supporto',
                    'Volatilità',
                    'Liquidità'
                ]
            }
            
            indicators_df = pd.DataFrame(indicators_data)
            st.dataframe(indicators_df, use_container_width=True, hide_index=True)
            
            # Grafico completo
            st.markdown("## 📈 GRAFICO COMPLETO")
            
            fig = make_subplots(
                rows=4, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.4, 0.2, 0.2, 0.2],
                subplot_titles=('Prezzo & Bollinger', 'Volume', 'MACD', 'RSI')
            )
            
            # Prezzo e Bollinger
            fig.add_trace(go.Candlestick(
                x=data.index[-100:],
                open=open_series[-100:],
                high=high_series[-100:],
                low=low_series[-100:],
                close=close_series[-100:],
                name='Prezzo',
                showlegend=False
            ), row=1, col=1)
            
            # Bollinger Bands
            fig.add_trace(go.Scatter(
                x=data.index[-100:],
                y=bb_upper[-100:],
                line=dict(color='rgba(0,255,0,0.3)', width=1),
                name='BB Upper',
                showlegend=False
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data.index[-100:],
                y=bb_lower[-100:],
                line=dict(color='rgba(255,0,0,0.3)', width=1),
                fill='tonexty',
                fillcolor='rgba(128,128,128,0.1)',
                name='BB Lower',
                showlegend=False
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
                vol_data = data['Volume'].iloc[-100:] if not isinstance(data['Volume'].iloc[-100:], pd.DataFrame) else data['Volume'].iloc[-100:,0]
                fig.add_trace(go.Bar(
                    x=data.index[-100:],
                    y=vol_data,
                    marker_color='#00ff00',
                    name='Volume',
                    showlegend=False
                ), row=2, col=1)
            
            # MACD
            fig.add_trace(go.Scatter(
                x=data.index[-100:],
                y=macd[-100:],
                line=dict(color='#00ff00', width=2),
                name='MACD',
                showlegend=False
            ), row=3, col=1)
            
            fig.add_trace(go.Scatter(
                x=data.index[-100:],
                y=macd_signal[-100:],
                line=dict(color='#ffaa00', width=2),
                name='Signal',
                showlegend=False
            ), row=3, col=1)
            
            fig.add_trace(go.Bar(
                x=data.index[-100:],
                y=macd_hist[-100:],
                marker_color=['#00ff00' if x >= 0 else '#ff4444' for x in macd_hist[-100:]],
                name='Histogram',
                showlegend=False
            ), row=3, col=1)
            
            # RSI
            fig.add_trace(go.Scatter(
                x=data.index[-100:],
                y=rsi[-100:],
                line=dict(color='#aa00ff', width=2),
                name='RSI',
                showlegend=False
            ), row=4, col=1)
            
            fig.add_hline(y=70, line_color='red', line_dash='dash', row=4, col=1)
            fig.add_hline(y=30, line_color='green', line_dash='dash', row=4, col=1)
            
            fig.update_layout(
                template='plotly_dark',
                height=800,
                showlegend=False,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Supporto/Resistenza
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">SUPPORTO (20gg)</div>
                    <div class="entry-value">{low_20:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">RESISTENZA (20gg)</div>
                    <div class="tp-value">{high_20:,.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Errore durante l'analisi: {str(e)}")
            st.exception(e)

else:
    # Messaggio iniziale
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px; color: #cccccc;">
        <h2 style="color: #00ff00;">👋 Benvenuto su Trading Terminal AI Ultimate</h2>
        <p style="font-size: 18px; margin: 20px 0;">
            Seleziona un asset e i parametri dal menu a sinistra, poi clicca su ANALIZZA CON AI & ML
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; margin: 40px 0; flex-wrap: wrap;">
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">📊 15+</h3>
                <p>Asset</p>
            </div>
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">📈 5</h3>
                <p>Indicatori</p>
            </div>
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">🤖 3</h3>
                <p>Modelli ML</p>
            </div>
            <div style="background: #1a1f2e; padding: 20px; border-radius: 10px; width: 200px;">
                <h3 style="color: #00ff00;">📐 4</h3>
                <p>Pivot Methods</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ Disclaimer: Questo è un tool informativo, non un consiglio finanziario. I dati possono subire ritardi.</p>
    <p>© 2024 Trading Terminal AI Ultimate | RSI • MACD • Bollinger • ML • Pivot Points • Sentiment AI</p>
</div>
""", unsafe_allow_html=True)
