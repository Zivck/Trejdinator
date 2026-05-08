import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class RSI_EMA_Filter(OsnovnaStrategija):

    def __init__(self, rsi_period: int = 14, ema_period: int = 50, oversold: float = 30.0, **kwargs):
        super().__init__(ime=f"RSI+EMA({rsi_period}/{ema_period})")
        self.rsi_period = rsi_period
        self.ema_period = ema_period
        self.oversold = oversold

    def generisi_signale(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.ewm(alpha=1/self.rsi_period, min_periods=self.rsi_period).mean()
        avg_loss = loss.ewm(alpha=1/self.rsi_period, min_periods=self.rsi_period).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        df['rsi'] = 100 - (100 / (1 + rs))
        df['rsi'] = df['rsi'].fillna(50.0)

        #trend filter 
        df['ema_trend'] = df['Close'].ewm(span=self.ema_period, adjust=False).mean()

        # signal:RSI< oversold IN cena> EMA (dip v uptrendu)
        df['signal'] = np.where((df['rsi'] < self.oversold) & (df['Close'] > df['ema_trend']), 1.0, 0.0)
        return df