import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class EMA_Crossover(OsnovnaStrategija):
    def __init__(self, hitro:int= 12, pocasno:int= 26, **kwargs):
        super().__init__(ime=f"EMA({hitro}/{pocasno})")
        self.hitro =hitro
        self.pocasno =pocasno

    def generiraj_signale(self, df: pd.DataFrame)-> pd.DataFrame:
        df=df.copy

        df['ema_hitro'] =df['Close'].ewm(span=self.hitro, adjust=False).mean()
        df['ema_pocasno'] =df['Close'].ewm(span=self.pocasno, adjust=False).mean()

        df['signal'] = np.where(df['ema_hitro']> df['ema_pocasno'], 1.0, 0.0)
        return df


        