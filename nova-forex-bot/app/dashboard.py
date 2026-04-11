import streamlit as st
import pandas as pd
import json
import asyncio
import websockets
import threading
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(page_title="Nova HFT | Institutional Interface", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Ultra-Premium Institutional Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

    /* Background and global font */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #0b1121 0%, #04060c 80%);
        font-family: 'Space Grotesk', sans-serif;
        color: #cbd5e1;
    }

    /* Hide default Streamlit header/footer */
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* Custom Top Navigation Banner */
    .nav-banner {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    
    .logo-container {
        display: flex;
        align-items: baseline;
        gap: 15px;
    }

    .logo-text {
        font-size: 26px;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1.5px;
        margin: 0;
    }
    
    .account-meta {
        color: #64748b;
        font-size: 14px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* Status Pill Animation */
    .status-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Metric Cards Customization */
    div[data-testid="metric-container"] {
        background: rgba(17, 24, 39, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 16px !important;
        padding: 24px 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stMetricValue"] div {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-shadow: 0px 0px 20px rgba(255, 255, 255, 0.1) !important;
    }

    /* Kill Switch Button */
    .stButton>button {
        background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 25px 15px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.2) !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%) !important;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    h3 {
        font-weight: 400;
        font-size: 1.2rem;
        color: #94a3b8;
        letter-spacing: 0.5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Shared State
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {
        "symbol": "None",
        "account": None,
        "health": {"ping": 0, "velocity": 0.0},
        "equity": {"balance": 0.0, "drawdown": 0.0, "pnl": 0.0},
        "ai": {"confidence": 0.0, "spread": 0},
        "chart": []
    }

# --- WEBSOCKET CLIENT ---
async def listen_to_bot():
    uri = "ws://127.0.0.1:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    msg = await websocket.recv()
                    st.session_state.shared_data.update(json.loads(msg))
                    st.rerun()
        except Exception:
            await asyncio.sleep(1)

# Start WebSocket thread if not running
if "ws_thread_started" not in st.session_state:
    def run_async():
        asyncio.new_event_loop().run_until_complete(listen_to_bot())
    threading.Thread(target=run_async, daemon=True).start()
    st.session_state.ws_thread_started = True

# Data References
data = st.session_state.shared_data
acct = data.get("account")

# Loader if no MT5 connection yet
if not acct:
    st.markdown("""
        <div style="height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div style="width: 50px; height: 50px; border: 3px solid rgba(56, 189, 248, 0.1); border-top-color: #38bdf8; border-radius: 50%; animation: spin 1s infinite linear;"></div>
            <h2 style="color: #94a3b8; margin-top: 20px; font-weight: 300;">Awaiting MetaTrader 5 Uplink...</h2>
            <style>@keyframes spin {100% {transform: rotate(360deg);}}</style>
        </div>
    """, unsafe_allow_html=True)
    st.stop()
    import sys
    sys.exit(0)



# --- 1. GLOBAL NAVIGATION BANNER ---
st.markdown(f"""
    <div class="nav-banner">
        <div class="logo-container">
            <h1 class="logo-text">NOVA HFT</h1>
            <span class="account-meta">| &nbsp; {acct.get('name', 'N/A')} &nbsp;•&nbsp; {acct.get('server', 'N/A')} &nbsp;•&nbsp; ID: {acct.get('login', 'N/A')} &nbsp;•&nbsp; Leverage: 1:{acct.get('leverage', 'N/A')}</span>
        </div>
        <div class="status-pill">
            <div class="status-dot"></div>
            DATA STREAM LIVE
        </div>
    </div>
""", unsafe_allow_html=True)


# --- 2. KPI METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Equity", f"{acct.get('currency', '$')} {data['equity']['balance']:,.2f}")
with col2:
    st.metric("Unrealized PnL", f"${data['equity']['pnl']:,.2f}", delta=f"{data['equity']['pnl']:,.2f}")
with col3:
    st.metric(f"AI Conf: {data.get('symbol', 'None')}", f"{data['ai']['confidence']*100:.1f}%", 
              delta="High Conviction" if data['ai']['confidence'] > 0.85 else "Monitoring",
              delta_color="normal" if data['ai']['confidence'] > 0.85 else "off")
with col4:
    ping_status = "Excellent" if data['health']['ping'] < 10 else "Sub-Optimal"
    st.metric("Broker Latency", f"{data['health']['ping']} ms", delta=ping_status, delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# --- 3. CHARTS & SYSTEM DIAGNOSTICS DECK ---
c1, c2 = st.columns([2.5, 1])

with c1:
    st.markdown(f"### 📈 Micro-Structure Tape: {data.get('symbol', 'None')}")
    if data['chart']:
        df = pd.DataFrame(data['chart'])
        
        # Ultra-Premium Plotly Glow Line Chart
        fig = go.Figure()
        
        # Glow Effect Layer
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['price'],
            mode='lines',
            line=dict(color='rgba(56, 189, 248, 0.3)', width=10),
            hoverinfo='skip'
        ))
        
        # Main Line
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['price'],
            fill='tozeroy',
            mode='lines',
            line=dict(color='#38bdf8', width=2),
            fillcolor='rgba(56, 189, 248, 0.05)',
            hovertemplate='Price: <b>%{y:.5f}</b><extra></extra>'
        ))
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, color='#475569', tickfont=dict(color='#64748b')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, tickformat=".5f", tickfont=dict(color='#64748b')),
            height=350,
            hovermode="x unified",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Ingesting tick history...")

with c2:
    st.markdown("### 🛡️ Risk Terminal")
    
    # Progress Bar container custom styling
    st.write(f"**Daily Drawdown Risk:** &nbsp; <span style='color:#f87171;'>{data['equity']['drawdown']:.2f}%</span> / 5.0%", unsafe_allow_html=True)
    st.progress(min(data['equity']['drawdown']/5.0, 1.0))
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Diagnostics")
    
    # Tiny dataframe styling for stats
    diag_html = f"""
    <div style="background: rgba(17, 24, 39, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 15px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #94a3b8;">Tick Velocity</span>
            <span style="color: #fff; font-weight: 600;">{data['health']['velocity']:.0f} t/s</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #94a3b8;">Bid/Ask Spread</span>
            <span style="color: #fff; font-weight: 600;">{data['ai']['spread']} pts</span>
        </div>
    </div>
    """
    st.markdown(diag_html, unsafe_allow_html=True)
    
    # The Big Red Button
    if st.button("🚨 TRIGGER EMERGENCY HALT", use_container_width=True):
        st.empty() # Placeholder for when we connect the UI WS back to the MT5 Engine
        st.markdown("""
            <div style="background: rgba(220, 38, 38, 0.1); border: 1px solid #dc2626; color: #ef4444; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px; font-weight: 600; animation: flash 1s infinite alternate;">
                KILL SWITCH SIGNAL SENT
            </div>
            <style>@keyframes flash { from {opacity:0.5;} to {opacity:1;} }</style>
        """, unsafe_allow_html=True)
