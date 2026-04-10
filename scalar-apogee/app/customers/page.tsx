"use client";
import { useState } from "react";
import { Users, UserPlus, Mail, Phone, Star, Search, Download } from "lucide-react";

const customers = [
    { id: "CUS-001", name: "Olivia Carter", email: "o.carter@email.com", phone: "+1 (555) 210-3344", location: "New York, USA", orders: 14, spent: "$18,492", tier: "vip", since: "Jan 2023" },
    { id: "CUS-002", name: "James Thornton", email: "j.thornton@email.com", phone: "+1 (555) 847-9920", location: "Chicago, USA", orders: 6, spent: "$3,140", tier: "regular", since: "Mar 2024" },
    { id: "CUS-003", name: "Ava Mitchell", email: "a.mitchell@email.com", phone: "+44 20 7946 0958", location: "London, UK", orders: 9, spent: "$8,701", tier: "premium", since: "Aug 2023" },
    { id: "CUS-004", name: "Liam Patterson", email: "l.patterson@email.com", phone: "+1 (555) 332-0011", location: "Austin, USA", orders: 22, spent: "$31,256", tier: "vip", since: "Sep 2022" },
    { id: "CUS-005", name: "Sophia Jenkins", email: "s.jenkins@email.com", phone: "+49 30 12345678", location: "Berlin, DE", orders: 3, spent: "$1,247", tier: "regular", since: "Nov 2024" },
    { id: "CUS-006", name: "Noah Williams", email: "n.williams@email.com", phone: "+1 (555) 900-4421", location: "Miami, USA", orders: 18, spent: "$22,130", tier: "premium", since: "Feb 2023" },
    { id: "CUS-007", name: "Isabella Brown", email: "i.brown@email.com", phone: "+61 2 9374 4000", location: "Sydney, AU", orders: 7, spent: "$5,980", tier: "regular", since: "Jun 2024" },
    { id: "CUS-008", name: "Mason Davis", email: "m.davis@email.com", phone: "+1 (555) 774-2200", location: "Seattle, USA", orders: 11, spent: "$12,340", tier: "premium", since: "Apr 2023" },
];

const tierBadge = (t: string) => {
    const m: Record<string, string> = { vip: "badge-primary", premium: "badge-success", regular: "badge-muted" };
    const icons: Record<string, string> = { vip: "👑", premium: "⭐", regular: "" };
    return <span className={`badge ${m[t]}`}>{icons[t]} {t.toUpperCase()}</span>;
};

export default function CustomersPage() {
    const [search, setSearch] = useState("");
    const [tier, setTier] = useState("all");
    const filtered = customers.filter(c => {
        const ms = c.name.toLowerCase().includes(search.toLowerCase()) || c.email.toLowerCase().includes(search.toLowerCase());
        const mt = tier === "all" || c.tier === tier;
        return ms && mt;
    });

    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Customers</h1>
                    <p>Manage customer relationships and track lifetime value.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-customers-btn"><Download size={15} />Export</button>
                    <button className="btn btn-primary" id="add-customer-btn"><UserPlus size={15} />Add Customer</button>
                </div>
            </div>

            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                <div className="kpi-card indigo"><div className="kpi-top"><div className="kpi-icon indigo"><Users size={20} /></div></div><div className="kpi-value">8,472</div><div className="kpi-label">Total Customers</div></div>
                <div className="kpi-card teal"><div className="kpi-top"><div className="kpi-icon teal"><Star size={20} /></div></div><div className="kpi-value">241</div><div className="kpi-label">VIP Clients</div></div>
                <div className="kpi-card amber"><div className="kpi-top"><div className="kpi-icon amber"><UserPlus size={20} /></div></div><div className="kpi-value">132</div><div className="kpi-label">New This Month</div></div>
                <div className="kpi-card rose"><div className="kpi-top"><div className="kpi-icon rose"><Users size={20} /></div></div><div className="kpi-value">$2,840</div><div className="kpi-label">Avg. LTV</div></div>
            </div>

            <div className="toolbar">
                <div className="toolbar-left">
                    <div className="search-bar">
                        <Search size={15} style={{ color: "var(--text-muted)" }} />
                        <input placeholder="Search by name or email..." value={search} onChange={e => setSearch(e.target.value)} id="customers-search" />
                    </div>
                    <div className="filter-tabs">
                        {["all", "vip", "premium", "regular"].map(t => (
                            <button key={t} className={`filter-tab${tier === t ? " active" : ""}`} onClick={() => setTier(t)} id={`tier-filter-${t}`}>
                                {t.charAt(0).toUpperCase() + t.slice(1)}
                            </button>
                        ))}
                    </div>
                </div>
                <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>{filtered.length} customers</div>
            </div>

            <div className="table-wrapper">
                <table>
                    <thead><tr><th>Customer</th><th>Contact</th><th>Location</th><th>Orders</th><th>Total Spent</th><th>Member Since</th><th>Tier</th></tr></thead>
                    <tbody>
                        {filtered.map(c => (
                            <tr key={c.id}>
                                <td>
                                    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                                        <div style={{ width: 34, height: 34, borderRadius: "50%", background: "var(--gradient-primary)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.75rem", fontWeight: 700, color: "white", flexShrink: 0 }}>
                                            {c.name.split(" ").map(n => n[0]).join("")}
                                        </div>
                                        <div>
                                            <div className="td-primary" style={{ fontWeight: 600, fontSize: "0.875rem" }}>{c.name}</div>
                                            <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>{c.id}</div>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>
                                        <div style={{ display: "flex", alignItems: "center", gap: 4 }}><Mail size={11} /> {c.email}</div>
                                        <div style={{ display: "flex", alignItems: "center", gap: 4, marginTop: 2 }}><Phone size={11} /> {c.phone}</div>
                                    </div>
                                </td>
                                <td>{c.location}</td>
                                <td style={{ fontWeight: 700, color: "var(--text-primary)" }}>{c.orders}</td>
                                <td style={{ fontWeight: 700, color: "var(--accent-success)" }}>{c.spent}</td>
                                <td>{c.since}</td>
                                <td>{tierBadge(c.tier)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
