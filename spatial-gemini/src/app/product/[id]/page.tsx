"use client";

import Image from "next/image";
import Link from "next/link";
import React from "react";
import { useCart } from "@/context/CartContext";
import { getProductById } from "@/data/products";

export default function ProductPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = React.use(params);
    const { addToCart } = useCart();

    const product = getProductById(id);

    if (!product) {
        return (
            <div className="container" style={{ padding: '8rem 2rem', textAlign: 'center', minHeight: '80vh' }}>
                <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Product Not Found</h1>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Sorry, the product you are looking for does not exist.</p>
                <Link href="/shop" className="btn btn-primary">Back to Shop</Link>
            </div>
        );
    }

    const handleAdd = () => {
        addToCart({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image
        });
    };

    return (
        <div className="container" style={{ padding: '4rem 2rem', minHeight: '80vh' }}>
            <div style={{ marginBottom: '2rem' }}>
                <Link href="/shop" style={{ color: 'var(--text-secondary)', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
                    &larr; Back to Shop
                </Link>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '4rem', alignItems: 'center' }}>
                <div style={{ position: 'relative', width: '100%', aspectRatio: '1/1', backgroundColor: 'var(--bg-surface-elevated)', borderRadius: 'var(--border-radius-lg)', overflow: 'hidden' }}>
                    <Image src={product.image} alt={product.name} fill style={{ objectFit: 'cover' }} priority sizes="(max-width: 768px) 100vw, 50vw" />
                    {product.isNewArrival && (
                        <span style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', background: 'var(--accent-color)', color: '#fff', fontSize: '0.8rem', fontWeight: 'bold', padding: '0.4rem 0.8rem', borderRadius: '4px', textTransform: 'uppercase', zIndex: 10 }}>
                            New Arrival
                        </span>
                    )}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <h1 style={{ fontSize: 'clamp(2rem, 4vw, 3.5rem)', lineHeight: '1.1' }}>{product.name}</h1>
                    <p style={{ fontSize: '1.5rem', color: 'var(--accent-hover)', fontWeight: '600' }}>${product.price.toFixed(2)}</p>

                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', lineHeight: '1.8' }}>
                        {product.description}
                    </p>

                    <div style={{ marginTop: '1rem' }}>
                        <h3 style={{ marginBottom: '1rem', color: 'var(--text-primary)' }}>Key Features:</h3>
                        <ul style={{ listStylePosition: 'inside', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {product.features.map((feat: string, i: number) => (
                                <li key={i}>{feat}</li>
                            ))}
                        </ul>
                    </div>

                    <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                        <button className="btn btn-primary" onClick={handleAdd} style={{ flex: 1, padding: '1.2rem', fontSize: '1.1rem' }}>
                            Add to Cart
                        </button>
                        <button className="btn btn-secondary" style={{ padding: '1.2rem' }}>
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
