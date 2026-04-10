"use client";

import { useState } from "react";

export default function Contact() {
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
    };

    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh', maxWidth: '800px' }}>
            <h1 style={{ fontSize: '3.5rem', marginBottom: '1.5rem', textAlign: 'center' }}>Contact Us</h1>
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginBottom: '4rem', fontSize: '1.1rem' }}>
                We're here to help. Reach out to our dedicated support team or visit us at our flagship studio.
            </p>

            {isSubmitted ? (
                <div style={{ textAlign: 'center', padding: '4rem', backgroundColor: 'var(--bg-surface-elevated)', borderRadius: 'var(--border-radius-lg)' }}>
                    <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '60px', height: '60px', borderRadius: '50%', backgroundColor: 'rgba(123, 97, 255, 0.1)', color: 'var(--accent-color)', marginBottom: '1.5rem' }}>
                        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <h2 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Message Received</h2>
                    <p style={{ color: 'var(--text-secondary)' }}>Thank you for reaching out. A member of our team will respond to your inquiry within 24 hours.</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 2fr) 1fr', gap: '3rem' }}>
                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                            <input type="text" placeholder="First Name" required style={inputStyle} />
                            <input type="text" placeholder="Last Name" required style={inputStyle} />
                        </div>
                        <input type="email" placeholder="Email Address" required style={inputStyle} />
                        <input type="text" placeholder="Topic (Shipping, Warranty, etc.)" required style={inputStyle} />
                        <textarea placeholder="Your Message" required rows={6} style={{ ...inputStyle, resize: 'vertical' }}></textarea>
                        <button type="submit" className="btn btn-primary" style={{ padding: '1rem' }}>Send Message</button>
                    </form>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                        <div>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>Email Us</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>support@aurastore.com<br />careers@aurastore.com</p>
                        </div>
                        <div>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>Call Us</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>+1 (888) 123-4567<br />Mon-Fri, 9am - 6pm EST</p>
                        </div>
                        <div>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>Headquarters</h3>
                            <p style={{ color: 'var(--text-secondary)' }}>123 Minimalist Avenue<br />Design District<br />New York, NY 10001</p>
                        </div>
                    </div>
                </div>
            )}
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
