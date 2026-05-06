import plotly.graph_objects as go
from plotly.subplots import make_subplots


def vizualiziraj_rezultate(rezultati):
    """
    Ustvari interaktivni graf z dvema podgrafoma:
    1. Gibanje cene delnice + signali za nakup/prodajo
    2. Rast portfelja (Equity Curve)
    """
    
    # Pridobimo DataFrame iz rezultatov backtesta
    df = rezultati['podatki']
    
    # 1. PRIPRAVA PODGRAFOV (2 vrstici, 1 stolpec)
    # shared_xaxes=True pomeni, da se datumi na spodnjem grafu 
    # ujemajo z zgornjim (ko zumiraš enega, zumiraš oba).
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,  # Majhen razmik med grafoma
        row_heights=[0.6, 0.4], # Zgornji graf je malo višji
        subplot_titles=('Cena delnice & Signali', 'Rast portfelja (Equity)')
    )

    # =========================================================================
    # GRAF 1: CENA DELNICE (Zgornji del)
    # =========================================================================
    
    # Dodamo črto za zapiralno ceno (Close)
    fig.add_trace(
        go.Scatter(
            x=df.index,          # Datum na X osi
            y=df['Close'],       # Cena na Y osi
            name='Zapiralna cena',
            line=dict(color='blue', width=2)
        ),
        row=1, col=1
    )

    # Filtriramo trenutke, ko je SIGNAL = 1.0 (Nakup)
    # To so točke, kjer strategija svetuje nakup
    nakupi = df[df['signal'] == 1.0]
    
    # Dodamo zelene trikotnike za signale nakupa
    fig.add_trace(
        go.Scatter(
            x=nakupi.index,
            y=nakupi['Close'],
            mode='markers',
            name='Signal: KUPI',
            marker=dict(
                symbol='triangle-up',  # Simbol: trikotnik gor
                size=12,
                color='green'
            )
        ),
        row=1, col=1
    )

    # Filtriramo trenutke, ko je SIGNAL = 0.0 (Izhod/Prodaja)
    # V naši strategiji je 0.0 pomenilo 'flat' (brez pozicije)
    izhodi = df[df['signal'] == 0.0]
    
    # Dodamo rdeče trikotnike za signale izhoda
    fig.add_trace(
        go.Scatter(
            x=izhodi.index,
            y=izhodi['Close'],
            mode='markers',
            name='Signal: PRODAJ/IZHOD',
            marker=dict(
                symbol='triangle-down', # Simbol: trikotnik dol
                size=12,
                color='red'
            )
        ),
        row=1, col=1
    )

    # =========================================================================
    # GRAF 2: EQUITY CURVE (Spodnji del)
    # =========================================================================
    
    # Dodamo črto rasti računa
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['stanje'],
            name='Stanje računa',
            line=dict(color='green', width=2),
            fill='tozeroy' # Zapolni prostor pod črto do osi X
        ),
        row=2, col=1
    )
    
    # Dodamo črtkano črto za začetni kapital (referenčna točka)
    fig.add_hline(
        y=rezultati['koncno_stanje'] / (1 + df['P/L'].iloc[0]), # Približek začetnega
        line_dash="dash", 
        line_color="gray",
        annotation_text="Začetni kapital",
        row=2, col=1
    )

    # =========================================================================
    # UREJANJE IZGLEDA (LAYOUT)
    # =========================================================================
    
    fig.update_layout(
        title={
            'text': "Rezultati Backtesta",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center'
        },
        height=800,         # Višina grafa v slikovnih pikah
        template='plotly_white', # Čist, bel dizajn
        hovermode='x unified'    # KLJUČNO: Prikaži info za vse grafe naenkrat na določen datum
    )
    
    # Imena osi
    fig.update_yaxes(title_text="Cena ($)", row=1, col=1)
    fig.update_yaxes(title_text="Stanje ($)", row=2, col=1)
    fig.update_xaxes(title_text="Datum", row=2, col=1)

    # PRIKAŽI GRAF V BRSKALNIKU
    fig.show()