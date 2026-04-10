"use client";
import { UserCheck, DollarSign, Briefcase, Plus, Search, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, Cell } from "recharts";

const employees = [
    { id: "EMP-001", name: "Sarah Johnson", role: "VP Engineering", dept: "Engineering", salary: "$12,500/mo", status: "active", joined: "Jan 2021", projects: 8, color: "#6366F1" },
    { id: "EMP-002", name: "Marcus Chen", role: "Lead Designer", dept: "Design", salary: "$9,200/mo", status: "active", joined: "Mar 2022", projects: 12, color: "#06B6D4" },
    { id: "EMP-003", name: "Priya Patel", role: "Product Manager", dept: "Product", salary: "$10,800/mo", status: "active", joined: "Jun 2021", projects: 6, color: "#10B981" },
    { id: "EMP-004", name: "Alex Rivera", role: "Sales Manager", dept: "Sales", salary: "$8,500/mo", status: "active", joined: "Sep 2022", projects: 4, color: "#F59E0B" },
    { id: "EMP-005", name: "Emma Thompson", role: "Financial Analyst", dept: "Finance", salary: "$7,800/mo", status: "active", joined: "Nov 2022", projects: 3, color: "#8B5CF6" },
    { id: "EMP-006", name: "David Kim", role: "DevOps Engineer", dept: "Engineering", salary: "$11,200/mo", status: "remote", joined: "Feb 2023", projects: 7, color: "#6366F1" },
    { id: "EMP-007", name: "Luna Martinez", role: "Marketing Lead", dept: "Marketing", salary: "$8,100/mo", status: "active", joined: "Apr 2023", projects: 9, color: "#EF4444" },
    { id: "EMP-008", name: "Oliver Scott", role: "HR Manager", dept: "HR", salary: "$7,200/mo", status: "on-leave", joined: "Jul 2023", projects: 2, color: "#F59E0B" },
];

const deptData = [
    { dept: "Engineering", count: 18, color: "#6366F1" },
    { dept: "Sales", count: 12, color: "#06B6D4" },
    { dept: "Design", count: 7, color: "#10B981" },
    { dept: "Marketing", count: 8, color: "#F59E0B" },
    { dept: "Finance", count: 5, color: "#8B5CF6" },
    { dept: "HR", count: 4, color: "#EF4444" },
];

const statusBadge = (s: string) => {
    const m: Record<string, string> = { active: "badge-success", remote: "badge-info", "on-leave": "badge-warning" };
    return <span className={`badge ${m[s]}`}><span className="badge-dot" />{s.replace("-", " ")}</span>;
};

const deptColors: Record<string, string> = { Engineering: "#6366F1", Design: "#06B6D4", Product: "#10B981", Sales: "#F59E0B", Finance: "#8B5CF6", Marketing: "#EF4444", HR: "#F97316" };

export default function HRPage() {
    return (
        <div className="page-container">
            <div className="page-header">
                <div className="page-header-left">
                    <h1>HR & Employees</h1>
                    <p>Employee directory, departments, and payroll overview.</p>
                </div>
                <div className="page-header-actions">
                    <button className="btn btn-secondary" id="export-hr-btn"><Download size={15} />Export</button>
                    <button className="btn btn-primary" id="add-employee-btn"><Plus size={15} />Add Employee</button>
                </div>
            </div>

            <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                <div className="kpi-card indigo"><div className="kpi-top"><div className="kpi-icon indigo"><UserCheck size={20} /></div></div><div className="kpi-value">54</div><div className="kpi-label">Total Employees</div></div>
                <div className="kpi-card teal"><div className="kpi-top"><div className="kpi-icon teal"><Briefcase size={20} /></div></div><div className="kpi-value">7</div><div className="kpi-label">Departments</div></div>
                <div className="kpi-card amber"><div className="kpi-top"><div className="kpi-icon amber"><UserCheck size={20} /></div></div><div className="kpi-value">3</div><div className="kpi-label">New Hires (Mar)</div></div>
                <div className="kpi-card rose"><div className="kpi-top"><div className="kpi-icon rose"><DollarSign size={20} /></div></div><div className="kpi-value">$422K</div><div className="kpi-label">Monthly Payroll</div></div>
            </div>

            <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
                <div className="chart-wrapper">
                    <div className="chart-header"><div><div className="chart-title">Headcount by Department</div><div className="chart-subtitle">Current distribution</div></div></div>
                    <ResponsiveContainer width="100%" height={190}>
                        <BarChart data={deptData} layout="vertical" margin={{ left: 10 }}>
                            <XAxis type="number" tick={{ fill: "#475569", fontSize: 11 }} axisLine={false} tickLine={false} />
                            <YAxis type="category" dataKey="dept" tick={{ fill: "#94A3B8", fontSize: 12 }} axisLine={false} tickLine={false} width={90} />
                            <Tooltip contentStyle={{ background: "var(--bg-secondary)", border: "1px solid var(--border-primary)", borderRadius: 10, fontSize: 12 }} />
                            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                                {deptData.map((d, i) => <Cell key={i} fill={d.color} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div className="card">
                    <div className="card-header"><span className="card-title">Payroll Summary</span><span className="badge badge-success">March 2026</span></div>
                    {[
                        { label: "Engineering", value: "$182,400", pct: 43 },
                        { label: "Sales", value: "$102,000", pct: 24 },
                        { label: "Marketing", value: "$64,800", pct: 15 },
                        { label: "Design", value: "$64,400", pct: 15 },
                        { label: "Finance & HR", value: "$12,600", pct: 3 },
                    ].map(e => (
                        <div className="stat-bar-item" key={e.label}>
                            <div className="stat-bar-header">
                                <span className="stat-bar-label">{e.label}</span>
                                <span className="stat-bar-value">{e.value}</span>
                            </div>
                            <div className="stat-bar-track">
                                <div className="stat-bar-fill" style={{ width: `${e.pct}%`, background: deptColors[e.label.split(" ")[0]] || "#6366F1" }} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Employee Cards Grid */}
            <h2 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: "1rem" }}>Employee Directory</h2>
            <div className="grid-auto">
                {employees.map(e => (
                    <div className="employee-card" key={e.id} id={`employee-${e.id}`}>
                        <div className="employee-avatar" style={{ background: `${e.color}33`, color: e.color, border: `1.5px solid ${e.color}44` }}>
                            {e.name.split(" ").map(n => n[0]).join("")}
                        </div>
                        <div className="employee-name">{e.name}</div>
                        <div className="employee-role">{e.role}</div>
                        <div className="employee-dept" style={{ background: `${deptColors[e.dept]}22`, color: deptColors[e.dept] }}>{e.dept}</div>
                        <div style={{ marginBottom: "0.75rem" }}>{statusBadge(e.status)}</div>
                        <div className="employee-stats">
                            <div><div className="employee-stat-label">Salary</div><div className="employee-stat-value" style={{ fontSize: "0.78rem" }}>{e.salary}</div></div>
                            <div><div className="employee-stat-label">Projects</div><div className="employee-stat-value">{e.projects}</div></div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
