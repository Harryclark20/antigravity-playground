"use client";
import { useState } from "react";
import { ShoppingCart, TrendingUp, Clock, CheckCircle, Plus, Download, Search } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";

const ordersData = [
    { id: "#ORD-8821", customer: "Olivia Carter", date: "Mar 8, 2026", items: 2, amount: "$2,499", payment: "Visa •••• 4821", status: "completed" },
    { id: "#ORD-8820", customer: "James Thornton", date: "Mar 8, 2026", items: 1, amount: "$349", payment: "PayPal", status: "processing" },
    { id: "#ORD-8819", customer: "Ava Mitchell", date: "Mar 7, 2026", items: 1, amount: "$1,199", payment: "Mastercard •••• 2031", status: "shipped" },
    { id: "#ORD-8818", customer: "Liam Patterson", date: "Mar 7, 2026", items: 3, amount: "$189", payment: "Visa •••• 9102", status: "completed" },
    { id: "#ORD-8817", customer: "Sophia Jenkins", date: "Mar 6, 2026", items: 1, amount: "$599", payment: "Apple Pay", status: "pending" },
    { id: "#ORD-8816", customer: "Noah Williams", date: "Mar 6, 2026", items: 4, amount: "$876", payment: "Visa •••• 3344", status: "completed" },
    { id: "#ORD-8815", customer: "Isabella Brown", date: "Mar 5, 2026", items: 2, amount: "$1,249", payment: "PayPal", status: "shipped" },
    { id: "#ORD-8814", customer: "Mason Davis", date: "Mar 5, 2026", items: 1, amount: "$449", payment: "Mastercard •••• 7890", status: "cancelled" },
    { id: "#ORD-8813", customer: "Emma Wilson", date: "Mar 4, 2026", items: 5, amount: "$2,119", payment: "Visa •••• 5511", status: "completed" },
    { id: "#ORD-8812", customer: "Ethan Harris", date: "Mar 4, 2026", items: 2, amount: "$698", payment: "Bank Transfer", status: "processing" },
];

const trendData = [
    { day: "Mon", orders: 42 }, { day: "Tue", orders: 58 }, { day: "Wed", orders: 71 },
    { day: "Thu", orders: 63 }, { day: "Fri", orders: 84 }, { day: "Sat", orders: 91 }, { day: "Sun", orders: 55 },
];

const statusBadge = (s: string) => {
    const m: Record<string, string> = { completed: "badge-success", processing: "badge-primary", shipped: "badge-info", pending: "badge-warning", cancelled: "badge-danger" };
    return <span className={`badge ${m[s] || "badge-muted"}`}><span className="badge-dot" />{s}</span>;
};

export default function SalesPage() {
    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState("all");

    const filtered = ordersData.filter(o => {
        const ms = o.customer.toLowerCase().includes(search.toLowerCase()) || o.id.toLowerCase().includes(search.toLowerCase());
        const mf = filter === "all" || o.status === filter;
        return ms && mf;
    });

    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Sales & Orders</h1>
                    <p>Track, manage, and fulfill customer orders.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-sales-btn"><Download size={15} />Export</button>
                    <button className="btn btn-primary" id="new-order-btn"><Plus size={15} />New Order</button>
                </div>
            </div>

            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                <div className="kpi-card indigo"><div className="kpi-top"><div className="kpi-icon indigo"><ShoppingCart size={20} /></div></div><div className="kpi-value">1,284</div><div className="kpi-label">Total Orders</div></div>
                <div className="kpi-card teal"><div className="kpi-top"><div className="kpi-icon teal"><CheckCircle size={20} /></div></div><div className="kpi-value">864</div><div className="kpi-label">Completed</div></div>
                <div className="kpi-card amber"><div className="kpi-top"><div className="kpi-icon amber"><Clock size={20} /></div></div><div className="kpi-value">143</div><div className="kpi-label">Pending</div></div>
                <div className="kpi-card rose"><div className="kpi-top"><div className="kpi-icon rose"><TrendingUp size={20} /></div></div><div className="kpi-value">$91.3K</div><div className="kpi-label">Revenue</div></div>
            </div>

            <div className="chart-wrapper" style={{ marginBottom: "1.5rem" }}>
                <div className="chart-header">
                    <div><div className="chart-title">Orders this Week</div><div className="chart-subtitle">Daily order volume</div></div>
                </div>
                <ResponsiveContainer width="100%" height={160}>
                    <LineChart data={trendData}>
                        <XAxis dataKey="day" tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} />
                        <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                        <Line type="monotone" dataKey="orders" stroke="#6366F1" strokeWidth={2.5} dot={{ fill: "#6366F1", r: 4 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="toolbar">
                <div className="toolbar-left">
                    <div className="search-bar">
                        <Search size={15} style={{ color: "var(--text-muted)" }} />
                        <input placeholder="Search order ID or customer..." value={search} onChange={e => setSearch(e.target.value)} id="orders-search" />
                    </div>
                    <div className="filter-tabs">
                        {["all", "completed", "processing", "shipped", "pending", "cancelled"].map(f => (
                            <button key={f} className={`filter-tab${filter === f ? " active" : ""}`} onClick={() => setFilter(f)} id={`sales-filter-${f}`}>
                                {f.charAt(0).toUpperCase() + f.slice(1)}
                            </button>
                        ))}
                    </div>
                </div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{filtered.length} orders</div>
            </div>

            <div className="table-wrapper">
                <table>
                    <thead><tr><th>Order ID</th><th>Customer</th><th>Date</th><th>Items</th><th>Amount</th><th>Payment</th><th>Status</th></tr></thead>
                    <tbody>
                        {filtered.map(o => (
                            <tr key={o.id}>
                                <td className="td-primary td-mono">{o.id}</td>
                                <td className="td-primary">{o.customer}</td>
                                <td>{o.date}</td>
                                <td style={{ textAlign: "center" }}>{o.items}</td>
                                <td className="td-primary" style={{ fontWeight: 700 }}>{o.amount}</td>
                                <td>{o.payment}</td>
                                <td>{statusBadge(o.status)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
