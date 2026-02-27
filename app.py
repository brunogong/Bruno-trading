"""
TRADING TERMINAL AI PRO - VERSIONE CON PREVISIONI ML GIORNALIERE CORRETTE
✅ Previsioni diverse per ogni giorno
✅ LSTM per serie temporali
✅ Random Forest con features lag
✅ Prophet con seasonality
"""

# ============================================
# FUNZIONI MACHINE LEARNING CORRETTE
# ============================================

def prepare_ml_features_improved(data, lags=5):
    """Prepara features per ML con lags"""
    df = data.copy()
    
    # Feature tecniche di base
    df['returns'] = df['Close'].pct_change()
    df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['volume_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
    df['high_low_ratio'] = df['High'] / df['Low']
    df['close_open_ratio'] = df['Close'] / df['Open']
    
    # Lagged features per previsioni multiple
    for lag in range(1, lags + 1):
        df[f'return_lag_{lag}'] = df['returns'].shift(lag)
        df[f'close_lag_{lag}'] = df['Close'].shift(lag)
        df[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
    
    # Rolling statistics (trend)
    for window in [5, 10, 20]:
        df[f'rolling_mean_{window}'] = df['Close'].rolling(window).mean()
        df[f'rolling_std_{window}'] = df['Close'].rolling(window).std()
        df[f'rolling_max_{window}'] = df['High'].rolling(window).max()
        df[f'rolling_min_{window}'] = df['Low'].rolling(window).min()
    
    # Technical indicators
    df['rsi'] = calculate_rsi(df['Close'])
    macd, signal, hist = calculate_macd(df['Close'])
    df['macd'] = macd
    df['macd_signal'] = signal
    df['macd_hist'] = hist
    
    bb_upper, bb_middle, bb_lower = calculate_bollinger(df['Close'])
    df['bb_upper'] = bb_upper
    df['bb_middle'] = bb_middle
    df['bb_lower'] = bb_lower
    df['bb_width'] = (bb_upper - bb_lower) / bb_middle
    
    df['atr'] = calculate_atr(df['High'], df['Low'], df['Close'])
    
    # Time features
    df['day_of_week'] = df.index.dayofweek
    df['day_of_month'] = df.index.day
    df['month'] = df.index.month
    df['quarter'] = df.index.quarter
    
    return df.dropna()

def train_random_forest_sequential(data, forecast_days=5):
    """
    Random Forest con previsioni sequenziali (diverse per ogni giorno)
    """
    try:
        df = prepare_ml_features_improved(data)
        
        if len(df) < 50:
            return None, None
        
        forecasts = []
        confidence_scores = []
        
        # Addestra un modello per ogni giorno futuro (previsione ricorsiva)
        current_data = df.copy()
        last_price = float(data['Close'].iloc[-1])
        
        for day in range(1, forecast_days + 1):
            # Target: prezzo futuro a day giorni
            df['target'] = df['Close'].shift(-day)
            df_model = df.dropna()
            
            if len(df_model) < 30:
                break
            
            # Features
            feature_cols = [col for col in df_model.columns 
                           if col not in ['Close', 'target', 'Open', 'High', 'Low', 'Volume']]
            X = df_model[feature_cols].values
            y = df_model['target'].values
            
            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42 + day
            )
            
            # Addestra modello
            model = RandomForestRegressor(
                n_estimators=100, 
                max_depth=10, 
                random_state=42 + day,
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            
            # Valuta accuratezza
            score = model.score(X_test, y_test)
            confidence_scores.append(max(0, min(100, (score + 1) * 50)))
            
            # Previsione per questo giorno
            last_features = X[-1:].reshape(1, -1)
            pred_price = model.predict(last_features)[0]
            
            # Se la previsione è troppo estrema, la aggiustiamo
            max_change = last_price * 0.1  # max 10% change
            if abs(pred_price - last_price) > max_change:
                pred_price = last_price + (max_change if pred_price > last_price else -max_change)
            
            forecasts.append({
                'day': day,
                'price': pred_price,
                'change_pct': ((pred_price / last_price) - 1) * 100
            })
        
        if not forecasts:
            return None
        
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 70
        direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
        
        return {
            'method': 'random_forest_sequential',
            'forecasts': forecasts,
            'confidence': avg_confidence,
            'direction': direction
        }
        
    except Exception as e:
        st.error(f"Errore Random Forest: {str(e)}")
        return None

def train_lstm_model(data, forecast_days=5, lookback=20):
    """
    LSTM per previsioni serie temporali (TensorFlow/Keras)
    """
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from tensorflow.keras.callbacks import EarlyStopping
        
        # Prepara dati
        prices = data['Close'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_prices = scaler.fit_transform(prices)
        
        # Crea sequenze
        X, y = [], []
        for i in range(lookback, len(scaled_prices) - forecast_days):
            X.append(scaled_prices[i-lookback:i, 0])
            y.append(scaled_prices[i:i+forecast_days, 0])
        
        X, y = np.array(X), np.array(y)
        
        if len(X) < 20:
            return None
        
        # Reshape per LSTM [samples, timesteps, features]
        X = X.reshape(X.shape[0], X.shape[1], 1)
        
        # Train/test split
        split = int(len(X) * 0.8)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # Costruisci modello LSTM
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(lookback, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(forecast_days)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # Early stopping
        early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        # Addestra
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_data=(X_test, y_test),
            callbacks=[early_stop],
            verbose=0
        )
        
        # Valuta
        train_loss = model.evaluate(X_train, y_train, verbose=0)
        test_loss = model.evaluate(X_test, y_test, verbose=0)
        
        # Previsione
        last_sequence = scaled_prices[-lookback:].reshape(1, lookback, 1)
        scaled_forecast = model.predict(last_sequence, verbose=0)[0]
        
        # Inverti scaling
        forecast_prices = scaler.inverse_transform(scaled_forecast.reshape(-1, 1)).flatten()
        
        # Calcola confidence basata su errori
        confidence = 100 * (1 - min(1, test_loss[0] / np.var(scaled_prices)))
        
        last_price = float(data['Close'].iloc[-1])
        forecasts = []
        
        for i, price in enumerate(forecast_prices):
            forecasts.append({
                'day': i + 1,
                'price': price,
                'change_pct': ((price / last_price) - 1) * 100
            })
        
        direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
        
        return {
            'method': 'lstm',
            'forecasts': forecasts,
            'confidence': confidence,
            'direction': direction
        }
        
    except Exception as e:
        st.warning(f"LSTM non disponibile: {str(e)}")
        return None

def train_prophet_improved(data, forecast_days=5):
    """
    Prophet con previsioni giornaliere realistiche
    """
    try:
        # Prepara dati per Prophet
        df_prophet = pd.DataFrame({
            'ds': data.index,
            'y': data['Close'].values
        })
        
        # Configura Prophet con seasonality
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10
        )
        
        # Aggiungi regressor esterni se disponibili
        if 'Volume' in data.columns:
            model.add_regressor('volume')
            df_prophet['volume'] = data['Volume'].values
        
        model.fit(df_prophet)
        
        # Previsioni future
        future = model.make_future_dataframe(periods=forecast_days)
        
        if 'volume' in df_prophet.columns:
            # Usa volume medio per future
            future['volume'] = data['Volume'].mean()
        
        forecast = model.predict(future)
        
        # Estrai previsioni
        last_price = float(data['Close'].iloc[-1])
        forecasts = []
        
        for i in range(1, forecast_days + 1):
            pred_price = float(forecast['yhat'].iloc[-forecast_days + i - 1])
            
            # Calcola intervallo di confidenza come misura di confidence
            yhat_lower = float(forecast['yhat_lower'].iloc[-forecast_days + i - 1])
            yhat_upper = float(forecast['yhat_upper'].iloc[-forecast_days + i - 1])
            
            # Più stretto è l'intervallo, più alta la confidence
            interval_width = (yhat_upper - yhat_lower) / pred_price
            confidence = max(50, min(95, 100 - interval_width * 100))
            
            forecasts.append({
                'day': i,
                'price': pred_price,
                'change_pct': ((pred_price / last_price) - 1) * 100,
                'lower_bound': yhat_lower,
                'upper_bound': yhat_upper,
                'confidence': confidence
            })
        
        avg_confidence = np.mean([f['confidence'] for f in forecasts])
        direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
        
        return {
            'method': 'prophet',
            'forecasts': forecasts,
            'confidence': avg_confidence,
            'direction': direction
        }
        
    except Exception as e:
        st.error(f"Errore Prophet: {str(e)}")
        return None

def generate_ml_forecast_improved(data, forecast_days=5, method='ensemble'):
    """
    Genera previsioni ML giornaliere corrette (valori diversi per ogni giorno)
    """
    
    if not ML_AVAILABLE:
        # Simulazione realistica con trend e volatilità
        return generate_simulated_forecast(data, forecast_days)
    
    try:
        if method == 'random_forest':
            return train_random_forest_sequential(data, forecast_days)
        
        elif method == 'lstm':
            return train_lstm_model(data, forecast_days)
        
        elif method == 'prophet':
            return train_prophet_improved(data, forecast_days)
        
        else:  # ensemble
            # Ottieni previsioni da tutti i modelli
            rf_forecast = train_random_forest_sequential(data, forecast_days)
            prophet_forecast = train_prophet_improved(data, forecast_days)
            lstm_forecast = train_lstm_model(data, forecast_days) if method == 'ensemble_full' else None
            
            forecasts = []
            models_used = []
            
            # Combina le previsioni giorno per giorno
            for day in range(1, forecast_days + 1):
                day_prices = []
                day_confidences = []
                
                if rf_forecast and len(rf_forecast['forecasts']) >= day:
                    day_prices.append(rf_forecast['forecasts'][day-1]['price'])
                    day_confidences.append(rf_forecast['confidence'])
                    if 'rf' not in models_used:
                        models_used.append('RF')
                
                if prophet_forecast and len(prophet_forecast['forecasts']) >= day:
                    day_prices.append(prophet_forecast['forecasts'][day-1]['price'])
                    day_confidences.append(prophet_forecast['confidence'])
                    if 'Prophet' not in models_used:
                        models_used.append('Prophet')
                
                if lstm_forecast and len(lstm_forecast['forecasts']) >= day:
                    day_prices.append(lstm_forecast['forecasts'][day-1]['price'])
                    day_confidences.append(lstm_forecast['confidence'])
                    if 'LSTM' not in models_used:
                        models_used.append('LSTM')
                
                if day_prices:
                    # Media ponderata per confidenza
                    weights = np.array(day_confidences) / sum(day_confidences)
                    avg_price = np.average(day_prices, weights=weights)
                    
                    forecasts.append({
                        'day': day,
                        'price': avg_price,
                        'change_pct': 0  # Calcolato dopo
                    })
            
            if not forecasts:
                return generate_simulated_forecast(data, forecast_days)
            
            # Calcola change_pct
            last_price = float(data['Close'].iloc[-1])
            for f in forecasts:
                f['change_pct'] = ((f['price'] / last_price) - 1) * 100
            
            avg_confidence = np.mean([rf_forecast['confidence'] if rf_forecast else 70,
                                     prophet_forecast['confidence'] if prophet_forecast else 70])
            
            direction = 'UP' if forecasts[-1]['price'] > last_price else 'DOWN'
            
            return {
                'method': f"ensemble ({', '.join(models_used)})",
                'forecasts': forecasts,
                'confidence': avg_confidence,
                'direction': direction
            }
            
    except Exception as e:
        st.warning(f"Errore ML: {str(e)}. Uso simulazione.")
        return generate_simulated_forecast(data, forecast_days)

def generate_simulated_forecast(data, forecast_days=5):
    """
    Genera previsioni simulate realistiche (diverse per ogni giorno)
    """
    last_price = float(data['Close'].iloc[-1])
    
    # Calcola trend e volatilità dai dati storici
    returns = data['Close'].pct_change().dropna()
    avg_return = returns.mean() * forecast_days  # Trend medio
    volatility = returns.std() * np.sqrt(forecast_days / 252)  # Volatilità annualizzata
    
    # Genera prezzi con mean reversion e trend
    forecasts = []
    current_price = last_price
    
    for day in range(1, forecast_days + 1):
        # Random walk with drift e mean reversion
        drift = avg_return / forecast_days
        random_shock = np.random.normal(0, volatility / np.sqrt(forecast_days))
        
        # Mean reversion (tende a tornare verso la media)
        mean_price = last_price * (1 + avg_return * day / forecast_days)
        reversion = 0.1 * (mean_price - current_price) / day
        
        price_change = current_price * (drift + random_shock) + reversion
        new_price = current_price + price_change
        
        # Limita cambiamenti estremi
        max_change = last_price * 0.05  # Max 5% al giorno
        if abs(new_price - current_price) > max_change:
            new_price = current_price + (max_change if new_price > current_price else -max_change)
        
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
