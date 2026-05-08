import plotly.graph_objects as go
from plotly.subplots import make_subplots


def vizualiziraj_rezultate(rezultati):
    df = rezultati["podatki"]
    
    # 1. PRIPRAVA PODGRAFOV
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.6, 0.4],
        subplot_titles=("Cena (Candlestick) & Signali", "Rast portfolja (Equity)")
    )


    # GRAF 1: CANDLESTICK CHART z ohlcv podatki
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Cena",
            increasing_line_color="cyan",
            decreasing_line_color="orange"
        ),
        row=1, col=1
    )
    # DETEKCIJA PREHODOV
    # Zagotovimo, da so signali števila(float)
    df["signal"]= df["signal"].astype(float)
    df["prev_signal"]= df["signal"].shift(1).fillna(0.0)

    # LONG: vstop (pozicija postane 1), izhod (pozicija pade iz 1)
    long_vstop = df[(df["signal"]== 1.0) & (df["prev_signal"]!= 1.0)]
    long_izhod = df[(df["signal"]!= 1.0) & (df["prev_signal"]== 1.0)]

    # SHORT: vstop (pozicija postane -1), izhod (pozicija naraste iz -1)
    short_vstop= df[(df["signal"]== -1.0) & (df["prev_signal"]!= -1.0)]
    short_izhod= df[(df["signal"]!= -1.0) & (df["prev_signal"]== -1.0)]

    
    # LONG signali(Zeleni)-> Postavljeni MALO POD ceno (y * 0.99)
    if len(long_vstop)> 0:
        fig.add_trace(
            go.Scatter(x=long_vstop.index, y=long_vstop["Close"] * 0.99, mode="markers",
                       marker=dict(symbol="triangle-up", size=12, color="green"),
                       name='LONG Vstop', showlegend=True),
            row=1, col=1
        )
    if len(long_izhod)> 0:
        fig.add_trace(
            go.Scatter(x=long_izhod.index, y=long_izhod["Close"] * 0.99, mode="markers",
                       marker=dict(symbol="triangle-down", size=12, color="green"),
                       name="LONG Izhod", showlegend=True),
            row=1, col=1
        )

    # SHORT signali(Rdeči)-> Postavljeni MALO NAD ceno (y * 1.01)
    if len(short_vstop)> 0:
        fig.add_trace(
            go.Scatter(x=short_vstop.index, y=short_vstop["Close"] * 1.01, mode="markers",
                       marker=dict(symbol="triangle-down", size=12, color="red"),
                       name="SHORT Vstop", showlegend=True),
            row=1, col=1
        )
    if len(short_izhod)> 0:
        fig.add_trace(
            go.Scatter(x=short_izhod.index, y=short_izhod["Close"] * 1.01, mode="markers",
                       marker=dict(symbol="triangle-up", size=12, color="red"),
                       name="SHORT Izhod", showlegend=True),
            row=1, col=1
        )

    # GRAF 2: EQUITY CURVE
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["stanje"],
            name="Stanje računa",
            line=dict(color="green", width=2),
            fill="tonextx", fillcolor="rgba(0,0,255,0.1)"
        ),
        row=2, col=1
    )
    # LAYOUT
    fig.update_layout(
        title={"text": "Rezultati Backtesta", "y": 0.95, "x": 0.5, "xanchor": "center"},
        height=800,
        template="plotly_white",
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_yaxes(title_text="Cena ($)", row=1, col=1)
    fig.update_yaxes(title_text="Stanje ($)", row=2, col=1)
    fig.update_xaxes(title_text="Datum", row=2, col=1)

    fig.show()