"use client";
import { useState } from "react";
import { Package, AlertTriangle, Plus, Download, Search, Filter } from "lucide-react";
import {
    BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell
} from "recharts";

const products = [
    { id: "PRD-001", name: "MacBook Pro 14\" M3", category: "Electronics", sku: "MBP14-M3-512", stock: 48, reorder: 20, price: "$2,499", status: "in-stock" },
    { id: "PRD-002", name: "iPhone 15 Pro 256GB", category: "Electronics", sku: "IP15P-256-NL", stock: 102, reorder: 30, price: "$1,199", status: "in-stock" },
    { id: "PRD-003", name: "Sony WH-1000XM5", category: "Electronics", sku: "SWHXM5-BLK", stock: 8, reorder: 15, price: "$349", status: "low-stock" },
    { id: "PRD-004", name: "Nike Air Max 270", category: "Footwear", sku: "NAM270-BLK-10", stock: 65, reorder: 25, price: "$189", status: "in-stock" },
    { id: "PRD-005", name: "Dyson V15 Detect", category: "Home", sku: "DYV15-DET", stock: 3, reorder: 10, price: "$599", status: "low-stock" },
    { id: "PRD-006", name: "Levi's 511 Slim", category: "Apparel", sku: "LV511-32-32-IDG", stock: 0, reorder: 20, price: "$79", status: "out-of-stock" },
    { id: "PRD-007", name: "Vitamix A3500", category: "Kitchen", sku: "VMA3500-SLT", stock: 17, reorder: 8, price: "$629", status: "in-stock" },
    { id: "PRD-008", name: 'Samsung 65" QLED', category: "Electronics", sku: "SSG65Q80C", stock: 12, reorder: 5, price: "$1,499", status: "in-stock" },
    { id: "PRD-009", name: "Adidas Ultraboost 23", category: "Footwear", sku: "AUB23-WHT-9", stock: 0, reorder: 20, price: "$189", status: "out-of-stock" },
    { id: "PRD-010", name: "KitchenAid Mixer", category: "Kitchen", sku: "KAM-5QT-RED", stock: 22, reorder: 10, price: "$449", status: "in-stock" },
];

const stockChart = [
    { cat: "Electronics", count: 173 },
    { cat: "Footwear", count: 65 },
    { cat: "Apparel", count: 38 },
    { cat: "Home", count: 20 },
    { cat: "Kitchen", count: 39 },
];

const COLORS = ["#6366F1", "#06B6D4", "#10B981", "#F59E0B", "#8B5CF6"];

const statusBadge = (s: string) => {
    const m: Record<string, string> = { "in-stock": "badge-success", "low-stock": "badge-warning", "out-of-stock": "badge-danger" };
    return <span className={`badge ${m[s]}`}><span className="badge-dot" />{s.replace("-", " ")}</span>;
};

export default function InventoryPage() {
    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState("all");

    const filtered = products.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(search.toLowerCase()) || p.sku.toLowerCase().includes(search.toLowerCase());
        const matchFilter = filter === "all" || p.status === filter;
        return matchSearch && matchFilter;
    });

    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Inventory</h1>
                    <p>Manage products, stock levels, and reorder alerts.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-inventory-btn"><Download size={15} />Export</button>
                    <button className="btn btn-primary" id="add-product-btn"><Plus size={15} />Add Product</button>
                </div>
            </div>

            {/* KPIs */}
            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)", marginBottom: "1.5rem" }}>
                <div className="kpi-card indigo">
                    <div className="kpi-top"><div className="kpi-icon indigo"><Package size={20} /></div></div>
                    <div className="kpi-value">335</div>
                    <div className="kpi-label">Total SKUs</div>
                </div>
                <div className="kpi-card teal">
                    <div className="kpi-top"><div className="kpi-icon teal"><Package size={20} /></div></div>
                    <div className="kpi-value">289</div>
                    <div className="kpi-label">In Stock</div>
                </div>
                <div className="kpi-card amber">
                    <div className="kpi-top"><div className="kpi-icon amber"><AlertTriangle size={20} /></div></div>
                    <div className="kpi-value">3</div>
                    <div className="kpi-label">Low Stock Alerts</div>
                </div>
                <div className="kpi-card rose">
                    <div className="kpi-top"><div className="kpi-icon rose"><AlertTriangle size={20} /></div></div>
                    <div className="kpi-value">2</div>
                    <div className="kpi-label">Out of Stock</div>
                </div>
            </div>

            <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
                <div className="chart-wrapper">
                    <div className="chart-header">
                        <div>
                            <div className="chart-title">Stock by Category</div>
                            <div className="chart-subtitle">Units in warehouse</div>
                        </div>
                    </div>
                    <ResponsiveContainer width="100%" height={180}>
                        <BarChart data={stockChart} margin={{ top: 5, left: -10 }}>
                            <XAxis dataKey="cat" tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                                {stockChart.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div className="card">
                    <div className="card-header"><span className="card-title">Reorder Alerts</span><span className="badge badge-warning">3 items</span></div>
                    {products.filter(p => p.status !== "in-stock").map(p => (
                        <div key={p.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0.65rem 0", borderBottom: "1px solid var(--border-primary)" }}>
                            <div>
                                <div style={{ fontSize: "0.85rem", fontWeight: 600, color: "var(--text-primary)" }}>{p.name}</div>
                                <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)" }}>Stock: {p.stock} / Reorder at: {p.reorder}</div>
                            </div>
                            {statusBadge(p.status)}
                        </div>
                    ))}
                </div>
            </div>

            {/* Toolbar */}
            <div className="toolbar">
                <div className="toolbar-left">
                    <div className="search-bar">
                        <Search size={15} style={{ color: "var(--text-muted)" }} />
                        <input placeholder="Search products or SKU..." value={search} onChange={e => setSearch(e.target.value)} id="inventory-search" />
                    </div>
                    <div className="filter-tabs">
                        {["all", "in-stock", "low-stock", "out-of-stock"].map(f => (
                            <button key={f} className={`filter-tab${filter === f ? " active" : ""}`} onClick={() => setFilter(f)} id={`filter-${f}`}>
                                {f === "all" ? "All" : f.replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase())}
                            </button>
                        ))}
                    </div>
                </div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{filtered.length} products</div>
            </div>

            <div className="table-wrapper">
                <table>
                    <thead><tr><th>Product</th><th>SKU</th><th>Category</th><th>Stock</th><th>Reorder At</th><th>Unit Price</th><th>Status</th></tr></thead>
                    <tbody>
                        {filtered.map(p => (
                            <tr key={p.id}>
                                <td className="td-primary">{p.name}</td>
                                <td className="td-mono">{p.sku}</td>
                                <td>{p.category}</td>
                                <td><span style={{ fontWeight: 700, color: p.stock === 0 ? "var(--accent-danger)" : p.stock <= p.reorder ? "var(--accent-warning)" : "var(--accent-success)" }}>{p.stock}</span></td>
                                <td style={{ color: "var(--text-muted)" }}>{p.reorder}</td>
                                <td className="td-primary">{p.price}</td>
                                <td>{statusBadge(p.status)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
