"use client";
import { Bell, Search, Settings, HelpCircle } from "lucide-react";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const pageTitles: Record<string, { title: string; breadcrumb: string }> = {
    "/": { title: "Dashboard", breadcrumb: "NexusERP / Overview" },
    "/inventory": { title: "Inventory", breadcrumb: "NexusERP / Operations / Inventory" },
    "/sales": { title: "Sales & Orders", breadcrumb: "NexusERP / Operations / Sales" },
    "/customers": { title: "Customers", breadcrumb: "NexusERP / Operations / Customers" },
    "/finance": { title: "Finance", breadcrumb: "NexusERP / Finance & People / Finance" },
    "/hr": { title: "HR & Employees", breadcrumb: "NexusERP / Finance & People / HR" },
    "/reports": { title: "Reports & Analytics", breadcrumb: "NexusERP / Intelligence / Reports" },
    "/settings": { title: "Settings", breadcrumb: "NexusERP / Intelligence / Settings" },
};

function LiveClock() {
    const [time, setTime] = useState<string>("");
    const [date, setDate] = useState<string>("");

    useEffect(() => {
        const fmt = () => {
            const now = new Date();
            setTime(now.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
            setDate(now.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }));
        };
        fmt();
        const id = setInterval(fmt, 1000);
        return () => clearInterval(id);
    }, []);

    if (!time) return null;

    return (
        <div style={{
            display: "flex", flexDirection: "column", alignItems: "flex-end",
            borderRight: "1px solid var(--border-primary)", paddingRight: "1rem", marginRight: "0.25rem",
        }}>
            <span style={{
                fontSize: "0.9rem", fontWeight: 700, color: "var(--text-primary)",
                fontVariantNumeric: "tabular-nums", letterSpacing: "0.03em", lineHeight: 1.2,
            }}>
                {time}
            </span>
            <span style={{ fontSize: "0.68rem", color: "var(--text-muted)", marginTop: 1 }}>{date}</span>
        </div>
    );
}

export default function Topbar() {
    const pathname = usePathname();
    const page = pageTitles[pathname] ?? { title: "NexusERP", breadcrumb: "NexusERP" };

    return (
        <header className="topbar">
            <div className="topbar-left">
                <span className="topbar-title">{page.title}</span>
                <span className="topbar-breadcrumb">{page.breadcrumb}</span>
            </div>

            <div className="topbar-right">
                <LiveClock />

                <div className="topbar-search">
                    <Search size={14} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
                    <input placeholder="Search anything..." id="global-search" />
                    <span style={{
                        fontSize: "0.65rem", color: "var(--text-muted)",
                        background: "var(--bg-secondary)", border: "1px solid var(--border-primary)",
                        borderRadius: 5, padding: "1px 5px", flexShrink: 0,
                    }}>⌘K</span>
                </div>

                <button className="topbar-icon-btn" id="help-btn" aria-label="Help">
                    <HelpCircle size={16} />
                </button>
                <button className="topbar-icon-btn" id="notifications-btn" aria-label="Notifications">
                    <Bell size={16} />
                    <span className="notification-dot" />
                </button>
                <button className="topbar-icon-btn" id="settings-btn" aria-label="Settings">
                    <Settings size={16} />
                </button>

                <div className="topbar-user" id="topbar-user-menu">
                    <div className="topbar-avatar">AD</div>
                    <span className="topbar-username">Admin</span>
                </div>
            </div>
        </header>
    );
}
