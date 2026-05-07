import pandas as pd
from strategije.osnovno import OsnovnaStrategija

class BacktestMasina:
    def __init__(self, df:pd.DataFrame, strategija:OsnovnaStrategija, zacetni_kapital: float = 10000.0, provizija:  float= 0.01):

        self.df=df.copy()
        self.strategija= strategija
        self.zacetni_kapital= zacetni_kapital
        self.provizija= provizija # 1% nad trejd
        self.rezultati= {}
    
    def zaženi(self)-> dict:
        df_signali= self.strategija.generiraj_signale(self.df)

        df_signali["pozicija"]= df_signali["signal"].shift(1).fillna(0.0) #Da zamaknemo nakup za eno(kupiš po signalu ne med)

        df_signali["delta_cene"]= df_signali["Close"].pct_change() #V procentih za koliko se je trenutni spremenil od predhodnika

        df_signali["P/L"]= df_signali["pozicija"]* df_signali["delta_cene"] #kot Excel tabela "vektorizacija". Pozicija 1 in trg zraste za 0.1 P=0.1

        št_sprememb_pozicije= df_signali["pozicija"].diff().fillna(0.0).abs() # diff() izračuna razliko med trenutno in prejšno vrstico abs() da ne bo -1

        provizija_trade= št_sprememb_pozicije* self.provizija

        df_signali["P/L"]-= provizija_trade

        df_signali["stanje"]= self.zacetni_kapital* (1 + df_signali["P/L"]).cumprod() #cumprod() 10000 +1%, 10100 +2%, 10302 -3% = 9,992.94 nisi na nuli ampak mal manj

        self.rezultati= {
            "podatki": df_signali,
            "koncno_stanje":df_signali["stanje"].iloc[-1] #Potegne zadnje stanje
            } 

        return self.rezultati


        