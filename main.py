import argparse
import pandas as pd
import datetime
import ccxt
from masina import BacktestMasina
import importlib
import inspect
from strategije.osnovno import OsnovnaStrategija
from izracuni import izracunaj_metrike
from hrana_za_oci import vizualiziraj_rezultate

def nalozi_podatke(simbol: str, borza: str, timeframe: str, zacetek: str, limit: int= 1000  ):
    
    print(f"Povezujem se z {borza.upper()} in prenašam {simbol} ({timeframe})")

    try:
        exchange= getattr(ccxt, borza)({"enableRateLimit": True}) #enableRateLimit da nam ne zablokirajo IP
        zacetek_v_ms=None
        if zacetek:
            zacetek_v_ms= int(datetime.datetime.fromisoformat(zacetek).timestamp()* 1000) #ccxt knjižnica rabi datum v milisekundah 

        ohlcv = exchange.fetch_ohlcv(simbol, timeframe, since=zacetek_v_ms, limit=limit)

        if not ohlcv:
            raise ValueError(f"Ni podatkov za {simbol}. Preveri pravilen vpis")
        
        df = pd.DataFrame(ohlcv, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True) #spremenimo nazaj v UTC
        df.set_index("timestamp", inplace=True)

        stevilski_stolpci = ["Open", "High", "Low", "Close", "Volume"] #Da ni kakšna slučajno str
        df[stevilski_stolpci] = df[stevilski_stolpci].astype(float)

        df.dropna(inplace=True)
        df.sort_index(inplace=True)

        print(f"Naloženo {len(df)} sveč. Od {df.index[0].date()} do {df.index[-1].date()}")
        return df
    
    except ccxt.ExchangeError as e:
        raise RuntimeError(f"Napaka borze {borza}: {e}")
    except Exception as e:
        raise RuntimeError(f"Napaka pri prenosu podatkov: {e}")

def nalozi_strategijo(ime_dttk: str, **kwargs):
    try:
        modul = importlib.import_module(f"strategije.{ime_dttk}")
    except ModuleNotFoundError:
        raise ValueError(f"Datoteka strategije/{ime_dttk}.py ne obstaja.")

    razred_strategije = None
    for ime_attr in dir(modul):
        attr = getattr(modul, ime_attr)
        if inspect.isclass(attr) and issubclass(attr, OsnovnaStrategija) and attr is not OsnovnaStrategija:
            razred_strategije= attr
            break
    
    if razred_strategije is None:
        raise ValueError(f"V strategije/{ime_dttk}.py ni najdenega podrazreda razreda Osnovneastrategija.")
    
    return razred_strategije(**kwargs)


def izpisi_metrike(metrike: dict):
    print("\n"+"="*50)
    print("METRIKE")
    print("="*50)
    for key,value in metrike.items():
        print(f"\n{key}:{value}")
    print("\n"+"="*50)

def main():
    parser = argparse.ArgumentParser(description="TREJDINATOR")
    parser.add_argument("--strategija", type=str, required=True, help="Ime datoteke v mapi strategije/ (npr. sma_crossover, rsi, macd)")
    # Parametri, ki jih lahko uporabijo različne strategije
    parser.add_argument("--kratki", type=int, default=20)
    parser.add_argument("--dolgi", type=int, default=50)
    parser.add_argument("--perioda", type=int, default=14)
    
    parser.add_argument("--simbol", type=str, default="BTC/USDT")
    parser.add_argument("--borza", type=str, default="binance")
    parser.add_argument("--timeframe", type=str, default="1d")
    parser.add_argument("--zacetek", type=str, default=None)
    #Dodatni parametri
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--kapital", type=float, default=10000)
    parser.add_argument("--provizija", type=float, default=0.001)
    parser.add_argument("--brez-grafa", action="store_true")
    
    args = parser.parse_args()    

    df=nalozi_podatke(args.simbol, args.borza, args.timeframe, args.zacetek, args.limit)
    strategija = nalozi_strategijo( args.strategija, kratko_avg=args.kratki, dolgo_avg=args.dolgi, perioda=args.perioda)

    motor = BacktestMasina(df, strategija, args.kapital, args.provizija)
    rezultati = motor.zaženi()
    metrike=izracunaj_metrike(rezultati["podatki"]["stanje"], rezultati["podatki"]["P/L"])
    izpisi_metrike(metrike)

    if not args.brez_grafa:
        vizualiziraj_rezultate(rezultati)

if __name__ == "__main__":
    main() 