"use client";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";
import {
  TrendingUp, TrendingDown, DollarSign, ShoppingCart,
  Users, Package, ArrowRight, Plus, RefreshCw, Eye, CheckCircle, Clock
} from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { useToast } from "@/components/Toast";

const revenueData = [
  { month: "Sep", revenue: 38000, expenses: 22000 },
  { month: "Oct", revenue: 44000, expenses: 26000 },
  { month: "Nov", revenue: 61000, expenses: 31000 },
  { month: "Dec", revenue: 89000, expenses: 42000 },
  { month: "Jan", revenue: 72000, expenses: 34000 },
  { month: "Feb", revenue: 83000, expenses: 38000 },
  { month: "Mar", revenue: 97420, expenses: 45800 },
];

const categoryData = [
  { name: "Electronics", value: 38, color: "#6366F1" },
  { name: "Apparel", value: 22, color: "#06B6D4" },
  { name: "Home & Kitchen", value: 18, color: "#10B981" },
  { name: "Beauty", value: 13, color: "#F59E0B" },
  { name: "Sports", value: 9, color: "#8B5CF6" },
];

const initialOrders = [
  { id: "#RS-9041", customer: "Amelia Johnson", product: "Sony WH-1000XM5", amount: "$349", status: "completed", time: "2 min ago" },
  { id: "#RS-9040", customer: "Marcus Wright", product: "iPhone 15 Pro 256GB", amount: "$1,199", status: "processing", time: "15 min ago" },
  { id: "#RS-9039", customer: "Priya Sharma", product: "Nike Air Max 2024", amount: "$189", status: "shipped", time: "1 hr ago" },
  { id: "#RS-9038", customer: "Ethan Cole", product: "Dyson V15 Detect", amount: "$749", status: "completed", time: "2 hr ago" },
  { id: "#RS-9037", customer: "Sofia Laurent", product: "MacBook Air M3", amount: "$1,299", status: "pending", time: "3 hr ago" },
];

