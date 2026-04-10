export default function Terms() {
    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh', maxWidth: '800px' }}>
            <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Terms of Service</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '3rem' }}>Last Updated: October 2024</p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem', color: 'var(--text-secondary)', lineHeight: '1.8' }}>
                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>1. Acceptance of Terms</h2>
                    <p>
                        By accessing and using aurastore.com (the "Site"), you accept and agree to be bound by the terms and provision of this agreement. In addition, when using this Site's particular services, you shall be subject to any posted guidelines or rules applicable to such services.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>2. Intellectual Property</h2>
                    <p>
                        The Site and its original content, features, and functionality are owned by AURA Inc. and are protected by international copyright, trademark, patent, trade secret, and other intellectual property or proprietary rights laws.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>3. User Accounts</h2>
                    <p>
                        If you create an account on the Site, you are responsible for maintaining the security of your account, and you are fully responsible for all activities that occur under the account and any other actions taken in connection with it.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>4. Products and Pricing</h2>
                    <p>
                        All products are subject to availability, and we cannot guarantee that items will be in stock. We reserve the right to discontinue any products at any time for any reason. Prices for all products are subject to change.
                    </p>
                </section>

                <section>
                    <h2 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '1rem' }}>5. Limitation of Liability</h2>
                    <p>
                        In no event shall AURA Inc., nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the Service.
                    </p>
                </section>
            </div>
        </div>
    );
}
