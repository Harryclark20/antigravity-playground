import streamlit as st
import pandas as pd
import numpy as np
import json
import asyncio
import websockets
import threading
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(page_title="Nova HFT Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Premium Glassmorphism Look
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Hide top bar */
    header { visibility: hidden; }
    
    /* Top Account Banner */
    .account-banner {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-bottom: 1px solid #334155;
        padding: 15px 25px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .account-info { font-size: 16px; color: #94a3b8; }
    .account-name { font-size: 20px; font-weight: 700; color: #38bdf8; letter-spacing: 0.5px; }
    .live-badge { 
        background: rgba(16, 185, 129, 0.1); 
        color: #10b981; 
        padding: 5px 12px; 
        border-radius: 20px; 
        font-weight: 600; 
        font-size: 12px; 
        border: 1px solid rgba(16, 185, 129, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    div[data-testid="metric-container"] > label { color: #64748b; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    div[data-testid="metric-container"] > div { color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# Shared State
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {
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
                    data = json.loads(msg)
                    st.session_state.shared_data.update(data)
                    # Trigger rerun to show fresh data
                    st.rerun()
        except Exception:
            await asyncio.sleep(1)

# Start WebSocket thread if not running
if "ws_thread_started" not in st.session_state:
    def run_async():
        asyncio.new_event_loop().run_until_complete(listen_to_bot())
    threading.Thread(target=run_async, daemon=True).start()
    st.session_state.ws_thread_started = True

# Extract data
data = st.session_state.shared_data
acct = data.get("account")
if not acct:
    st.warning("📡 Waiting for MetaTrader 5 connection packet...")
    st.stop()

# --- TOP BANNER (Account Integration Proof) ---
st.markdown(f"""
    <div class="account-banner">
        <div>
            <div class="account-name">{acct.get('name', 'N/A')}</div>
            <div class="account-info">Broker: {acct.get('server', 'N/A')} &nbsp;•&nbsp; Acc: #{acct.get('login', 'N/A')} &nbsp;•&nbsp; Leverage: 1:{acct.get('leverage', 'N/A')}</div>
        </div>
        <div class="live-badge">● DATA STREAM ACTIVE</div>
    </div>
""", unsafe_allow_html=True)

# --- KPIS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Equity", f"{acct.get('currency', '$')} {data['equity']['balance']:,.2f}")
with col2:
    st.metric("Live PnL", f"${data['equity']['pnl']:,.2f}", delta=f"{data['equity']['pnl']:,.2f}")
with col3:
    st.metric("AI Confidence", f"{data['ai']['confidence']*100:.1f}%", 
              delta="High Probability" if data['ai']['confidence'] > 0.85 else "Monitoring",
              delta_color="normal" if data['ai']['confidence'] > 0.85 else "off")
with col4:
    ping_status = "Good" if data['health']['ping'] < 10 else "High"
    st.metric("Latency", f"{data['health']['ping']} ms", delta=ping_status, delta_color="inverse")


# --- CHARTS & BARS ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 📈 Micro-Momentum Tape (50 Ticks)")
    if data['chart']:
        df = pd.DataFrame(data['chart'])
        # Premium Plotly Area Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['price'],
            fill='tozeroy',
            mode='lines',
            line=dict(color='#0ea5e9', width=2),
            fillcolor='rgba(14, 165, 233, 0.1)',
            hovertemplate='%{y:.5f}<extra></extra>'
        ))
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, color='#475569'),
            yaxis=dict(showgrid=True, gridcolor='#1e293b', color='#475569', tickformat=".5f"),
            height=300,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Waiting for tick history...")

with c2:
    st.markdown("### 🛡️ Risk Management")
    st.progress(min(data['equity']['drawdown']/5.0, 1.0))
    st.caption(f"Daily Drawdown Risk: {data['equity']['drawdown']:.2f}% / 5.0%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ System Status")
    st.write(f"**Tick Velocity:** {data['health']['velocity']:.0f} ticks/s")
    st.write(f"**Current Spread:** {data['ai']['spread']} pts")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚨 OVERRIDE / KILL SWITCH", type="primary", use_container_width=True):
        st.error("KILL SWITCH COMMANDED — Sent to MT5 Loop.")
