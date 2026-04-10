"use client";
import { Download, BarChart3, TrendingUp, Users, Package } from "lucide-react";
import {
    AreaChart, Area, BarChart, Bar, LineChart, Line,
    XAxis, YAxis, ResponsiveContainer, Tooltip, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis
} from "recharts";

const revenueByMonth = [
    { month: "Jan", revenue: 68000 }, { month: "Feb", revenue: 79000 }, { month: "Mar", revenue: 91000 },
    { month: "Apr", revenue: 84000 }, { month: "May", revenue: 97000 }, { month: "Jun", revenue: 110000 },
];

const topProducts = [
    { name: "MacBook Pro 14\"", sales: 142, color: "#6366F1" },
    { name: "iPhone 15 Pro", sales: 231, color: "#06B6D4" },
    { name: "Sony WH-1000XM5", sales: 98, color: "#10B981" },
    { name: "Dyson V15", sales: 67, color: "#F59E0B" },
    { name: "Samsung 65\" QLED", sales: 43, color: "#8B5CF6" },
];

const customerGrowth = [
    { month: "Sep", customers: 6100 }, { month: "Oct", customers: 6480 }, { month: "Nov", customers: 6920 },
    { month: "Dec", customers: 7340 }, { month: "Jan", customers: 7810 }, { month: "Feb", customers: 8141 }, { month: "Mar", customers: 8472 },
];

const performanceData = [
    { subject: "Revenue", A: 91 }, { subject: "Customer Sat", A: 87 }, { subject: "Order Rate", A: 76 },
    { subject: "Inventory", A: 82 }, { subject: "HR", A: 70 }, { subject: "Finance", A: 88 },
];

export default function ReportsPage() {
    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Reports & Analytics</h1>
                    <p>Business intelligence and performance insights.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-reports-btn"><Download size={15} />Export PDF</button>
                    <button className="btn btn-primary" id="generate-report-btn"><BarChart3 size={15} />Generate Report</button>
                </div>
            </div>

            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                <div className="kpi-card indigo"><div className="kpi-top"><div className="kpi-icon indigo"><TrendingUp size={20} /></div></div><div className="kpi-value">$91K</div><div className="kpi-label">Mar Revenue</div></div>
                <div className="kpi-card teal"><div className="kpi-top"><div className="kpi-icon teal"><Users size={20} /></div></div><div className="kpi-value">+331</div><div className="kpi-label">New Customers</div></div>
                <div className="kpi-card amber"><div className="kpi-top"><div className="kpi-icon amber"><Package size={20} /></div></div><div className="kpi-value">581</div><div className="kpi-label">Units Sold</div></div>
                <div className="kpi-card rose"><div className="kpi-top"><div className="kpi-icon rose"><TrendingUp size={20} /></div></div><div className="kpi-value">51.6%</div><div className="kpi-label">Profit Margin</div></div>
            </div>

            <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
                <div className="chart-wrapper">
                    <div className="chart-header"><div><div className="chart-title">6-Month Revenue Forecast</div><div className="chart-subtitle">Projected trend</div></div></div>
                    <ResponsiveContainer width="100%" height={220}>
                        <AreaChart data={revenueByMonth}>
                            <defs>
                                <linearGradient id="gRev6" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#6366F1" stopOpacity={0.35} /><stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="month" tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${v / 1000}k`} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} formatter={(v: any) => [`$${Number(v).toLocaleString()}`, "Revenue"]} />
                            <Area type="monotone" dataKey="revenue" stroke="#6366F1" strokeWidth={2.5} fill="url(#gRev6)" dot={{ fill: "#6366F1", r: 4 }} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
                <div className="chart-wrapper">
                    <div className="chart-header"><div><div className="chart-title">Customer Growth</div><div className="chart-subtitle">7-month trajectory</div></div></div>
                    <ResponsiveContainer width="100%" height={220}>
                        <LineChart data={customerGrowth}>
                            <XAxis dataKey="month" tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `${(v / 1000).toFixed(1)}k`} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                            <Line type="monotone" dataKey="customers" stroke="#06B6D4" strokeWidth={2.5} dot={{ fill: "#06B6D4", r: 4 }} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="grid-2">
                <div className="chart-wrapper">
                    <div className="chart-header"><div><div className="chart-title">Top Products by Units Sold</div><div className="chart-subtitle">March 2026</div></div></div>
                    <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={topProducts} layout="vertical" margin={{ left: 10 }}>
                            <XAxis type="number" tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} />
                            <YAxis type="category" dataKey="name" tick={{ fill: "#94A3B8", fontSize: 11 }} axisLine={false} tickLine={false} width={140} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                            <Bar dataKey="sales" radius={[0, 6, 6, 0]}>
                                {topProducts.map((d, i) => <Cell key={i} fill={d.color} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div className="chart-wrapper">
                    <div className="chart-header"><div><div className="chart-title">Business Health Score</div><div className="chart-subtitle">Across all departments</div></div></div>
                    <ResponsiveContainer width="100%" height={200}>
                        <RadarChart data={performanceData}>
                            <PolarGrid stroke="rgba(255,255,255,0.07)" />
                            <PolarAngleAxis dataKey="subject" tick={{ fill: "#94A3B8", fontSize: 11 }} />
                            <Radar name="Score" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.2} strokeWidth={2} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} formatter={(v: any) => [`${v}/100`, "Score"]} />
                        </RadarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}
