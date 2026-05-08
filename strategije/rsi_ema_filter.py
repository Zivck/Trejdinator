import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class RSI_EMA_Filter(OsnovnaStrategija):

    def __init__(self, rsi_perioda: int = 14, ema_trend: int = 50, ema_entry: int = 20, oversold: float = 35.0, **kwargs):
        super().__init__(ime=f"RSI+EMA({rsi_perioda}/{ema_trend})")
        self.rsi_perioda = rsi_perioda
        self.ema_trend = ema_trend      # Dolgoročni trend filter
        self.ema_entry = ema_entry      # Kratkoročni entry filter
        self.oversold = oversold

    def generiraj_signale(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.ewm(alpha=1/self.rsi_perioda, min_periods=self.rsi_perioda).mean()
        avg_loss = loss.ewm(alpha=1/self.rsi_perioda, min_periods=self.rsi_perioda).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        df['rsi'] = 100 - (100 / (1 + rs))
        df['rsi'] = df['rsi'].fillna(50.0)

        df['ema_dolgorocni'] = df['Close'].ewm(span=self.ema_trend, adjust=False).mean()
        df['ema_kratkorocni'] = df['Close'].ewm(span=self.ema_entry, adjust=False).mean()

        # Signal: RSI < oversold IN (cena > dolgorocni EMA ALI cena > kratkorocni EMA)
        # To omogoča več fleksibilnosti
        trend_ok = df['ema_dolgorocni'] > df['ema_dolgorocni'].shift(5)  # EMA narašča (ni nujno da je cena nad njo)
        df['signal'] = np.where((df['rsi'] < self.oversold) & trend_ok, 1.0, 0.0)
        return df