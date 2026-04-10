export default function Shipping() {
    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh', maxWidth: '800px' }}>
            <h1 style={{ fontSize: '3.5rem', marginBottom: '1.5rem', textAlign: 'center' }}>Shipping & Returns</h1>
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginBottom: '4rem', fontSize: '1.1rem' }}>
                Our commitment to you doesn't end when you place an order.
            </p>

            <section style={{ marginBottom: '4rem' }}>
                <h2 style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'var(--text-primary)', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>Shipping Policy</h2>
                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.8', marginBottom: '1rem' }}>
                    We offer complimentary standard shipping on all orders over $150 within the United States. For international orders, shipping rates are calculated dynamically at checkout based on your delivery address and preferred courier speed.
                </p>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', paddingLeft: '1.5rem', marginBottom: '1.5rem' }}>
                    <li><strong>Standard US Shipping:</strong> 3-5 business days</li>
                    <li><strong>Expedited US Shipping:</strong> 2 business days</li>
                    <li><strong>Overnight US Shipping:</strong> Next business day</li>
                    <li><strong>International Shipping:</strong> 7-14 business days</li>
                </ul>
                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.8' }}>
                    Orders are processed and shipped within 24 hours of placement, excluding weekends and public holidays. Once your order ships, you will receive a tracking confirmation email.
                </p>
            </section>

            <section>
                <h2 style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'var(--text-primary)', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>Return Policy</h2>
                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.8', marginBottom: '1rem' }}>
                    AURA products are backed by our 30-Day Happiness Guarantee. If you are unsatisfied with your product for any reason, you may return it within 30 days of receipt for a full refund to the original payment method.
                </p>
                <ol style={{ color: 'var(--text-secondary)', lineHeight: '1.8', paddingLeft: '1.5rem', marginBottom: '1.5rem' }}>
                    <li>Ensure the item is in completely original condition with all packaging included.</li>
                    <li>Contact our support team via the <a href="/contact" style={{ color: 'var(--accent-color)' }}>Contact</a> page to initiate a return request.</li>
                    <li>Print the provided prepaid return label and drop the package off at your nearest carrier location.</li>
                    <li>Refunds are processed within 3-5 business days of us receiving the item back at our facility.</li>
                </ol>
            </section>
        </div>
    );
}
