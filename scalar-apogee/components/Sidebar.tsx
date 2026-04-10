"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard, Package, ShoppingCart, Users, DollarSign,
    Users2, BarChart3, Settings, ChevronDown, Store, Bell, LogOut
} from "lucide-react";
import { useState } from "react";

const navGroups = [
    {
        label: "Overview",
        items: [
            { href: "/", icon: LayoutDashboard, label: "Dashboard" },
        ],
    },
    {
        label: "Operations",
        items: [
            { href: "/inventory", icon: Package, label: "Inventory", badge: "3" },
            { href: "/sales", icon: ShoppingCart, label: "Sales & Orders" },
            { href: "/customers", icon: Users, label: "Customers" },
        ],
    },
    {
        label: "Finance & People",
        items: [
            { href: "/finance", icon: DollarSign, label: "Finance" },
            { href: "/hr", icon: Users2, label: "HR & Employees" },
        ],
    },
    {
        label: "Intelligence",
        items: [
            { href: "/reports", icon: BarChart3, label: "Reports" },
            { href: "/settings", icon: Settings, label: "Settings" },
        ],
    },
];

export default function Sidebar() {
    const pathname = usePathname();
    const [collapsed, setCollapsed] = useState(false);

    return (
        <aside className="sidebar" style={{ width: collapsed ? 72 : undefined, transition: "width 0.3s ease" }}>
            {/* Brand */}
            <div className="sidebar-brand" style={{ justifyContent: collapsed ? "center" : undefined }}>
                <div style={{
                    width: 36, height: 36, borderRadius: 10, flexShrink: 0,
                    background: "linear-gradient(135deg, #6366F1, #8B5CF6)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    boxShadow: "0 4px 12px rgba(99,102,241,0.4)",
                }}>
                    <Store size={18} color="#fff" />
                </div>
                {!collapsed && (
                    <div>
                        <div style={{ fontWeight: 800, fontSize: "1rem", letterSpacing: "-0.03em", color: "var(--text-primary)" }}>
                            Revilo<span style={{ color: "var(--accent-primary)" }}>.</span>
                        </div>
                        <div style={{ fontSize: "0.65rem", color: "var(--text-muted)", letterSpacing: "0.06em", textTransform: "uppercase" }}>Store ERP</div>
                    </div>
                )}
                <button
                    onClick={() => setCollapsed(c => !c)}
                    style={{
                        marginLeft: collapsed ? undefined : "auto",
                        background: "none", border: "none", cursor: "pointer",
                        color: "var(--text-muted)", display: "flex", padding: 4,
                        borderRadius: 6, transition: "color 0.2s",
                    }}
                    title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
                >
                    <ChevronDown size={14} style={{ transform: collapsed ? "rotate(-90deg)" : "rotate(90deg)", transition: "transform 0.3s" }} />
                </button>
            </div>

            {/* Nav */}
            <nav className="sidebar-nav">
                {navGroups.map(group => (
                    <div key={group.label} className="sidebar-nav-group">
                        {!collapsed && <div className="sidebar-nav-label">{group.label}</div>}
                        {group.items.map(item => {
                            const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`sidebar-nav-item${active ? " active" : ""}`}
                                    title={collapsed ? item.label : undefined}
                                    style={{ justifyContent: collapsed ? "center" : undefined }}
                                >
                                    <span className="nav-icon"><item.icon size={18} /></span>
                                    {!collapsed && <span className="nav-label">{item.label}</span>}
                                    {!collapsed && item.badge && (
                                        <span style={{
                                            marginLeft: "auto", background: "#EF4444",
                                            color: "#fff", fontSize: "0.65rem", fontWeight: 700,
                                            padding: "1px 6px", borderRadius: 20, minWidth: 18, textAlign: "center",
                                        }}>{item.badge}</span>
                                    )}
                                </Link>
                            );
                        })}
                    </div>
                ))}
            </nav>

            {/* Footer */}
            {!collapsed && (
                <div className="sidebar-footer">
                    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flex: 1, minWidth: 0 }}>
                        <div style={{
                            width: 34, height: 34, borderRadius: 10, flexShrink: 0,
                            background: "linear-gradient(135deg, #6366F1, #8B5CF6)",
                            display: "flex", alignItems: "center", justifyContent: "center",
                            fontWeight: 700, fontSize: "0.85rem", color: "#fff",
                        }}>RS</div>
                        <div style={{ minWidth: 0 }}>
                            <div style={{ fontSize: "0.82rem", fontWeight: 600, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>Admin</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-muted)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>admin@revilostore.com</div>
                        </div>
                    </div>
                    <div style={{ display: "flex", gap: "0.25rem" }}>
                        <button style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)", padding: 6, borderRadius: 6, display: "flex" }} title="Notifications">
                            <Bell size={15} />
                        </button>
                        <button style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)", padding: 6, borderRadius: 6, display: "flex" }} title="Sign Out">
                            <LogOut size={15} />
                        </button>
                    </div>
                </div>
            )}
        </aside>
    );
}
