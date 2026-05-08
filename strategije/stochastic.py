import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class Stochastic(OsnovnaStrategija):

    def __init__(self, k_perioda:int= 14, d_perioda:int= 3, oversold:float =20.0, overbought:float =80.0, **kwargs):
        super().__init__(ime=f"Stochastic({k_perioda}/{d_perioda})")
        self.k_period =k_perioda
        self.d_period =d_perioda
        self.oversold =oversold
        self.overbought =overbought

    def generiraj_signale(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        lowest_low =df["Low"].rolling(window=self.k_period).min()
        highest_high =df['High'].rolling(window=self.k_period).max()
        
        # %K = trenutna cena relativno na razpon
        df["k"]= 100* (df["Close"]- lowest_low)/ (highest_high - lowest_low)
        df["k"]= df["k"].fillna(50.0)  # da se ne bo delil z 0 na začetku
        df["d"]= df["k"].rolling(window=self.d_period).mean()  # %D = glajenje %K

        # detekcija prekucnjenja navzgor (včeraj pod, danes nad)
        cross_up =(df["k"]> df["d"])& (df["k"].shift(1) <= df["d"].shift(1))
        in_oversold =(df["k"]< self.oversold)| (df["d"] < self.oversold)
        
        df["signal"] =np.where(cross_up & in_oversold, 1.0, 0.0)
        return df