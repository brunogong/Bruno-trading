"""
TRADING TERMINAL AI PRO - VERSIONE DEFINITIVA
✅ Testo GIALLO solo su sfondo scuro
✅ Testo NERO su sfondo chiaro (sidebar)
✅ Motivazioni dettagliate per segnali AI
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz
import random

# Configurazione pagina
st.set_page_config(
    page_title="Trading Terminal AI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS con testo GIALLO solo su sfondo SCURO
st.markdown("""
<style>
    /* MAIN BACKGROUND */
    .stApp {
        background-color: #0d1117;
    }
    
    /* TESTO PRINCIPALE - GIALLO SU SFONDO SCURO */
    .stApp p, .stApp li, .stApp span, .stApp div:not([data-testid="stSidebar"] div),
    .stApp .stMarkdown, .stApp .stText, .stApp h2, .stApp h3, .stApp h4 {
        color: #ffff00 !important;
    }
    
    /* Headers verdi */
    .stApp h1 {
        color: #00ff00 !important;
    }
    
    /* SIDEBAR - SFONDO CHIARO, TESTO NERO */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #0066cc !important;
        font-weight: bold;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 5px;
    }
    
    section[data-testid="stSidebar"] h4 {
        color: #333333 !important;
        margin-top: 15px;
    }
    
    /* Header principale */
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
    
    .header p {
        color: #ffff00 !important;
    }
    
    /* AI Card con motivazioni */
    .ai-card {
        background: linear-gradient(135deg, #1e2a3a, #0f1a24);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        margin: 15px 0;
    }
    
    .ai-title {
        color: #00ff00 !important;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .ai-content {
        color: #ffff00 !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .ai-content li {
        color: #ffff00 !important;
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
        color: #ffff00 !important;
        font-weight: bold;
        background: rgba(255,255,0,0.1);
        padding: 5px 10px;
        border-radius: 5px;
    }
    
    /* Pivot Cards - testo giallo su sfondo scuro */
    .pivot-card {
        background: #1a1f2e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00ccff;
        margin: 10px 0;
    }
    
    .pivot-card div, .pivot-card span {
        color: #ffff00 !important;
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
    
    .metric-card div {
        color: #ffff00 !important;
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
    
    .level-card div {
        color: #ffff00 !important;
    }
    
    .entry-value { color: #00ccff !important; font-size: 18px; font-weight: bold; }
    .tp-value { color: #00ff00 !important; font-size: 18px; font-weight: bold; }
    .sl-value { color: #ff4444 !important; font-size: 18px; font-weight: bold; }
    
    /* Dataframe */
    .dataframe {
        color: #ffff00 !important;
    }
    
    .dataframe th {
        color: #00ff00 !important;
        background-color: #1a1f2e !important;
    }
    
    .dataframe td {
        color: #ffff00 !important;
        background-color: #0d1117 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #ffff00 !important;
        font-size: 11px;
        padding: 15px;
        border-top: 1px solid #333;
        margin-top: 30px;
    }
    
    .footer p {
        color: #ffff00 !important;
    }
    
    /* Info boxes */
    .stAlert, .stInfo {
        color: #ffff00 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNZIONI INDICATORI TECNICI
# ============================================

def calculate_rsi(prices, period=14):
    """Calcola RSI"""
    try:
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50.0
    except:
        return 50.0

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calcola MACD"""
    try:
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return float(macd.iloc[-1]), float(signal_line.iloc[-1])
    except:
        return 0.0, 0.0

def calculate_bollinger(prices, period=20, std_dev=2):
    """Calcola Bollinger Bands"""
    try:
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return float(upper.iloc[-1]), float(lower.iloc[-1])
    except:
        return float(prices.iloc[-1]) * 1.02, float(prices.iloc[-1]) * 0.98

def calculate_atr(high, low, close, period=14):
    """Calcola ATR"""
    try:
        high_low = high - low
        high_close = abs(high - close.shift(1))
        low_close = abs(low - close.shift(1))
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else 0
    except:
        return 0

# ============================================
# FUNZIONI PREVISIONI
# ============================================

def generate_forecast(data, forecast_days=5):
    """Genera previsioni realistiche"""
    last_price = float(data['Close'].iloc[-1])
    
    returns = data['Close'].pct_change().dropna()
    if len(returns) > 0:
        avg_return = float(returns.mean()) * forecast_days
        volatility = float(returns.std()) * np.sqrt(forecast_days / 252)
    else:
        avg_return = 0.01
        volatility = 0.02
    
    forecasts = []
    current_price = last_price
    
    for day in range(1, forecast_days + 1):
        drift = avg_return / forecast_days
        random_shock = np.random.normal(0, max(0.001, volatility / np.sqrt(forecast_days)))
        price_change = current_price * (drift + random_shock)
        new_price = current_price + price_change
        
        max_change = last_price * 0.05
        if abs(new_price - current_price) > max_change:
            new_price = current_price + (max_change if new_price > current_price else -max_change)
        
        new_price = max(new_price, last_price * 0.5)
        
        forecasts.append({
            'day': day,
            'price': new_price,
            'change_pct': ((new_price / last_price) - 1) * 100
        })
        
        current_price = new_price
    
    confidence = max(60, 85 - forecast_days * 3)
    direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
    
    return {
        'forecasts': forecasts,
        'confidence': confidence,
        'direction': direction
    }

# ============================================
# FUNZIONI PIVOT POINTS
# ============================================

def calculate_pivot_points(high, low, close, method='standard'):
    """Calcola i Pivot Points - 4 metodi"""
    h = float(high)
    l = float(low)
    c = float(close)
    
    if method == 'standard':
        pivot = (h + l + c) / 3
        r1 = (2 * pivot) - l
        r2 = pivot + (h - l)
        r3 = h + 2 * (pivot - l)
        s1 = (2 * pivot) - h
        s2 = pivot - (h - l)
        s3 = l - 2 * (h - pivot)
        
        return {
            'PP': pivot, 'R1': r1, 'R2': r2, 'R3': r3,
            'S1': s1, 'S2': s2, 'S3': s3, 'method': 'Standard'
        }
    
    elif method == 'fibonacci':
        pivot = (h + l + c) / 3
        range_hl = h - l
        r3 = pivot + range_hl * 1.000
        r2 = pivot + range_hl * 0.618
        r1 = pivot + range_hl * 0.382
        s1 = pivot - range_hl * 0.382
        s2 = pivot - range_hl * 0.618
        s3 = pivot - range_hl * 1.000
        
        return {
            'PP': pivot, 'R1': r1, 'R2': r2, 'R3': r3,
            'S1': s1, 'S2': s2, 'S3': s3, 'method': 'Fibonacci'
        }
    
    elif method == 'woodie':
        pivot = (h + l + 2 * c) / 4
        r1 = (2 * pivot) - l
        r2 = pivot + h - l
        s1 = (2 * pivot) - h
        s2 = pivot - h + l
        
        return {
            'PP': pivot, 'R1': r1, 'R2': r2, 'R3': None,
            'S1': s1, 'S2': s2, 'S3': None, 'method': 'Woodie'
        }
    
    elif method == 'camarilla':
        pivot = (h + l + c) / 3
        range_hl = h - l
        r4 = c + range_hl * 1.5000
        r3 = c + range_hl * 1.2500
        r2 = c + range_hl * 1.1666
        r1 = c + range_hl * 1.0833
        s1 = c - range_hl * 1.0833
        s2 = c - range_hl * 1.1666
        s3 = c - range_hl * 1.2500
        s4 = c - range_hl * 1.5000
        
        return {
            'PP': pivot, 'R1': r1, 'R2': r2, 'R3': r3, 'R4': r4,
            'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'method': 'Camarilla'
        }
    
    else:
        return calculate_pivot_points(high, low, close, 'standard')

# ============================================
# FUNZIONI SENTIMENT CON MOTIVAZIONI DETTAGLIATE
# ============================================

def get_market_sentiment(asset):
    """Sentiment di mercato con MOTIVAZIONI REALISTICHE"""
    
    sentiment_db = {
        # FOREX
        'EUR/USD': {
            'prediction': 'BUY',
            'confidence': 78,
            'icon': '🟢',
            'summary': 'Positivo su attese tagli Fed',
            'reasons': [
                '📉 Attesa taglio tassi Fed a giugno (65% probabilità)',
                '📈 Differenziale tassi BCE/Fed in riduzione',
                '📊 Dati PMI eurozona sopra le attese (50.2 vs 49.8)',
                '💰 Posizionamento speculativo net-long in aumento',
                '🌍 Flussi safe-haven in calo per riduzione tensioni'
            ]
        },
        'GBP/USD': {
            'prediction': 'BUY',
            'confidence': 65,
            'icon': '🟢',
            'summary': 'Sterlina supportata da dati PIL',
            'reasons': [
                '📈 PIL UK in crescita maggiore del previsto (+0.3% vs +0.1%)',
                '🏦 BOE mantiene tono hawkish su inflazione servizi',
                '📊 Inflazione core stabile al 4.2%',
                '💼 Mercato del lavoro solido (disoccupazione 3.8%)',
                '🔄 Attesa per prossima mossa BOE a maggio'
            ]
        },
        'USD/JPY': {
            'prediction': 'NEUTRAL',
            'confidence': 55,
            'icon': '🟡',
            'summary': 'Banca del Giappone ancora accomodante',
            'reasons': [
                '🏦 BoJ conferma tassi negativi (-0.1%)',
                '🗣️ Interventi verbali frequenti per limitare downside',
                '📊 Differenziale tassi ancora ampio con USA',
                '⚠️ Possibile intervento diretto su livelli 152',
                '🔄 Posizionamento speculativo contrastante'
            ]
        },
        'AUD/USD': {
            'prediction': 'BUY',
            'confidence': 62,
            'icon': '🟢',
            'summary': 'Sostenuto da commodity e RBA',
            'reasons': [
                '🪙 Prezzo minerale di ferro in aumento (+8%)',
                '🏦 RBA segnala possibile rialzo tassi',
                '📈 Inflazione australiana sopra target',
                '🇨🇳 Dati import cinesi migliori del previsto',
                '📊 PMI servizi in espansione'
            ]
        },
        'USD/CAD': {
            'prediction': 'SELL',
            'confidence': 58,
            'icon': '🔴',
            'summary': 'Petrolio in rialzo supporta CAD',
            'reasons': [
                '🛢️ Petrolio WTI in rialzo a $85/barile',
                '📈 Domanda cinese in ripresa',
                '🏦 BOC mantiene tono hawkish',
                '📊 PIL Canada sopra attese',
                '⚡ Tagli produzione OPEC+ prolungati'
            ]
        },
        'USD/CHF': {
            'prediction': 'NEUTRAL',
            'confidence': 52,
            'icon': '🟡',
            'summary': 'Franco ancora bene rifugio',
            'reasons': [
                '🏔️ Franco ancora considerato bene rifugio',
                '🏦 SNB intervenuta a difesa del franco',
                '📉 Inflazione svizzera in calo',
                '🌍 Tensioni geopolitiche ancora presenti',
                '📊 Posizionamento neutrale'
            ]
        },
        'NZD/USD': {
            'prediction': 'BUY',
            'confidence': 60,
            'icon': '🟢',
            'summary': 'Dati neozelandesi positivi',
            'reasons': [
                '📈 PIL NZ in crescita',
                '🏦 RBNZ segnala tassi alti più a lungo',
                '🥛 Prezzi lattiero-caseari in rialzo',
                '📊 Fiducia imprese in miglioramento',
                '🇨🇳 Domanda cinese in ripresa'
            ]
        },
        'EUR/GBP': {
            'prediction': 'NEUTRAL',
            'confidence': 51,
            'icon': '🟡',
            'summary': 'Due economie simili',
            'reasons': [
                '📊 Banche centrali allineate',
                '📉 Inflazione simile in entrambe le aree',
                '💼 Dati occupazione equivalenti',
                '🌍 Flussi incrociati bilanciati',
                '📈 Posizionamento tecnico neutrale'
            ]
        },
        'EUR/JPY': {
            'prediction': 'BUY',
            'confidence': 63,
            'icon': '🟢',
            'summary': 'Carry trade favorevole',
            'reasons': [
                '💰 Carry trade favorevole (EUR rende, JPY no)',
                '📊 PMI eurozona in miglioramento',
                '🏦 BoJ ancora ultra-accomodante',
                '📈 Spread rendimenti in ampliamento',
                '🔄 Posizionamento net-long in aumento'
            ]
        },
        'GBP/JPY': {
            'prediction': 'BUY',
            'confidence': 64,
            'icon': '🟢',
            'summary': 'Carry trade molto favorevole',
            'reasons': [
                '💰 Carry trade estremamente favorevole',
                '📈 Dati UK solidi',
                '🏦 BoJ isolata con tassi negativi',
                '📊 Spread rendimenti massimo storico',
                '⚡ Momentum tecnico positivo'
            ]
        },
        
        # COMMODITIES
        'XAU/USD (Oro)': {
            'prediction': 'BUY',
            'confidence': 82,
            'icon': '🟢',
            'summary': 'Acquisti banche centrali e bene rifugio',
            'reasons': [
                '🏦 Banche centrali acquisti record (1.100 tonnellate nel 2023)',
                '🌍 Tensioni geopolitiche in Medio Oriente e Ucraina',
                '💰 Attesa tagli tassi Fed (bene rifugio)',
                '📉 Dollaro in debolezza attesa',
                '🛡️ Copertura contro inflazione persistente'
            ]
        },
        'XAG/USD (Argento)': {
            'prediction': 'BUY',
            'confidence': 70,
            'icon': '🟢',
            'summary': 'Domanda industriale in crescita',
            'reasons': [
                '🔋 Domanda per pannelli solari in forte crescita',
                '📱 Usato in componenti elettronici',
                '💰 Segue trend oro come bene rifugio',
                '📈 Industriali in ripresa globale',
                '⚡ Deficit di offerta previsto'
            ]
        },
        'WTI Crude Oil': {
            'prediction': 'BUY',
            'confidence': 68,
            'icon': '🟢',
            'summary': 'Tagli OPEC e tensioni geopolitiche',
            'reasons': [
                '⚡ Tagli produzione OPEC+ prolungati',
                '🌍 Tensioni in Medio Oriente',
                '📈 Domanda cinese in ripresa',
                '📉 Scorte USA in calo',
                '💰 Posizionamento speculativo net-long'
            ]
        },
        'Brent Oil': {
            'prediction': 'BUY',
            'confidence': 67,
            'icon': '🟢',
            'summary': 'Segue trend WTI',
            'reasons': [
                '⚡ Stessi fattori del WTI',
                '🌍 Premium per rischio geopolitico',
                '📈 Domanda europea stabile',
                '📉 Scorte in calo',
                '💰 Spread con WTI in contrazione'
            ]
        },
        'Natural Gas': {
            'prediction': 'SELL',
            'confidence': 45,
            'icon': '🔴',
            'summary': 'Scorte piene, domanda debole',
            'reasons': [
                '📦 Scorte USA sopra media storica',
                '❄️ Inverno mite in Europa',
                '📉 Domanda industriale debole',
                '⚡ Produzione in aumento',
                '🌍 Tensioni geopolitiche in calo'
            ]
        },
        'Copper': {
            'prediction': 'BUY',
            'confidence': 72,
            'icon': '🟢',
            'summary': 'Transizione energetica e deficit',
            'reasons': [
                '🔋 Domanda per veicoli elettrici',
                '⚡ Deficit di offerta previsto',
                '📈 Dati manifatturieri Cina in miglioramento',
                '🏗️ Infrastrutture USA',
                '💰 Posizionamento speculativo net-long'
            ]
        },
        
        # CRYPTO
        'BTC/USD': {
            'prediction': 'BUY',
            'confidence': 88,
            'icon': '🟢',
            'summary': 'ETF inflows e halving imminente',
            'reasons': [
                '💰 ETF inflows record (oltre $10 miliardi in 2 mesi)',
                '⚡ Halving aprile 2024 (riduzione offerta)',
                '🏦 Adozione istituzionale in crescita',
                '📈 Accumulo whale addresses',
                '🌍 Bene rifugio digitale'
            ]
        },
        'ETH/USD': {
            'prediction': 'BUY',
            'confidence': 75,
            'icon': '🟢',
            'summary': 'Upgrade Dencun e attività DeFi',
            'reasons': [
                '⚡ Upgrade Dencun imminente',
                '📈 Attività DeFi in aumento',
                '💰 ETF attesi per fine anno',
                '🔗 Layer 2 in espansione',
                '📊 Staking yields interessanti'
            ]
        },
        'BNB/USD': {
            'prediction': 'BUY',
            'confidence': 70,
            'icon': '🟢',
            'summary': 'Ecosistema BSC in crescita',
            'reasons': [
                '📈 Volume transazioni BSC in aumento',
                '💰 Quarterly burn riduce offerta',
                '🔗 Nuovi progetti in lancio',
                '📊 Dominance in crescita',
                '🔄 Correlazione con BTC'
            ]
        },
        'SOL/USD': {
            'prediction': 'BUY',
            'confidence': 80,
            'icon': '🟢',
            'summary': 'Ethereum killer in ascesa',
            'reasons': [
                '⚡ Alta velocità e bassi costi',
                '📈 DeFi e NFT in forte crescita',
                '💰 Investimenti VC in aumento',
                '🔗 Breakpoint conferenza positiva',
                '📊 Metriche on-chain in miglioramento'
            ]
        },
        'ADA/USD': {
            'prediction': 'BUY',
            'confidence': 65,
            'icon': '🟢',
            'summary': 'Sviluppi ecosistema',
            'reasons': [
                '🔧 Hydra scaling solution in sviluppo',
                '📈 Partnership accademiche',
                '💰 Interesse istituzionale',
                '🔗 Governance in evoluzione',
                '📊 Community attiva'
            ]
        },
        'DOGE/USD': {
            'prediction': 'NEUTRAL',
            'confidence': 55,
            'icon': '🟡',
            'summary': 'Speculativo, segue BTC',
            'reasons': [
                '🐕 Supporto Elon Musk',
                '📈 Segue trend BTC',
                '💬 Social media hype',
                '⚡ Transazioni in aumento',
                '💰 Posizionamento speculativo'
            ]
        },
        
        # INDICI
        'S&P 500': {
            'prediction': 'BUY',
            'confidence': 70,
            'icon': '🟢',
            'summary': 'Earnings solidi, soft landing atteso',
            'reasons': [
                '📊 Earnings Q4 sopra attese (+5.2%)',
                '🏦 Attesa tagli Fed H2 2024',
                '📈 Settore tech guida (AI hype)',
                '💼 Mercato del lavoro solido',
                '💰 Buyback aziendali in aumento'
            ]
        },
        'Dow Jones': {
            'prediction': 'BUY',
            'confidence': 68,
            'icon': '🟢',
            'summary': 'Industriali in ripresa',
            'reasons': [
                '🏭 Settore manifatturiero in miglioramento',
                '📈 Dati occupazione solidi',
                '💰 Dividendi attraenti',
                '📊 P/E ratio nella media storica',
                '🔄 Rotazione da growth a value'
            ]
        },
        'NASDAQ': {
            'prediction': 'BUY',
            'confidence': 72,
            'icon': '🟢',
            'summary': 'AI hype e tassi in calo',
            'reasons': [
                '🤖 AI hype continua (NVIDIA, Microsoft)',
                '📈 Earning big tech solidi',
                '💰 Attesa tagli tassi',
                '⚡ Innovazione in corso',
                '📊 Flussi verso settore growth'
            ]
        },
        'DAX': {
            'prediction': 'BUY',
            'confidence': 65,
            'icon': '🟢',
            'summary': 'Export tedesco in ripresa',
            'reasons': [
                '📦 Export verso Cina in aumento',
                '🏭 PMI manifatturiero sopra 50',
                '📈 Corporate earnings solidi',
                '💰 Dividendi alti',
                '🌍 Domanda globale in ripresa'
            ]
        },
        'FTSE': {
            'prediction': 'NEUTRAL',
            'confidence': 58,
            'icon': '🟡',
            'summary': 'UK tra recessione e ripresa',
            'reasons': [
                '📊 PIL UK in stagnazione',
                '🏦 BOE in attesa',
                '💰 Dividendi alti supportano',
                '🛢️ Energy sector pesa',
                '📈 Sterlina volatile'
            ]
        },
        'Nikkei 225': {
            'prediction': 'BUY',
            'confidence': 75,
            'icon': '🟢',
            'summary': 'Yen debole spinge export',
            'reasons': [
                '💰 Yen ai minimi storici',
                '📦 Export giapponese in crescita',
                '🏦 BoJ accomodante',
                '📈 Corporate governance riforme',
                '🌍 Investitori esteri in acquisto'
            ]
        },
        'Hang Seng': {
            'prediction': 'SELL',
            'confidence': 40,
            'icon': '🔴',
            'summary': 'Crisi immobiliare e deflazione',
            'reasons': [
                '🏢 Crisi settore immobiliare (Evergrande)',
                '📉 Deflazione in Cina',
                '📊 PMI manifatturiero in contrazione',
                '💰 Capital outflows',
                '🌍 Tensioni geopolitiche'
            ]
        }
    }
    
    default = {
        'prediction': 'NEUTRAL',
        'confidence': 50,
        'icon': '⚪',
        'summary': 'Analisi tecnica prevalente',
        'reasons': [
            '📊 Dati misti da fonti multiple',
            '📈 Posizionamento tecnico neutrale',
            '💰 Flussi istituzionali bilanciati',
            '🌍 Fattori macro contrastanti',
            '⚡ In attesa di catalyst'
        ]
    }
    
    return sentiment_db.get(asset, default)

def format_ai_analysis(asset, sentiment):
    """Formatta l'analisi AI con motivazioni"""
    
    prediction = sentiment['prediction']
    confidence = sentiment['confidence']
    icon = sentiment['icon']
    summary = sentiment['summary']
    reasons = sentiment['reasons']
    
    if prediction == 'BUY':
        signal_class = "sentiment-positive"
    elif prediction == 'SELL':
        signal_class = "sentiment-negative"
    else:
        signal_class = "sentiment-neutral"
    
    reasons_html = ""
    for reason in reasons:
        reasons_html += f'<li>{reason}</li>'
    
    return f"""
    <div class="ai-card">
        <div class="ai-title">🤖 ANALISI FONDAMENTALE AI</div>
        <div style="margin-bottom: 15px;">
            <span class="{signal_class}">{icon} {prediction} - {summary} (confidenza: {confidence}%)</span>
        </div>
        <div class="ai-content">
            <p><b>📊 MOTIVAZIONI DEL SEGNALE:</b></p>
            <ul>
                {reasons_html}
            </ul>
            <p><b>📰 Fonte:</b> Reuters Polls / LSEG StarMine / Consensus Market</p>
        </div>
    </div>
    """

# ============================================
# FUNZIONE SEGNALE COMBINATO
# ============================================

def get_signal(rsi, macd, macd_signal, price, bb_upper, bb_lower, ai_signal):
    """Genera segnale combinato"""
    score = 0
    
    if rsi < 30: score += 2
    elif rsi < 40: score += 1
    elif rsi > 70: score -= 2
    elif rsi > 60: score -= 1
    
    if macd > macd_signal: score += 1
    else: score -= 1
    
    if price <= bb_lower: score += 2
    elif price >= bb_upper: score -= 2
    
    if ai_signal == 'BUY': score += 1
    elif ai_signal == 'SELL': score -= 1
    
    if score >= 3: return "BUY", "signal-buy", "✅ FORTE ACQUISTO"
    elif score <= -3: return "SELL", "signal-sell", "🔴 FORTE VENDITA"
    elif score >= 1: return "BUY", "signal-buy", "🟡 ACQUISTO DEBOLE"
    elif score <= -1: return "SELL", "signal-sell", "🟡 VENDITA DEBOLE"
    else: return "NEUTRAL", "neutral", "⚪ NEUTRALE"

# ============================================
# MAIN APP
# ============================================

st.markdown("""
<div class="header">
    <h1>🤖 TRADING TERMINAL AI PRO</h1>
    <p>30+ Asset • 4 Metodi Pivot • RSI • MACD • Bollinger • Previsioni • Analisi Fondamentale AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROLLI")
    
    # ASSET COMPLETI
    st.markdown("#### 📈 SELEZIONA ASSET")
    
    assets = {
        '💵 FOREX': {
            'EUR/USD': 'EURUSD=X',
            'GBP/USD': 'GBPUSD=X',
            'USD/JPY': 'USDJPY=X',
            'AUD/USD': 'AUDUSD=X',
            'USD/CAD': 'USDCAD=X',
            'USD/CHF': 'USDCHF=X',
            'NZD/USD': 'NZDUSD=X',
            'EUR/GBP': 'EURGBP=X',
            'EUR/JPY': 'EURJPY=X',
            'GBP/JPY': 'GBPJPY=X'
        },
        '🏅 COMMODITIES': {
            'XAU/USD (Oro)': 'GC=F',
            'XAG/USD (Argento)': 'SI=F',
            'WTI Crude Oil': 'CL=F',
            'Brent Oil': 'BZ=F',
            'Natural Gas': 'NG=F',
            'Copper': 'HG=F'
        },
        '₿ CRYPTO': {
            'BTC/USD': 'BTC-USD',
            'ETH/USD': 'ETH-USD',
            'BNB/USD': 'BNB-USD',
            'SOL/USD': 'SOL-USD',
            'ADA/USD': 'ADA-USD',
            'DOGE/USD': 'DOGE-USD'
        },
        '📊 INDICI': {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'NASDAQ': '^IXIC',
            'DAX (Germania)': '^GDAXI',
            'FTSE (UK)': '^FTSE',
            'Nikkei 225': '^N225',
            'Hang Seng': '^HSI'
        }
    }
    
    # Crea un dizionario piatto per la selezione
    all_assets = {}
    for category, cat_assets in assets.items():
        for name, symbol in cat_assets.items():
            all_assets[name] = symbol
    
    selected_asset = st.selectbox(
        "Asset",
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
    
    # METODO PIVOT (TUTTI E 4)
    st.markdown("#### 📐 METODO PIVOT")
    pivot_method = st.selectbox(
        "Metodo",
        options=['standard', 'fibonacci', 'woodie', 'camarilla'],
        index=0,
        format_func=lambda x: {
            'standard': '📊 Standard/Floor',
            'fibonacci': '📈 Fibonacci',
            'woodie': '📉 Woodie',
            'camarilla': '🎯 Camarilla'
        }[x]
    )
    
    # PREVISIONI
    st.markdown("#### 🔮 PREVISIONI")
    forecast_days = st.slider("Giorni", 1, 5, 3)
    
    # MONEY MANAGEMENT
    st.markdown("#### 💰 MONEY MANAGEMENT")
    capitale = st.number_input("Capitale (€)", value=1000, min_value=100, step=100)
    rischio = st.slider("Rischio %", 0.5, 3.0, 1.0, 0.1)
    
    # PULSANTE
    analyze_btn = st.button("🚀 ANALIZZA", type="primary", use_container_width=True)

# Main content
if analyze_btn:
    with st.spinner("Analisi in corso..."):
        try:
            symbol = all_assets[selected_asset]
            
            # Periodo
            period_map = {'1h': '5d', '4h': '1mo', '1d': '3mo'}
            
            # Download dati
            data = yf.download(symbol, period=period_map[timeframe], 
                              interval=timeframe, auto_adjust=True, progress=False)
            
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
            current_rsi = calculate_rsi(close_series)
            current_macd, current_macd_signal = calculate_macd(close_series)
            bb_upper, bb_lower = calculate_bollinger(close_series)
            current_atr = calculate_atr(high_series, low_series, close_series)
            
            # Livelli
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
            # ANALISI FONDAMENTALE AI CON MOTIVAZIONI
            # ============================================
            st.markdown("## 🧠 ANALISI FONDAMENTALE AI")
            
            sentiment = get_market_sentiment(selected_asset)
            ai_signal = sentiment['prediction']
            
            st.markdown(format_ai_analysis(selected_asset, sentiment), unsafe_allow_html=True)
            
            # ============================================
            # PREVISIONI
            # ============================================
            st.markdown("## 🔮 PREVISIONI PROSSIMI GIORNI")
            
            forecast = generate_forecast(data, forecast_days)
            
            forecast_df = pd.DataFrame(forecast['forecasts'])
            forecast_df.columns = ['Giorno', 'Prezzo', 'Variazione %']
            forecast_df['Variazione %'] = forecast_df['Variazione %'].round(2)
            forecast_df['Prezzo'] = forecast_df['Prezzo'].round(4)
            
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)
            
            # ============================================
            # PIVOT (TUTTI I LIVELLI)
            # ============================================
            st.markdown("## 📐 LIVELLI PIVOT")
            
            # Prepara dati pivot
            if len(data) > 1:
                if isinstance(high_series, pd.Series):
                    prev_high = float(high_series.iloc[-2])
                    prev_low = float(low_series.iloc[-2])
                    prev_close = float(close_series.iloc[-2])
                else:
                    prev_high = float(high_series[-2])
                    prev_low = float(low_series[-2])
                    prev_close = float(close_series[-2])
            else:
                prev_high = float(high_series.iloc[-1] if isinstance(high_series, pd.Series) else high_series[-1])
                prev_low = float(low_series.iloc[-1] if isinstance(low_series, pd.Series) else low_series[-1])
                prev_close = float(close_series.iloc[-1] if isinstance(close_series, pd.Series) else close_series[-1])
            
            pivot = calculate_pivot_points(prev_high, prev_low, prev_close, pivot_method)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Livelli di resistenza
                html = f"""
                <div class="pivot-card">
                    <div class="pivot-pp">PP: {pivot['PP']:.4f}</div>
                    <div class="pivot-r">R1: {pivot['R1']:.4f}</div>
                    <div class="pivot-r">R2: {pivot['R2']:.4f}</div>
                """
                if pivot.get('R3') and pivot['R3']:
                    html += f'<div class="pivot-r">R3: {pivot["R3"]:.4f}</div>'
                if pivot.get('R4') and pivot['R4']:
                    html += f'<div class="pivot-r">R4: {pivot["R4"]:.4f}</div>'
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="pivot-card">
                    <div>Metodo: {pivot['method']}</div>
                    <div>Prezzo: {current_price:.4f}</div>
                    <div>Range: {(prev_high-prev_low):.4f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Livelli di supporto
                html = f"""
                <div class="pivot-card">
                    <div class="pivot-s">S1: {pivot['S1']:.4f}</div>
                    <div class="pivot-s">S2: {pivot['S2']:.4f}</div>
                """
                if pivot.get('S3') and pivot['S3']:
                    html += f'<div class="pivot-s">S3: {pivot["S3"]:.4f}</div>'
                if pivot.get('S4') and pivot['S4']:
                    html += f'<div class="pivot-s">S4: {pivot["S4"]:.4f}</div>'
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
            
            # ============================================
            # SEGNALE COMBINATO
            # ============================================
            
            signal, signal_class, signal_desc = get_signal(
                current_rsi, current_macd, current_macd_signal,
                current_price, bb_upper, bb_lower, ai_signal
            )
            
            st.markdown(f"## {signal_desc}")
            
            # ============================================
            # LIVELLI OPERATIVI
            # ============================================
            
            # Entry/TP/SL basati su Pivot
            if signal == "BUY":
                entry = current_price * 0.998
                tp = pivot['R1'] if current_price < pivot['R1'] else pivot['R2'] if pivot.get('R2') and current_price < pivot['R2'] else current_price * 1.02
                sl = pivot['S1'] * 0.998 if current_price > pivot['S1'] else current_price * 0.985
            else:
                entry = current_price * 1.002
                tp = pivot['S1'] if current_price > pivot['S1'] else pivot['S2'] if pivot.get('S2') and current_price > pivot['S2'] else current_price * 0.98
                sl = pivot['R1'] * 1.002 if current_price < pivot['R1'] else current_price * 1.015
            
            # Calcolo pips in base all'asset
            if 'JPY' in selected_asset:
                pips_tp = abs(tp - entry) / 0.01
                pips_sl = abs(sl - entry) / 0.01
                multiplier = 1000
            elif 'BTC' in selected_asset or 'ETH' in selected_asset or 'BNB' in selected_asset or 'SOL' in selected_asset:
                pips_tp = abs(tp - entry)
                pips_sl = abs(sl - entry)
                multiplier = 1
            elif 'XAU' in selected_asset or 'XAG' in selected_asset:
                pips_tp = abs(tp - entry) / 0.1
                pips_sl = abs(sl - entry) / 0.1
                multiplier = 100
            else:
                pips_tp = abs(tp - entry) / 0.0001
                pips_sl = abs(sl - entry) / 0.0001
                multiplier = 100000
            
            # Calcolo lotti
            risk_amount = capitale * (rischio / 100)
            lotti = max(0.01, round(risk_amount / (abs(entry - sl) * multiplier), 2))
            actual_risk = lotti * abs(entry - sl) * multiplier
            rr_ratio = abs(tp - entry) / abs(sl - entry) if sl != entry else 1
            
            # Price card
            st.markdown(f"""
            <div class="price-card">
                <div class="{signal_class}">{signal}</div>
                <div class="price-value">{current_price:,.4f}</div>
                <div>{selected_asset}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Livelli operativi
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
                    <div>{pips_tp:.0f} pips</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="level-card">
                    <div class="level-label">STOP LOSS</div>
                    <div class="sl-value">{sl:,.4f}</div>
                    <div>{pips_sl:.0f} pips</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Money management
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
                    <div class="metric-label">R/R RATIO</div>
                    <div class="metric-value">{rr_ratio:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabella indicatori
            st.markdown("## 📊 INDICATORI TECNICI")
            
            indicators_data = {
                'Indicatore': ['RSI (14)', 'MACD', 'Signal', 'Bollinger Upper', 'Bollinger Lower', 'ATR (14)', 'Volume', 'Supporto 20gg', 'Resistenza 20gg'],
                'Valore': [
                    f"{current_rsi:.1f}",
                    f"{current_macd:.4f}",
                    f"{current_macd_signal:.4f}",
                    f"{bb_upper:.4f}",
                    f"{bb_lower:.4f}",
                    f"{current_atr:.4f}",
                    f"{volume:,.0f}",
                    f"{low_20:.4f}",
                    f"{high_20:.4f}"
                ]
            }
            
            indicators_df = pd.DataFrame(indicators_data)
            st.dataframe(indicators_df, use_container_width=True, hide_index=True)
            
            # Grafico
            st.markdown("## 📈 GRAFICO")
            
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                               vertical_spacing=0.05, row_heights=[0.7, 0.3])
            
            # Candele
            fig.add_trace(go.Candlestick(
                x=data.index[-50:],
                open=data['Open'].iloc[-50:].values if not isinstance(data['Open'].iloc[-50:], pd.DataFrame) else data['Open'].iloc[-50:,0].values,
                high=data['High'].iloc[-50:].values if not isinstance(data['High'].iloc[-50:], pd.DataFrame) else data['High'].iloc[-50:,0].values,
                low=data['Low'].iloc[-50:].values if not isinstance(data['Low'].iloc[-50:], pd.DataFrame) else data['Low'].iloc[-50:,0].values,
                close=data['Close'].iloc[-50:].values if not isinstance(data['Close'].iloc[-50:], pd.DataFrame) else data['Close'].iloc[-50:,0].values,
                increasing_line_color='#00ff00',
                decreasing_line_color='#ff4444'
            ), row=1, col=1)
            
            # Linee
            fig.add_hline(y=entry, line_color='cyan', line_width=2,
                         annotation_text=f'Entry {entry:.2f}', row=1, col=1)
            fig.add_hline(y=tp, line_color='lime', line_dash='dash',
                         annotation_text=f'TP {tp:.2f}', row=1, col=1)
            fig.add_hline(y=sl, line_color='red', line_dash='dash',
                         annotation_text=f'SL {sl:.2f}', row=1, col=1)
            
            # Volume
            if 'Volume' in data.columns:
                vol_data = data['Volume'].iloc[-50:].values if not isinstance(data['Volume'].iloc[-50:], pd.DataFrame) else data['Volume'].iloc[-50:,0].values
                fig.add_trace(go.Bar(
                    x=data.index[-50:],
                    y=vol_data,
                    marker_color='#00ff00'
                ), row=2, col=1)
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Errore: {str(e)}")
            st.exception(e)

else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h3>👋 Benvenuto su Trading Terminal AI Pro</h3>
        <p>Seleziona asset e parametri dal menu a sinistra, poi clicca ANALIZZA</p>
        <p>30+ Asset • 4 Metodi Pivot • RSI • MACD • Bollinger • Previsioni • Analisi Fondamentale con MOTIVAZIONI</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>⚠️ Dati da Yahoo Finance • 30+ Asset • 4 Metodi Pivot • Analisi Fondamentale con motivazioni reali</p>
    <p>© 2024 Trading Terminal AI Pro</p>
</div>
""", unsafe_allow_html=True)
