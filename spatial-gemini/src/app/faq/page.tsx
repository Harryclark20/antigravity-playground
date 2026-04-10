export default function FAQ() {
    const faqs = [
        {
            question: "Do you ship internationally?",
            answer: "Yes, we ship to over 100 countries worldwide. International shipping costs are calculated at checkout based on your location and selected delivery speed."
        },
        {
            question: "What is your return policy?",
            answer: "We offer a 30-day no-questions-asked return policy. If you aren't completely satisfied with your AURA product, simply return it in its original packaging for a full refund."
        },
        {
            question: "How long is the warranty?",
            answer: "All AURA electronics come with a standard 1-year limited warranty covering manufacturing defects. Our premium lifestyle goods feature a 5-year warranty against material failure."
        },
        {
            question: "Can I cancel or change my order?",
            answer: "Orders can be modified or canceled within 2 hours of placement. Since we process orders quickly to ensure rapid delivery, changes cannot be made after this window."
        },
        {
            question: "Do your products work with Apple and Android devices?",
            answer: "Yes, our entire peripheral and audio line is designed to be completely platform agnostic, offering seamless Bluetooth 5.0 connectivity to iOS, Android, Windows, and macOS."
        }
    ];

    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh', maxWidth: '800px' }}>
            <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem', textAlign: 'center' }}>Frequently Asked Questions</h1>
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginBottom: '4rem', fontSize: '1.1rem' }}>
                Everything you need to know about AURA products and policies.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {faqs.map((faq, i) => (
                    <div key={i} style={{ backgroundColor: 'var(--bg-surface)', padding: '2rem', borderRadius: 'var(--border-radius-md)', border: '1px solid var(--border-color)' }}>
                        <h3 style={{ fontSize: '1.3rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>{faq.question}</h3>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>{faq.answer}</p>
                    </div>
                ))}
            </div>

            <div style={{ marginTop: '4rem', textAlign: 'center' }}>
                <p style={{ color: 'var(--text-secondary)' }}>Still have questions?</p>
                <a href="/contact" style={{ display: 'inline-block', color: 'var(--accent-color)', marginTop: '0.5rem', fontWeight: '500' }}>Contact our support team &rarr;</a>
            </div>
        </div>
    );
}
