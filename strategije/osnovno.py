from abc import ABC, abstractmethod
import pandas as pd

class OsnovnaStrategija(ABC):
    
    def __init__(self, ime:str= "OsnovnaStrategija"):
        self.ime = ime
    
    @abstractmethod
    def generiraj_signale(self, df: pd.DataFrame) -> pd.DataFrame:
        """    
        Vrača:
            DataFrame z dodatim 'signal' stolpec:
                1.0 = BUY signal
                0.0 = FLAT (brez pozicije)
                -1.0 = SELL signal
        """
        pass
    
    def __str__(self):
        return self.ime
