"use client";

import { useCart } from "@/context/CartContext";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

export default function CheckoutPage() {
    const { cart, cartTotal } = useCart();
    const [isProcessing, setIsProcessing] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);

    const handleCheckout = (e: React.FormEvent) => {
        e.preventDefault();
        setIsProcessing(true);
        // Simulate API call
        setTimeout(() => {
            setIsProcessing(false);
            setIsSuccess(true);
            // Ideally clear cart here
        }, 2000);
    };

    if (isSuccess) {
        return (
            <div className="container" style={{ padding: '8rem 2rem', textAlign: 'center', minHeight: '80vh' }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '80px', height: '80px', borderRadius: '50%', backgroundColor: 'rgba(123, 97, 255, 0.1)', color: 'var(--accent-color)', marginBottom: '2rem' }}>
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                </div>
                <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Order Confirmed</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', marginBottom: '3rem', maxWidth: '500px', margin: '0 auto 3rem' }}>
                    Thank you for your purchase. We've sent a confirmation email with your order details and tracking information.
                </p>
                <Link href="/shop" className="btn btn-primary" style={{ padding: '1rem 2rem' }}>
                    Continue Shopping
                </Link>
            </div>
        );
    }

    return (
        <div className="container" style={{ padding: '4rem 2rem', minHeight: '80vh' }}>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '3rem' }}>Checkout</h1>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '4rem', alignItems: 'start' }}>
                <form onSubmit={handleCheckout} style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>

                    <section>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>Contact Information</h2>
                        <div style={{ display: 'grid', gap: '1.5rem' }}>
                            <input type="email" placeholder="Email Address" required style={inputStyle} />
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <input type="text" placeholder="First Name" required style={{ ...inputStyle, flex: 1 }} />
                                <input type="text" placeholder="Last Name" required style={{ ...inputStyle, flex: 1 }} />
                            </div>
                        </div>
                    </section>

                    <section>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>Shipping Address</h2>
                        <div style={{ display: 'grid', gap: '1.5rem' }}>
                            <input type="text" placeholder="Street Address" required style={inputStyle} />
                            <input type="text" placeholder="Apt, Suite, etc. (optional)" style={inputStyle} />
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <input type="text" placeholder="City" required style={{ ...inputStyle, flex: 2 }} />
                                <input type="text" placeholder="State/Province" required style={{ ...inputStyle, flex: 1 }} />
                                <input type="text" placeholder="ZIP/Postal Code" required style={{ ...inputStyle, flex: 1 }} />
                            </div>
                        </div>
                    </section>

                    <section>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>Payment Details</h2>
                        <div style={{ display: 'grid', gap: '1.5rem' }}>
                            <input type="text" placeholder="Card Number" required style={inputStyle} />
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <input type="text" placeholder="MM/YY" required style={{ ...inputStyle, flex: 1 }} />
                                <input type="text" placeholder="CVC" required style={{ ...inputStyle, flex: 1 }} />
                            </div>
                            <input type="text" placeholder="Name on Card" required style={inputStyle} />
                        </div>
                    </section>

                    <button type="submit" className="btn btn-primary" disabled={isProcessing || cart.length === 0} style={{ padding: '1.2rem', fontSize: '1.1rem', marginTop: '1rem' }}>
                        {isProcessing ? 'Processing...' : `Pay $${cartTotal.toFixed(2)}`}
                    </button>
                </form>

                <div style={{ backgroundColor: 'var(--bg-surface-elevated)', padding: '2rem', borderRadius: 'var(--border-radius-md)', position: 'sticky', top: '100px', border: '1px solid var(--border-color)' }}>
                    <h2 style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>Order Summary</h2>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginBottom: '2rem' }}>
                        {cart.map(item => (
                            <div key={item.id} style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                <div style={{ position: 'relative', width: '60px', height: '60px', borderRadius: '6px', overflow: 'hidden', flexShrink: 0 }}>
                                    <Image src={item.image} alt={item.name} fill style={{ objectFit: 'cover' }} />
                                    <span style={{ position: 'absolute', top: '-5px', right: '-5px', background: 'var(--accent-color)', color: '#fff', fontSize: '0.7rem', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
                                        {item.quantity}
                                    </span>
                                </div>
                                <div style={{ flex: 1 }}>
                                    <h4 style={{ fontSize: '0.9rem', marginBottom: '0.2rem' }}>{item.name}</h4>
                                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Qty: {item.quantity}</p>
                                </div>
                                <div style={{ fontWeight: '500' }}>
                                    ${(item.price * item.quantity).toFixed(2)}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                            <span>Subtotal</span>
                            <span>${cartTotal.toFixed(2)}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                            <span>Shipping</span>
                            <span>Free</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 'bold', marginTop: '0.5rem', color: 'var(--text-primary)' }}>
                            <span>Total</span>
                            <span>${cartTotal.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

const inputStyle = {
    width: '100%',
    padding: '1rem',
    backgroundColor: 'var(--bg-surface)',
    border: '1px solid var(--border-color)',
    borderRadius: 'var(--border-radius-sm)',
    color: 'var(--text-primary)',
    fontFamily: 'var(--font-body)',
    fontSize: '1rem',
    outline: 'none',
    transition: 'border-color var(--transition-fast)'
};
