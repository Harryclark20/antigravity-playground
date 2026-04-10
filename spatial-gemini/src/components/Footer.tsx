import Link from 'next/link';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="container footer-container">
                <div className="footer-column">
                    <Link href="/" className="brand-logo" style={{ fontSize: '1.5rem', marginBottom: '1rem', display: 'inline-block' }}>
                        AURA
                    </Link>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.6' }}>
                        Elevating modern tech and fashion. Designed for those who appreciate the profound aesthetic of deep contrasts.
                    </p>
                </div>

                <div className="footer-column">
                    <h4>Shop</h4>
                    <div className="footer-links">
                        <Link href="/shop?category=new">New Arrivals</Link>
                        <Link href="/shop?category=bestsellers">Bestsellers</Link>
                        <Link href="/shop?category=accessories">Accessories</Link>
                    </div>
                </div>

                <div className="footer-column">
                    <h4>Support</h4>
                    <div className="footer-links">
                        <Link href="/faq">FAQ</Link>
                        <Link href="/shipping">Shipping & Returns</Link>
                        <Link href="/contact">Contact Us</Link>
                    </div>
                </div>

                <div className="footer-column">
                    <h4>Legal</h4>
                    <div className="footer-links">
                        <Link href="/terms">Terms of Service</Link>
                        <Link href="/privacy">Privacy Policy</Link>
                    </div>
                </div>
            </div>

            <div className="container footer-bottom">
                <p>&copy; {new Date().getFullYear()} AURA Store. All rights reserved.</p>
            </div>
        </footer>
    );
}
