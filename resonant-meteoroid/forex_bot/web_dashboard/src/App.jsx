import { useState, useEffect } from 'react'
import axios from 'axios'
import './index.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [status, setStatus] = useState({
    connected: false,
    bot_running: false,
    balance: 0.0,
    equity: 0.0,
    active_trades: 0
  })

  const [logs, setLogs] = useState([])
  const [isConnecting, setIsConnecting] = useState(false)

  const [credentials, setCredentials] = useState({
    account: '',
    password: '',
    server: ''
  })

  // Poll status every 2 seconds
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await axios.get(`${API_URL}/api/status`)
        setStatus(res.data)
      } catch (err) {
        // console.error("API offline")
      }
    }

    const fetchLogs = async () => {
      try {
        const res = await axios.get(`${API_URL}/api/logs?lines=20`)
        setLogs(res.data.logs)
      } catch (err) {
        // console.error("API offline")
      }
    }

    fetchStatus()
    fetchLogs()
    const interval = setInterval(() => {
      fetchStatus()
      fetchLogs()
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const handleConnect = async (e) => {
    e.preventDefault()
    setIsConnecting(true)
    console.log("Attempting to connect with:", credentials)
    try {
      const res = await axios.post(`${API_URL}/api/connect`, {
        account: parseInt(credentials.account),
        password: credentials.password,
        server: credentials.server
      })
      console.log("Connection response:", res.data)
      alert("Successfully connected to MetaTrader 5!")
    } catch (err) {
      console.error("Connection error details:", err)
      const errorDetail = err.response?.data?.detail || err.message
      alert(`Connection failed: ${errorDetail}`)
    } finally {
      setIsConnecting(false)
    }
  }

  const handleStart = async () => {
    try {
      await axios.post(`${API_URL}/api/start`)
    } catch (err) {
      alert(`Start failed: ${err.response?.data?.detail || err.message}`)
    }
  }

  const handleStop = async () => {
    try {
      await axios.post(`${API_URL}/api/stop`)
    } catch (err) {
      alert(`Stop failed: ${err.response?.data?.detail || err.message}`)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6 md:p-12 selection:bg-indigo-500/30">

      {/* Header */}
      <header className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl md:text-5xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-cyan-400 to-emerald-400">
            Elite Hybrid Bot
          </h1>
          <p className="text-slate-400 mt-2 font-medium">Autonomous Quantitative Trading Terminal</p>
        </div>

        <div className="flex items-center gap-3 bg-slate-900/50 px-4 py-2 rounded-full border border-slate-800 backdrop-blur-sm">
          <div className={`w-3 h-3 rounded-full ${status.connected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="font-semibold text-sm">
            {status.connected ? 'MT5 Connected' : 'Disconnected'}
          </span>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-12 gap-8">

        {/* Left Column: Controls & Stats */}
        <div className="lg:col-span-4 space-y-8">

          {/* MT5 Login Card */}
          <div className="bg-slate-900/80 backdrop-blur-md rounded-2xl p-6 border border-slate-800 shadow-xl">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <svg className="w-5 h-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Broker Credentials
            </h2>

            <form onSubmit={handleConnect} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold tracking-wider text-slate-500 uppercase mb-1">Account Number</label>
                <input
                  type="text"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
                  placeholder="e.g. 12345678"
                  value={credentials.account}
                  onChange={e => setCredentials({ ...credentials, account: e.target.value })}
                  disabled={status.connected}
                />
              </div>
              <div>
                <label className="block text-xs font-semibold tracking-wider text-slate-500 uppercase mb-1">Password</label>
                <input
                  type="password"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
                  placeholder="••••••••"
                  value={credentials.password}
                  onChange={e => setCredentials({ ...credentials, password: e.target.value })}
                  disabled={status.connected}
                />
              </div>
              <div>
                <label className="block text-xs font-semibold tracking-wider text-slate-500 uppercase mb-1">Server</label>
                <input
                  type="text"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-mono"
                  placeholder="MetaQuotes-Demo"
                  value={credentials.server}
                  onChange={e => setCredentials({ ...credentials, server: e.target.value })}
                  disabled={status.connected}
                />
              </div>
              <button
                type="submit"
                disabled={status.connected || isConnecting}
                className="w-full mt-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold py-3 rounded-lg transition-all shadow-lg shadow-indigo-500/20 active:scale-[0.98]"
              >
                {isConnecting ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Initializing...
                  </span>
                ) : (
                  status.connected ? 'Securely Connected' : 'Initialize Connection'
                )}
              </button>
            </form>
          </div>

          {/* Metrics Card */}
          <div className="bg-slate-900/80 backdrop-blur-md rounded-2xl p-6 border border-slate-800 shadow-xl">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <svg className="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              Live Metrics
            </h2>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <div className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">Balance</div>
                <div className="text-2xl font-mono text-slate-200">
                  ${status.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </div>
              </div>

              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <div className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">Equity</div>
                <div className="text-2xl font-mono text-emerald-400">
                  ${status.equity.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </div>
              </div>
            </div>

            <div className="mt-4 bg-slate-950 border border-slate-800 rounded-xl p-4 flex justify-between items-center">
              <div className="text-slate-500 text-xs font-semibold uppercase tracking-wider">Active Positions</div>
              <div className="text-xl font-mono font-bold text-cyan-400">{status.active_trades}</div>
            </div>
          </div>

        </div>

        {/* Right Column: Engine Control & Logs */}
        <div className="lg:col-span-8 flex flex-col gap-8">

          {/* Engine Controls */}
          <div className="bg-slate-900/80 backdrop-blur-md rounded-2xl p-6 border border-slate-800 shadow-xl flex flex-col md:flex-row gap-6 items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">Trading Engine</h2>
              <p className="text-slate-400 mt-1">Status: <span className={status.bot_running ? "text-emerald-400 font-semibold" : "text-amber-400 font-semibold"}>{status.bot_running ? "ANALYZING MARKETS" : "STANDBY"}</span></p>
            </div>

            <div className="flex gap-4 w-full md:w-auto">
              <button
                onClick={handleStart}
                disabled={!status.connected || status.bot_running}
                className="flex-1 md:flex-none px-8 py-4 rounded-xl font-bold text-white bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-600 shadow-lg shadow-emerald-500/20 transition-all active:scale-[0.98]"
              >
                ENGAGE BOT
              </button>
              <button
                onClick={handleStop}
                disabled={!status.bot_running}
                className="flex-1 md:flex-none px-8 py-4 rounded-xl font-bold text-white bg-red-600 hover:bg-red-500 disabled:bg-slate-800 disabled:text-slate-600 shadow-lg shadow-red-500/20 transition-all active:scale-[0.98]"
              >
                HALT
              </button>
            </div>
          </div>

          {/* Terminal / Logs */}
          <div className="bg-slate-950 rounded-2xl border border-slate-800 shadow-xl flex-1 flex flex-col hidden lg:flex relative overflow-hidden">
            <div className="h-12 border-b border-slate-800 flex items-center px-6 gap-2 bg-slate-900/50">
              <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
              <span className="ml-4 font-mono text-xs text-slate-500 tracking-widest">engine.log</span>
            </div>

            <div className="p-6 font-mono text-sm overflow-auto h-[400px] flex flex-col justify-end">
              <div className="space-y-1.5">
                {logs.length > 0 ? logs.map((log, i) => (
                  <div key={i} className="leading-relaxed whitespace-pre-wrap break-all">
                    {log.includes('INFO') && <span className="text-blue-400">{log}</span>}
                    {log.includes('WARNING') && <span className="text-amber-400">{log}</span>}
                    {log.includes('ERROR') && <span className="text-red-400">{log}</span>}
                    {!log.includes('INFO') && !log.includes('WARNING') && !log.includes('ERROR') && <span className="text-slate-300">{log}</span>}
                  </div>
                )) : (
                  <div className="text-slate-600 animate-pulse">Waiting for engine output...</div>
                )}
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  )
}

export default App
