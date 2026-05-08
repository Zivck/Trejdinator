import pandas as pd
import numpy as np

def izracunaj_metrike(stanje_cez_cas: pd.Series, dnevni_profit: pd.Series, obresti_brez_riska: float= 0.02)-> dict:
    if len(dnevni_profit)== 0:
        return prazne_metrike()
    
    if len(dnevni_profit) == 0 or len(stanje_cez_cas) < 2:
        return prazne_metrike()
    
    dnevni_profit=dnevni_profit.dropna()#izbriše Nan vrednosti
    stanje_cez_cas=stanje_cez_cas.dropna()
    
    izkupiček= stanje_cez_cas.iloc[-1]/ stanje_cez_cas.iloc[0]- 1

    leta=len(stanje_cez_cas)/ 365
    izkupiček_v_1y= (stanje_cez_cas.iloc[-1]/ stanje_cez_cas.iloc[0])** (1/leta)- 1 
    volatilnost_v_1y= dnevni_profit.std()* np.sqrt(365) #std() gre čez elemente in vrne povprečno razliko med elemennti

    sharpe_razmerje= (izkupiček_v_1y- obresti_brez_riska)/ volatilnost_v_1y if volatilnost_v_1y > 0 else 0.0

    neg_profit= dnevni_profit[dnevni_profit < 0]
    if len(neg_profit) > 0 and neg_profit.std() > 0:
        neg_profit_delta= neg_profit.std()
        sortino_razmerje= (izkupiček_v_1y - obresti_brez_riska) / neg_profit_delta if neg_profit_delta > 0 else 0.0 #Isto kot sharpe samo da ko gre market gor ne odbija
    else:
        sortino_razmerje= 0.0

    tekoci_max= stanje_cez_cas.cummax() #Tekoči maksimum do vsakega dne
    padec= stanje_cez_cas/ tekoci_max -1 #trenutni padec od zadnjega vrha
    padec_max= padec.min() #največji padec

    donos_na_padec= izkupiček_v_1y/ abs(padec_max) if padec_max != 0 else 0.0

    P_dnevi= (dnevni_profit>0).sum() #(dnevni_profit>0) tole vrne True in false oz 1 in 0
    dnevi=len(dnevni_profit)
    win_rate= P_dnevi/dnevi

    profiti= dnevni_profit[dnevni_profit > 0].sum()
    izgube= abs(dnevni_profit[dnevni_profit < 0].sum())
    profit_razmrje= profiti/izgube if izgube > 0 else (999.0 if profiti > 0 else 0.0)

    return {
        'total_return': round(izkupiček, 4),           
        'annualized_return': round(izkupiček_v_1y, 4), 
        'volatility': round(volatilnost_v_1y, 4),               
        'sharpe_ratio': round(sharpe_razmerje, 3),           
        'sortino_ratio': round(sortino_razmerje, 3),         
        'max_drawdown': round(padec_max, 4),          
        'calmar_ratio': round(donos_na_padec, 3),           
        'win_rate': round(win_rate, 4),                   
        'profit_factor': round(profit_razmrje, 3), 
        'num_trades': dnevi,                        
        'best_day': round(dnevni_profit.max(), 4),    
        'worst_day': round(dnevni_profit.min(), 4)
    }


def prazne_metrike():
    return {
        'total_return': 0.0,
        'annualized_return': 0.0,
        'volatility': 0.0,
        'sharpe_ratio': 0.0,
        'sortino_ratio': 0.0,
        'max_drawdown': 0.0,
        'calmar_ratio': 0.0,
        'win_rate': 0.0,
        'profit_factor': 0.0,
        'num_trades': 0,
        'best_day': 0.0,
        'worst_day': 0.0
    }