const activities = [
  { icon: "🛒", text: <><strong>Order #RS-9041</strong> placed by Amelia Johnson — $349</>, time: "2 min ago", color: "rgba(99,102,241,0.15)" },
  { icon: "⚠️", text: <><strong>Low stock alert:</strong> AirPods Pro (Gen 3) — only 4 units left</>, time: "18 min ago", color: "rgba(245,158,11,0.15)" },
  { icon: "👤", text: <><strong>New customer</strong> Sofia Laurent registered via mobile app</>, time: "1 hr ago", color: "rgba(16,185,129,0.15)" },
  { icon: "💰", text: <><strong>Payment confirmed</strong> $3,840 from Zenith Retail Ltd</>, time: "2 hr ago", color: "rgba(6,182,212,0.15)" },
  { icon: "📦", text: <><strong>Shipment dispatched</strong> for orders #RS-9035 and #RS-9036</>, time: "3 hr ago", color: "rgba(139,92,246,0.15)" },
  { icon: "🔄", text: <><strong>Refund processed</strong> $189 for order #RS-9029 (size issue)</>, time: "4 hr ago", color: "rgba(239,68,68,0.15)" },
];

const statusStyles: Record<string, string> = {
  completed: "badge-success", processing: "badge-primary", shipped: "badge-info", pending: "badge-warning"
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload?.length) return (
    <div style={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 12, padding: "0.75rem 1rem", fontSize: "0.8rem" }}>
      <p style={{ color: "var(--text-secondary)", marginBottom: 6 }}>{label}</p>
      {payload.map((p: any) => <p key={p.name} style={{ color: p.color, fontWeight: 600 }}>{p.name}: ${p.value.toLocaleString()}</p>)}
    </div>
  );
  return null;
};

export default function DashboardPage() {
  const { toast } = useToast();
  const [orders, setOrders] = useState(initialOrders);
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => {
      setRefreshing(false);
      toast("success", "Dashboard refreshed", "All metrics are up to date.");
    }, 1200);
  };

  const markComplete = (id: string) => {
    setOrders(o => o.map(order => order.id === id ? { ...order, status: "completed" } : order));
    toast("success", "Order updated", `${id} marked as completed.`);
  };

  return (
    <div className="page-container">
      {/* Header */}
      <div className="page-header">
        <div className="page-header-left">
          <h1>Welcome back, Admin 👋</h1>
          <p>Here&apos;s what&apos;s happening at <strong>Revilo Store</strong> today — <span style={{ color: "var(--accent-primary)" }}>Sunday, 8 Mar 2026</span>.</p>
        </div>
        <div className="page-header-actions">
          <button className="btn btn-secondary" onClick={handleRefresh} id="refresh-dashboard-btn" disabled={refreshing}>
            <RefreshCw size={15} style={{ animation: refreshing ? "spin-slow 1s linear infinite" : undefined }} />
            {refreshing ? "Refreshing…" : "Refresh"}
          </button>
          <Link href="/sales" className="btn btn-primary" id="new-order-btn"><Plus size={15} />New Order</Link>
        </div>
      </div>

      {/* Quick stat chips */}
      <div className="stat-strip" style={{ marginBottom: "1.75rem" }}>
        <div className="stat-strip-inner">
          {[
            { label: "Avg Order Value", value: "$75.80", dot: "#6366F1" },
            { label: "Conversion Rate", value: "4.2%", dot: "#10B981" },
            { label: "Gross Margin", value: "53.1%", dot: "#06B6D4" },
            { label: "Refund Rate", value: "1.1%", dot: "#F59E0B" },
            { label: "Cart Abandon", value: "26.4%", dot: "#EF4444" },
            { label: "Active Users Today", value: "1,842", dot: "#8B5CF6" },
            { label: "Loyalty Members", value: "4,130", dot: "#10B981" },
          ].map(chip => (
            <div className="stat-chip" key={chip.label}>
              <div className="stat-chip-dot" style={{ background: chip.dot }} />
              {chip.label}: <span className="stat-chip-value">{chip.value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid">
        <div className="kpi-card indigo" id="kpi-revenue">
          <div className="kpi-top"><div className="kpi-icon indigo"><DollarSign size={20} /></div><div className="kpi-trend up"><TrendingUp size={12} />+21.4%</div></div>
          <div className="kpi-value">$97,420</div>
          <div className="kpi-label">Monthly Revenue</div>
        </div>
        <div className="kpi-card teal" id="kpi-orders">
          <div className="kpi-top"><div className="kpi-icon teal"><ShoppingCart size={20} /></div><div className="kpi-trend up"><TrendingUp size={12} />+9.2%</div></div>
          <div className="kpi-value">1,842</div>
          <div className="kpi-label">Total Orders</div>
        </div>
        <div className="kpi-card amber" id="kpi-customers">
          <div className="kpi-top"><div className="kpi-icon amber"><Users size={20} /></div><div className="kpi-trend up"><TrendingUp size={12} />+14.7%</div></div>
          <div className="kpi-value">12,340</div>
          <div className="kpi-label">Total Customers</div>
        </div>
        <div className="kpi-card rose" id="kpi-inventory">
          <div className="kpi-top"><div className="kpi-icon rose"><Package size={20} /></div><div className="kpi-trend down"><TrendingDown size={12} />-2.3%</div></div>
          <div className="kpi-value">4,218</div>
          <div className="kpi-label">SKUs in Stock</div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-wrapper">
          <div className="chart-header">
            <div>
              <div className="chart-title">Revenue vs Expenses</div>
              <div className="chart-subtitle">Last 7 months — Revilo Store</div>
            </div>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
              <span style={{ display: "flex", alignItems: "center", gap: 5, fontSize: "0.78rem", color: "var(--text-secondary)" }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: "#6366F1", display: "inline-block" }} />Revenue
              </span>
              <span style={{ display: "flex", alignItems: "center", gap: 5, fontSize: "0.78rem", color: "var(--text-secondary)" }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: "#EF4444", display: "inline-block" }} />Expenses
              </span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={revenueData} margin={{ top: 5, right: 5, left: 5, bottom: 0 }}>
              <defs>
                <linearGradient id="gradRevenue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366F1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gradExpenses" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="month" tick={{ fill: "#475569", fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={v => `$${v / 1000}k`} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="revenue" name="Revenue" stroke="#6366F1" strokeWidth={2} fill="url(#gradRevenue)" dot={false} />
              <Area type="monotone" dataKey="expenses" name="Expenses" stroke="#EF4444" strokeWidth={2} fill="url(#gradExpenses)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-wrapper">
          <div className="chart-header">
            <div>
              <div className="chart-title">Sales by Category</div>
              <div className="chart-subtitle">Current month distribution</div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={categoryData} cx="50%" cy="50%" innerRadius={50} outerRadius={75} dataKey="value" strokeWidth={0}>
                {categoryData.map(entry => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip formatter={(v: any) => [`${v}%`, ""]} contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10 }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="legend-list" style={{ marginTop: "0.5rem" }}>
            {categoryData.map(d => (
              <div className="legend-item" key={d.name}>
                <div className="legend-dot" style={{ background: d.color }} />
                <span className="legend-label">{d.name}</span>
                <span className="legend-value">{d.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Orders + Activity */}
      <div className="grid-2">
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <h2 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)" }}>Recent Orders</h2>
            <Link href="/sales" className="btn btn-ghost btn-sm">View all <ArrowRight size={13} /></Link>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr><th>Order</th><th>Customer</th><th>Amount</th><th>Status</th><th>Action</th></tr>
              </thead>
              <tbody>
                {orders.map(o => (
                  <tr key={o.id}>
                    <td className="td-primary td-mono">{o.id}</td>
                    <td>{o.customer}</td>
                    <td className="td-primary">{o.amount}</td>
                    <td><span className={`badge ${statusStyles[o.status] || "badge-muted"}`}><span className="badge-dot" />{o.status}</span></td>
                    <td>
                      {o.status !== "completed" ? (
                        <button
                          onClick={() => markComplete(o.id)}
                          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: 4, fontSize: "0.75rem", padding: "4px 8px", borderRadius: 6, transition: "all 0.2s" }}
                          onMouseEnter={e => { e.currentTarget.style.background = "rgba(16,185,129,0.1)"; e.currentTarget.style.color = "#10B981"; }}
                          onMouseLeave={e => { e.currentTarget.style.background = "none"; e.currentTarget.style.color = "var(--text-muted)"; }}
                        >
                          <CheckCircle size={13} /> Complete
                        </button>
                      ) : (
                        <Link href={`/sales`} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: "0.75rem", color: "var(--text-muted)", textDecoration: "none" }}>
                          <Eye size={13} /> View
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
            <h2 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)" }}>Live Activity</h2>
            <button className="btn btn-ghost btn-sm" onClick={() => toast("info", "Notifications cleared", "All activity marked as read.")}>
              Mark all read
            </button>
          </div>
          <div className="card" style={{ padding: "0.75rem 1.25rem" }}>
            <div className="activity-list">
              {activities.map((a, i) => (
                <div className="activity-item" key={i} style={{ cursor: "pointer" }}
                  onClick={() => toast("info", "Activity detail", `Clicked on activity from ${a.time}`)}
                >
                  <div className="activity-icon" style={{ background: a.color }}>{a.icon}</div>
                  <div className="activity-body">
                    <div className="activity-text">{a.text}</div>
                    <div className="activity-time"><Clock size={10} style={{ display: "inline", marginRight: 3 }} />{a.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
