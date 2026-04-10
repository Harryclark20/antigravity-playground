"use client";
import Link from "next/link";
import { Home, ArrowLeft } from "lucide-react";

export default function NotFound() {
    return (
        <div style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            textAlign: "center",
            padding: "2rem",
            background: "var(--bg-primary)",
            gap: "1.5rem",
        }}>
            {/* Glowing 404 */}
            <div style={{ position: "relative" }}>
                <div style={{
                    fontSize: "clamp(6rem, 20vw, 12rem)",
                    fontWeight: 900,
                    letterSpacing: "-0.06em",
                    lineHeight: 1,
                    background: "linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #06B6D4 100%)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    backgroundClip: "text",
                    filter: "drop-shadow(0 0 60px rgba(99, 102, 241, 0.4))",
                }}>
                    404
                </div>
                {/* Blurred glow behind */}
                <div style={{
                    position: "absolute",
                    top: "50%", left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: 300, height: 300,
                    borderRadius: "50%",
                    background: "rgba(99, 102, 241, 0.12)",
                    filter: "blur(60px)",
                    zIndex: -1,
                    pointerEvents: "none",
                }} />
            </div>

            <div>
                <h1 style={{
                    fontSize: "1.75rem", fontWeight: 800,
                    color: "var(--text-primary)", letterSpacing: "-0.04em",
                    marginBottom: "0.5rem",
                }}>
                    Page Not Found
                </h1>
                <p style={{ fontSize: "0.95rem", color: "var(--text-secondary)", maxWidth: 420, margin: "0 auto" }}>
                    The page you&apos;re looking for doesn&apos;t exist or has been moved.
                    Let&apos;s get you back to the dashboard.
                </p>
            </div>

            <div style={{ display: "flex", gap: "1rem" }}>
                <Link href="/" className="btn btn-primary" id="back-to-dashboard-btn">
                    <Home size={16} /> Go to Dashboard
                </Link>
                <button onClick={() => history.back()} className="btn btn-secondary" id="go-back-btn">
                    <ArrowLeft size={16} /> Go Back
                </button>
            </div>

            {/* Floating decorative dots */}
            <div style={{
                position: "fixed", inset: 0, pointerEvents: "none", overflow: "hidden", zIndex: 0,
            }}>
                {[...Array(6)].map((_, i) => (
                    <div key={i} style={{
                        position: "absolute",
                        width: `${[8, 12, 6, 10, 14, 8][i]}px`,
                        height: `${[8, 12, 6, 10, 14, 8][i]}px`,
                        borderRadius: "50%",
                        background: ["#6366F1", "#06B6D4", "#8B5CF6", "#10B981", "#6366F1", "#06B6D4"][i],
                        opacity: 0.3,
                        top: `${[15, 70, 40, 85, 25, 60][i]}%`,
                        left: `${[10, 85, 60, 20, 45, 75][i]}%`,
                        filter: "blur(2px)",
                        animation: `pulse ${[3, 4, 2.5, 3.5, 2, 4.5][i]}s ease-in-out infinite`,
                    }} />
                ))}
            </div>
        </div>
    );
}
