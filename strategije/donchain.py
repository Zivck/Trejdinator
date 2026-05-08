import pandas as pd
import numpy as np
from .osnovno import OsnovnaStrategija

class Donchian(OsnovnaStrategija):

    def __init__(self, window:int =20, **kwargs):
        super().__init__(ime=f"Donchian({window})")
        self.window= window

    def generiraj_signale(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # zgornji kanal = najvišja cena v oknu  spodnji = najnižja
        df["upper"] =df["High"].rolling(window=self.window).max()
        df["lower"] =df["Low"].rolling(window=self.window).min()

        df["signal"] = np.where(df["Close"]> df["upper"].shift(1), 1.0, 0.0) #no cheating
        return df