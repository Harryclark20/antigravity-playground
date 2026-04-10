"use client";
import { useState } from "react";
import { Building, Bell, Shield, Users, CreditCard, Globe, Save, Upload } from "lucide-react";

const settingsSections = [
    { id: "company", label: "Company", icon: Building },
    { id: "notifications", label: "Notifications", icon: Bell },
    { id: "security", label: "Security", icon: Shield },
    { id: "users", label: "Users & Roles", icon: Users },
    { id: "billing", label: "Billing", icon: CreditCard },
    { id: "integrations", label: "Integrations", icon: Globe },
];

const users = [
    { name: "Admin User", email: "admin@nexuserp.io", role: "Super Admin", status: "active" },
    { name: "Sarah Johnson", email: "s.johnson@nexuserp.io", role: "Manager", status: "active" },
    { name: "Marcus Chen", email: "m.chen@nexuserp.io", role: "Editor", status: "active" },
    { name: "Emma Thompson", email: "e.thompson@nexuserp.io", role: "Viewer", status: "inactive" },
];

const roleBadge = (r: string) => {
    const m: Record<string, string> = { "Super Admin": "badge-primary", Manager: "badge-success", Editor: "badge-info", Viewer: "badge-muted" };
    return <span className={`badge ${m[r]}`}>{r}</span>;
};

