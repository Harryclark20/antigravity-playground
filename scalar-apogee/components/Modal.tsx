"use client";
import { ReactNode, useEffect } from "react";
import { X } from "lucide-react";

interface ModalProps {
    open: boolean;
    onClose: () => void;
    title: string;
    children: ReactNode;
    size?: "sm" | "md" | "lg";
    footer?: ReactNode;
}

export default function Modal({ open, onClose, title, children, size = "md", footer }: ModalProps) {
    useEffect(() => {
        if (open) document.body.style.overflow = "hidden";
        else document.body.style.overflow = "";
        return () => { document.body.style.overflow = ""; };
    }, [open]);

    if (!open) return null;

    const widths = { sm: 420, md: 560, lg: 720 };

    return (
        <div
            onClick={onClose}
            style={{
                position: "fixed", inset: 0, zIndex: 1000,
                background: "rgba(0,0,0,0.6)", backdropFilter: "blur(4px)",
                display: "flex", alignItems: "center", justifyContent: "center",
                padding: "1rem", animation: "fadeIn 0.15s ease",
            }}
        >
            <div
                onClick={e => e.stopPropagation()}
                style={{
                    background: "var(--bg-secondary)", border: "1px solid var(--border-primary)",
                    borderRadius: 20, width: "100%", maxWidth: widths[size],
                    maxHeight: "90vh", display: "flex", flexDirection: "column",
                    boxShadow: "0 24px 80px rgba(0,0,0,0.6)", animation: "fadeInUp 0.2s ease",
                }}
            >
                {/* Header */}
                <div style={{
                    display: "flex", alignItems: "center", justifyContent: "space-between",
                    padding: "1.25rem 1.5rem", borderBottom: "1px solid var(--border-primary)", flexShrink: 0,
                }}>
                    <h2 style={{ fontSize: "1rem", fontWeight: 700, color: "var(--text-primary)", margin: 0 }}>{title}</h2>
                    <button onClick={onClose} style={{
                        background: "var(--bg-primary)", border: "1px solid var(--border-primary)",
                        borderRadius: 8, padding: "0.35rem", cursor: "pointer",
                        color: "var(--text-muted)", display: "flex", alignItems: "center", justifyContent: "center",
                        transition: "all 0.2s",
                    }}
                        onMouseEnter={e => (e.currentTarget.style.borderColor = "var(--border-accent)")}
                        onMouseLeave={e => (e.currentTarget.style.borderColor = "var(--border-primary)")}
                    >
                        <X size={16} />
                    </button>
                </div>

                {/* Body */}
                <div style={{ padding: "1.5rem", overflowY: "auto", flex: 1 }}>{children}</div>

                {/* Footer */}
                {footer && (
                    <div style={{
                        padding: "1rem 1.5rem", borderTop: "1px solid var(--border-primary)",
                        display: "flex", gap: "0.75rem", justifyContent: "flex-end", flexShrink: 0,
                    }}>
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
}
