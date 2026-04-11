import streamlit as st
import pandas as pd
import numpy as np
import json
import asyncio
import websockets
import threading
from datetime import datetime

# Page Config
st.set_page_config(page_title="Nova HFT Command Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    .status-red { color: #ff4b4b; font-weight: bold; }
    .status-green { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Shared State
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {
        "health": {"ping": 0, "velocity": 0},
        "equity": {"balance": 0.0, "drawdown": 0.0, "pnl": 0.0},
        "ai": {"confidence": 0, "spread": 0},
        "history": []
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
                    # Use a lightweight trigger to refresh
                    st.rerun()
        except Exception:
            await asyncio.sleep(2)

# Start WebSocket thread if not running
if "ws_thread_started" not in st.session_state:
    def run_async():
        asyncio.run(listen_to_bot())
    thread = threading.Thread(target=run_async, daemon=True)
    thread.start()
    st.session_state.ws_thread_started = True

# --- HEADER ---
st.title("🚀 NOVA HFT :: Command Dashboard")
st.divider()

# --- LAYOUT ZONES ---
col1, col2 = st.columns([1, 1])

with col1:
    # ZONE A: System Health
    st.subheader("📡 Zone A: System Health")
    a_col1, a_col2 = st.columns(2)
    
    ping = st.session_state.shared_data["health"]["ping"]
    ping_status = "status-green" if ping < 10 else "status-red"
    a_col1.metric("Broker Ping", f"{ping}ms", delta_color="inverse")
    
    velocity = st.session_state.shared_data["health"]["velocity"]
    a_col2.metric("Tick Velocity", f"{velocity} ticks/s")
    
    # Zone B: Risk & Equity
    st.subheader("💰 Zone B: Risk & Equity")
    b_col1, b_col2 = st.columns(2)
    
    drawdown = st.session_state.shared_data["equity"]["drawdown"]
    b_col1.progress(min(drawdown/3.0, 1.0), text=f"Daily Drawdown: {drawdown:.2f}%")
    
    pnl = st.session_state.shared_data["equity"]["pnl"]
    b_col2.metric("Live Trade PnL", f"${pnl:,.2f}", delta=pnl)

with col2:
    # Zone C: The AI's Mind
    st.subheader("🧠 Zone C: AI Logic Window")
    c_col1, c_col2 = st.columns(2)
    
    confidence = st.session_state.shared_data["ai"]["confidence"]
    c_col1.write(f"### AI Confidence: {confidence*100:.1f}%")
    st.progress(confidence)
    
    spread = st.session_state.shared_data["ai"]["spread"]
    c_col2.metric("Current Spread", f"{spread} pts")

    # Zone D: Emergency Override
    st.subheader("🛑 Zone D: Emergency Override")
    if st.button("🚨 TRIGGER KILL SWITCH", type="primary", use_container_width=True):
        st.error("KILL SWITCH COMMAND SENT TO MT5 LOOP")
        # Send back to bot via websocket (optional refinement)

# --- LIVE CHARTING ---
st.subheader("📊 Momentum Pulse (Last 100 Ticks)")
if st.session_state.shared_data["history"]:
    chart_data = pd.DataFrame(st.session_state.shared_data["history"])
    st.line_chart(chart_data)
else:
    st.info("Waiting for data stream from HFT loop...")