export default function SettingsPage() {
    const [active, setActive] = useState("company");
    const [toggles, setToggles] = useState({ emailAlerts: true, orderNotif: true, stockAlerts: true, twoFA: false, sessionLog: true, apiAccess: false });

    const toggle = (key: keyof typeof toggles) => setToggles(p => ({ ...p, [key]: !p[key] }));

    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Settings</h1>
                    <p>Manage your workspace, integrations, and preferences.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-primary" id="save-settings-btn"><Save size={15} />Save Changes</button>
                </div>
            </div>

            <div className="settings-grid">
                {/* Settings Nav */}
                <div className="settings-nav">
                    {settingsSections.map(({ id, label, icon: Icon }) => (
                        <div key={id} className={`settings-nav-item${active === id ? " active" : ""}`} onClick={() => setActive(id)} id={`settings-nav-${id}`}>
                            <Icon size={16} /> {label}
                        </div>
                    ))}
                </div>

                {/* Settings Panels */}
                <div className="settings-panel">
                    {active === "company" && (
                        <div className="card">
                            <div className="card-header"><span className="card-title">Company Information</span></div>
                            <div style={{ display: "flex", alignItems: "center", gap: "1.25rem", marginBottom: "1.5rem", padding: "1rem", background: "var(--bg-secondary)", borderRadius: 12, border: "1px solid var(--border-primary)" }}>
                                <div style={{ width: 72, height: 72, borderRadius: 16, background: "var(--gradient-primary)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.5rem", fontWeight: 800, color: "white", flexShrink: 0 }}>N</div>
                                <div>
                                    <div style={{ fontWeight: 700, color: "var(--text-primary)", marginBottom: 4 }}>NexusERP Inc.</div>
                                    <div style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>Update your logo and company branding.</div>
                                    <button className="btn btn-secondary btn-sm" style={{ marginTop: 8 }}><Upload size={13} />Upload Logo</button>
                                </div>
                            </div>
                            <div className="form-grid">
                                <div className="form-group"><label className="form-label">Company Name</label><input className="form-input" defaultValue="NexusERP Inc." id="company-name" /></div>
                                <div className="form-group"><label className="form-label">Industry</label><select className="form-input" id="company-industry"><option>Technology</option><option>Retail</option><option>Manufacturing</option><option>Healthcare</option></select></div>
                                <div className="form-group"><label className="form-label">Email Address</label><input className="form-input" defaultValue="admin@nexuserp.io" id="company-email" /></div>
                                <div className="form-group"><label className="form-label">Phone Number</label><input className="form-input" defaultValue="+1 (555) 000-0000" id="company-phone" /></div>
                                <div className="form-group"><label className="form-label">Country</label><select className="form-input" id="company-country"><option>United States</option><option>United Kingdom</option><option>Canada</option></select></div>
                                <div className="form-group"><label className="form-label">Timezone</label><select className="form-input" id="company-timezone"><option>UTC-5 Eastern</option><option>UTC-6 Central</option><option>UTC-8 Pacific</option><option>UTC+0 GMT</option><option>UTC+1 CET</option></select></div>
                            </div>
                            <div className="form-group" style={{ marginTop: "1rem" }}><label className="form-label">Company Description</label><textarea className="form-input" rows={3} defaultValue="Enterprise resource planning platform for modern businesses." id="company-description" style={{ resize: "vertical" }} /></div>
                        </div>
                    )}

                    {active === "notifications" && (
                        <div className="card">
                            <div className="card-header"><span className="card-title">Notification Preferences</span></div>
                            <div>
                                {[
                                    { key: "emailAlerts", label: "Email Alerts", desc: "Receive important updates via email" },
                                    { key: "orderNotif", label: "Order Notifications", desc: "Get notified when new orders arrive" },
                                    { key: "stockAlerts", label: "Low Stock Alerts", desc: "Alert when inventory hits reorder threshold" },
                                ].map(({ key, label, desc }) => (
                                    <div className="toggle-row" key={key}>
                                        <div className="toggle-info"><h4>{label}</h4><p>{desc}</p></div>
                                        <div className={`toggle${toggles[key as keyof typeof toggles] ? " on" : ""}`} onClick={() => toggle(key as keyof typeof toggles)} id={`toggle-${key}`} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {active === "security" && (
                        <div className="card">
                            <div className="card-header"><span className="card-title">Security Settings</span></div>
                            <div className="form-group" style={{ marginBottom: "1rem" }}>
                                <label className="form-label">Current Password</label>
                                <input type="password" className="form-input" placeholder="••••••••" id="current-password" />
                            </div>
                            <div className="form-grid" style={{ marginBottom: "1rem" }}>
                                <div className="form-group"><label className="form-label">New Password</label><input type="password" className="form-input" placeholder="••••••••" id="new-password" /></div>
                                <div className="form-group"><label className="form-label">Confirm Password</label><input type="password" className="form-input" placeholder="••••••••" id="confirm-password" /></div>
                            </div>
                            <div>
                                {[
                                    { key: "twoFA", label: "Two-Factor Authentication", desc: "Add an extra layer of security to your account" },
                                    { key: "sessionLog", label: "Session Logging", desc: "Log all user session activity for audit trails" },
                                    { key: "apiAccess", label: "API Access Tokens", desc: "Allow external API integrations" },
                                ].map(({ key, label, desc }) => (
                                    <div className="toggle-row" key={key}>
                                        <div className="toggle-info"><h4>{label}</h4><p>{desc}</p></div>
                                        <div className={`toggle${toggles[key as keyof typeof toggles] ? " on" : ""}`} onClick={() => toggle(key as keyof typeof toggles)} id={`toggle-${key}`} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {active === "users" && (
                        <div className="card" style={{ padding: 0, overflow: "hidden" }}>
                            <div style={{ padding: "1.25rem 1.5rem", borderBottom: "1px solid var(--border-primary)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <span className="card-title">Users & Roles</span>
                                <button className="btn btn-primary btn-sm" id="invite-user-btn"><Users size={13} />Invite User</button>
                            </div>
                            <table style={{ width: "100%" }}>
                                <thead><tr><th>User</th><th>Role</th><th>Status</th><th>Action</th></tr></thead>
                                <tbody>
                                    {users.map(u => (
                                        <tr key={u.email}>
                                            <td>
                                                <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                                                    <div style={{ width: 34, height: 34, borderRadius: "50%", background: "var(--gradient-primary)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.75rem", fontWeight: 700, color: "white" }}>
                                                        {u.name.split(" ").map(n => n[0]).join("")}
                                                    </div>
                                                    <div>
                                                        <div className="td-primary" style={{ fontWeight: 600 }}>{u.name}</div>
                                                        <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>{u.email}</div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>{roleBadge(u.role)}</td>
                                            <td><span className={`badge ${u.status === "active" ? "badge-success" : "badge-muted"}`}><span className="badge-dot" />{u.status}</span></td>
                                            <td><button className="btn btn-ghost btn-sm">Edit</button></td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    {(active === "billing" || active === "integrations") && (
                        <div className="card" style={{ textAlign: "center", padding: "3rem" }}>
                            <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>{active === "billing" ? "💳" : "🔌"}</div>
                            <div style={{ fontWeight: 700, color: "var(--text-primary)", fontSize: "1.1rem", marginBottom: "0.5rem" }}>
                                {active === "billing" ? "Billing & Subscription" : "Integrations"}
                            </div>
                            <div style={{ color: "var(--text-secondary)", fontSize: "0.85rem", marginBottom: "1.5rem" }}>
                                {active === "billing" ? "Manage your plan, payment methods, and invoices." : "Connect third-party tools like Slack, Stripe, and Zapier."}
                            </div>
                            <button className="btn btn-primary" id={`${active}-cta-btn`}>
                                {active === "billing" ? "Manage Subscription" : "Browse Integrations"}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
