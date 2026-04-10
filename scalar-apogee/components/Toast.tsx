"use client";
import { createContext, useContext, useState, useCallback, ReactNode } from "react";
import { CheckCircle, XCircle, AlertCircle, Info, X } from "lucide-react";

type ToastType = "success" | "error" | "warning" | "info";
interface Toast { id: number; type: ToastType; title: string; message?: string; }

const ToastContext = createContext<{ toast: (type: ToastType, title: string, message?: string) => void }>({ toast: () => { } });

export function useToast() { return useContext(ToastContext); }

const icons = { success: CheckCircle, error: XCircle, warning: AlertCircle, info: Info };
const colors = {
    success: { bg: "rgba(16,185,129,0.12)", border: "rgba(16,185,129,0.3)", icon: "#10B981" },
    error: { bg: "rgba(239,68,68,0.12)", border: "rgba(239,68,68,0.3)", icon: "#EF4444" },
    warning: { bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.3)", icon: "#F59E0B" },
    info: { bg: "rgba(99,102,241,0.12)", border: "rgba(99,102,241,0.3)", icon: "#6366F1" },
};

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<Toast[]>([]);
    let nextId = 0;

    const toast = useCallback((type: ToastType, title: string, message?: string) => {
        const id = ++nextId;
        setToasts(p => [...p, { id, type, title, message }]);
        setTimeout(() => setToasts(p => p.filter(t => t.id !== id)), 4000);
    }, []);

    const remove = (id: number) => setToasts(p => p.filter(t => t.id !== id));

    return (
        <ToastContext.Provider value={{ toast }}>
            {children}
            <div style={{
                position: "fixed", bottom: "1.5rem", right: "1.5rem",
                display: "flex", flexDirection: "column", gap: "0.75rem",
                zIndex: 9999, pointerEvents: "none",
            }}>
                {toasts.map(t => {
                    const Icon = icons[t.type];
                    const c = colors[t.type];
                    return (
                        <div key={t.id} style={{
                            display: "flex", alignItems: "flex-start", gap: "0.75rem",
                            background: c.bg, border: `1px solid ${c.border}`,
                            backdropFilter: "blur(16px)", borderRadius: 14,
                            padding: "0.875rem 1rem", minWidth: 280, maxWidth: 360,
                            pointerEvents: "all", animation: "fadeInUp 0.3s ease",
                            boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
                        }}>
                            <Icon size={18} style={{ color: c.icon, flexShrink: 0, marginTop: 1 }} />
                            <div style={{ flex: 1 }}>
                                <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--text-primary)" }}>{t.title}</div>
                                {t.message && <div style={{ fontSize: "0.78rem", color: "var(--text-secondary)", marginTop: 2 }}>{t.message}</div>}
                            </div>
                            <button onClick={() => remove(t.id)} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)", padding: 0, display: "flex" }}>
                                <X size={14} />
                            </button>
                        </div>
                    );
                })}
            </div>
        </ToastContext.Provider>
    );
}
