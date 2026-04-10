"use client";

import Link from 'next/link';
import { useCart } from '@/context/CartContext';

export default function Navbar() {
    const { cartCount, setIsCartOpen } = useCart();

    return (
        <header className="header-nav">
            <div className="container header-container">
                <Link href="/" className="brand-logo">
                    AURA
                </Link>
                <nav className="nav-links">
                    <Link href="/" className="nav-link">Home</Link>
                    <Link href="/shop" className="nav-link">Shop</Link>
                    <Link href="/collections" className="nav-link">Collections</Link>
                    <Link href="/about" className="nav-link">About</Link>
                </nav>
                <div className="header-actions">
                    <button className="action-icon" aria-label="Search">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                    </button>
                    <button className="action-icon" aria-label="Cart" onClick={() => setIsCartOpen(true)} style={{ position: 'relative' }}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                            <line x1="3" y1="6" x2="21" y2="6"></line>
                            <path d="M16 10a4 4 0 0 1-8 0"></path>
                        </svg>
                        {cartCount > 0 && (
                            <span style={{ position: 'absolute', top: '-8px', right: '-8px', background: 'var(--accent-color)', color: '#fff', fontSize: '0.7rem', fontWeight: 'bold', width: '18px', height: '18px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {cartCount}
                            </span>
                        )}
                    </button>
                </div>
            </div>
        </header>
    );
}
