"use client";
import { DollarSign, TrendingUp, TrendingDown, CreditCard, Download, Plus } from "lucide-react";
import {
    AreaChart, Area, BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell
} from "recharts";

const plData = [
    { month: "Sep", revenue: 53000, expenses: 31000, profit: 22000 },
    { month: "Oct", revenue: 48000, expenses: 29000, profit: 19000 },
    { month: "Nov", revenue: 61000, expenses: 35000, profit: 26000 },
    { month: "Dec", revenue: 72000, expenses: 38000, profit: 34000 },
    { month: "Jan", revenue: 68000, expenses: 36000, profit: 32000 },
    { month: "Feb", revenue: 79000, expenses: 41000, profit: 38000 },
    { month: "Mar", revenue: 91000, expenses: 44000, profit: 47000 },
];

const expenses = [
    { cat: "Payroll", amount: 22000, pct: 50, color: "#6366F1" },
    { cat: "Marketing", amount: 8800, pct: 20, color: "#06B6D4" },
    { cat: "Operations", amount: 5720, pct: 13, color: "#10B981" },
    { cat: "Technology", amount: 3960, pct: 9, color: "#F59E0B" },
    { cat: "Other", amount: 3520, pct: 8, color: "#8B5CF6" },
];

const transactions = [
    { id: "TXN-4401", description: "Payment from Zenith Corp", type: "income", amount: "+$4,800", date: "Mar 8, 2026", category: "Sales" },
    { id: "TXN-4400", description: "AWS Monthly Bill", type: "expense", amount: "-$1,240", date: "Mar 8, 2026", category: "Technology" },
    { id: "TXN-4399", description: "Payroll — March Cycle", type: "expense", amount: "-$22,000", date: "Mar 7, 2026", category: "Payroll" },
    { id: "TXN-4398", description: "Payment from Ava Mitchell", type: "income", amount: "+$1,199", date: "Mar 7, 2026", category: "Sales" },
    { id: "TXN-4397", description: "Office Rent — March", type: "expense", amount: "-$3,500", date: "Mar 5, 2026", category: "Operations" },
    { id: "TXN-4396", description: "Google Ads Campaign", type: "expense", amount: "-$2,800", date: "Mar 4, 2026", category: "Marketing" },
    { id: "TXN-4395", description: "Sales Revenue — Week 9", type: "income", amount: "+$28,400", date: "Mar 3, 2026", category: "Sales" },
];

export default function FinancePage() {
    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Finance</h1>
                    <p>Profit & Loss, cash flow, and transaction history.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-finance-btn"><Download size={15} />Export Report</button>
                    <button className="btn btn-primary" id="record-transaction-btn"><Plus size={15} />Record Transaction</button>
                </div>
            </div>

            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                <div className="kpi-card indigo">
                    <div className="kpi-top"><div className="kpi-icon indigo"><DollarSign size={20} /></div><div className="kpi-trend up"><TrendingUp size={12} />+18.2%</div></div>
                    <div className="kpi-value">$91K</div><div className="kpi-label">Monthly Revenue</div>
                </div>
                <div className="kpi-card rose">
                    <div className="kpi-top"><div className="kpi-icon rose"><CreditCard size={20} /></div><div className="kpi-trend down"><TrendingDown size={12} />+7.1%</div></div>
                    <div className="kpi-value">$44K</div><div className="kpi-label">Total Expenses</div>
                </div>
                <div className="kpi-card teal">
                    <div className="kpi-top"><div className="kpi-icon teal"><TrendingUp size={20} /></div><div className="kpi-trend up"><TrendingUp size={12} />+32%</div></div>
                    <div className="kpi-value">$47K</div><div className="kpi-label">Net Profit</div>
                </div>
                <div className="kpi-card amber">
                    <div className="kpi-top"><div className="kpi-icon amber"><DollarSign size={20} /></div></div>
                    <div className="kpi-value">51.6%</div><div className="kpi-label">Profit Margin</div>
                </div>
            </div>

            <div className="charts-grid">
                <div className="chart-wrapper">
                    <div className="chart-header">
                        <div><div className="chart-title">P&L Overview</div><div className="chart-subtitle">7-month trend</div></div>
                    </div>
                    <ResponsiveContainer width="100%" height={220}>
                        <AreaChart data={plData}>
                            <defs>
                                <linearGradient id="gRev" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#6366F1" stopOpacity={0.3} /><stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="gProfit" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} /><stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="month" tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${v / 1000}k`} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                            <Area type="monotone" dataKey="revenue" name="Revenue" stroke="#6366F1" strokeWidth={2} fill="url(#gRev)" dot={false} />
                            <Area type="monotone" dataKey="profit" name="Profit" stroke="#10B981" strokeWidth={2} fill="url(#gProfit)" dot={false} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
                <div className="chart-wrapper">
                    <div className="chart-header">
                        <div><div className="chart-title">Expense Breakdown</div><div className="chart-subtitle">March 2026</div></div>
                    </div>
                    <div style={{ padding: "0.5rem 0" }}>
                        {expenses.map(e => (
                            <div className="stat-bar-item" key={e.cat}>
                                <div className="stat-bar-header">
                                    <span className="stat-bar-label">{e.cat}</span>
                                    <span className="stat-bar-value">${e.amount.toLocaleString()}</span>
                                </div>
                                <div className="stat-bar-track">
                                    <div className="stat-bar-fill" style={{ width: `${e.pct}%`, background: e.color }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div style={{ marginTop: "1.5rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
                    <h2 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)" }}>Recent Transactions</h2>
                    <button className="btn btn-ghost btn-sm">View all</button>
                </div>
                <div className="table-wrapper">
                    <table>
                        <thead><tr><th>Transaction ID</th><th>Description</th><th>Category</th><th>Date</th><th>Amount</th></tr></thead>
                        <tbody>
                            {transactions.map(t => (
                                <tr key={t.id}>
                                    <td className="td-mono">{t.id}</td>
                                    <td className="td-primary">{t.description}</td>
                                    <td><span className="badge badge-muted">{t.category}</span></td>
                                    <td>{t.date}</td>
                                    <td style={{ fontWeight: 700, color: t.type === "income" ? "var(--accent-success)" : "var(--accent-danger)" }}>{t.amount}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
