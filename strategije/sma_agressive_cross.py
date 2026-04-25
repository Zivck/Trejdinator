import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class SMA_agressivecross(OsnovnaStrategija):
    """
    SMA: simple moving average 
    Crossover: presek
    Logika: ko se kratko povprečje cene povzdigne nad dolgo povprečje BUY signal,
            Obratno SELL signal  
    """
    def __init__(self, kratko_avg: int, dolgo_avg: int):

        super().__init__(ime=f"SMA({kratko_avg}/{dolgo_avg})")
        self.kratko_avg=kratko_avg
        self.dolgo_avg=dolgo_avg

        if self.dolgo_avg <= self.kratko_avg:
            raise ValueError("Kratki avg mora biti manjši od daljšega")
    
    def generiraj_signale(self, df: pd.DataFrame)->pd.DataFrame:
        df=df.copy()
        df["sma_kratki"]= df["Close"].rolling(window=self.kratko_avg).mean()

        df["sma_dolgi"]= df["Close"].rolling(window=self.dolgo_avg).mean()

        df["signal"] = np.where(df["sma_kratki"] > df["sma_dugi"], 1.0,-1.0)

        return df
    