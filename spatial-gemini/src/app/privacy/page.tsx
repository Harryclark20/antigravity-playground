export default function Privacy() {
    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh', maxWidth: '800px' }}>
            <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Privacy Policy</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '3rem' }}>Last Updated: October 2024</p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem', color: 'var(--text-secondary)', lineHeight: '1.8' }}>
                <p>
                    At AURA, we take your privacy seriously. This Privacy Policy outlines how we collect, use, and protect your personal information when you visit our website, purchase our products, or interact with us.
                </p>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>1. Information We Collect</h2>
                    <p>
                        We collect information that you manually provide to us (such as your name, shipping address, email, and payment details during checkout). We also automatically collect certain technical information (such as your IP address, browser type, and operating system) when you navigate aurastore.com.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>2. How We Use Your Information</h2>
                    <p>
                        We use the order information that we collect generally to fulfill any orders placed through the Site (including processing your payment information, arranging for shipping, and providing you with invoices and/or order confirmations). Additionally, we use this order information to communicate with you and screen orders for potential risk or fraud.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>3. Data Sharing</h2>
                    <p>
                        We do not sell, trade, or otherwise transfer to outside parties your Personally Identifiable Information unless we provide users with advance notice. This does not include website hosting partners and other parties who assist us in operating our website, conducting our business, or serving our users, so long as those parties agree to keep this information confidential.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>4. Your Rights</h2>
                    <p>
                        If you are a European resident, you have the right to access personal information we hold about you and to ask that your personal information be corrected, updated, or deleted. If you would like to exercise this right, please contact us through our Contact page.
                    </p>
                </section>
            </div>
        </div>
    );
}
