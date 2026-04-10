"use client";

import Image from "next/image";
import Link from "next/link";
import { useCart } from "@/context/CartContext";

export default function CartSidebar() {
    const { cart, removeFromCart, updateQuantity, isCartOpen, setIsCartOpen, cartTotal } = useCart();

    if (!isCartOpen) return null;

    return (
        <>
            {/* Backdrop overlay */}
            <div
                style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1000, backdropFilter: 'blur(4px)' }}
                onClick={() => setIsCartOpen(false)}
            />

            {/* Sidebar UI */}
            <div
                style={{ position: 'fixed', top: 0, right: 0, width: '100%', maxWidth: '400px', height: '100vh', backgroundColor: 'var(--bg-surface)', zIndex: 1001, borderLeft: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', boxShadow: '-10px 0 30px rgba(0,0,0,0.5)', animation: 'slideIn 0.3s ease-out forwards' }}
            >
                <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h2 style={{ fontSize: '1.5rem' }}>Your Cart</h2>
                    <button style={{ color: 'var(--text-secondary)' }} onClick={() => setIsCartOpen(false)}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>

                <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {cart.length === 0 ? (
                        <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>Your cart is empty.</p>
                    ) : (
                        cart.map(item => (
                            <div key={item.id} style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                <div style={{ position: 'relative', width: '80px', height: '80px', borderRadius: '8px', overflow: 'hidden', flexShrink: 0 }}>
                                    <Image src={item.image} alt={item.name} fill style={{ objectFit: 'cover' }} />
                                </div>
                                <div style={{ flex: 1 }}>
                                    <h4 style={{ fontSize: '0.9rem', marginBottom: '0.2rem' }}>{item.name}</h4>
                                    <p style={{ color: 'var(--accent-hover)', fontWeight: '600', fontSize: '0.9rem' }}>${item.price.toFixed(2)}</p>

                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                                        <button style={{ padding: '0.2rem 0.5rem', background: 'var(--bg-surface-elevated)', borderRadius: '4px' }} onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                                        <span style={{ fontSize: '0.9rem' }}>{item.quantity}</span>
                                        <button style={{ padding: '0.2rem 0.5rem', background: 'var(--bg-surface-elevated)', borderRadius: '4px' }} onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                                    </div>
                                </div>
                                <button style={{ color: 'var(--text-secondary)' }} onClick={() => removeFromCart(item.id)}>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                </button>
                            </div>
                        ))
                    )}
                </div>

                {cart.length > 0 && (
                    <div style={{ padding: '1.5rem', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-surface-elevated)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', fontSize: '1.2rem', fontWeight: 'bold' }}>
                            <span>Subtotal</span>
                            <span>${cartTotal.toFixed(2)}</span>
                        </div>
                        <Link href="/checkout" className="btn btn-primary" style={{ width: '100%', padding: '1rem' }} onClick={() => setIsCartOpen(false)}>
                            Proceed to Checkout
                        </Link>
                    </div>
                )}
            </div>

            <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); }
          to { transform: translateX(0); }
        }
      `}</style>
        </>
    );
}
