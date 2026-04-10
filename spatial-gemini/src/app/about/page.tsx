import Image from "next/image";

export default function About() {
    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6rem', alignItems: 'center', marginBottom: '6rem' }}>
                <div>
                    <h1 style={{ fontSize: '4rem', lineHeight: '1.1', marginBottom: '2rem' }}>Form meets <br /><span style={{ color: 'var(--accent-color)' }}>function.</span></h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', lineHeight: '1.8', marginBottom: '1.5rem' }}>
                        AURA was founded in 2024 with a singular vision: to create technology and lifestyle products that don't just perform flawlessly, but look beautiful doing it.
                    </p>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', lineHeight: '1.8' }}>
                        We observed a market saturated with chaotic designs and unnecessary features. Our response was a return to minimalism – stripping away the excess to reveal the pure essence of what a product should be.
                    </p>
                </div>
                <div style={{ position: 'relative', width: '100%', height: '600px', borderRadius: 'var(--border-radius-lg)', overflow: 'hidden' }}>
                    <Image src="https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?q=80&w=1200&auto=format&fit=crop" alt="Our Design Studio" fill style={{ objectFit: 'cover' }} />
                </div>
            </div>

            <div style={{ backgroundColor: 'var(--bg-surface)', padding: '4rem', borderRadius: 'var(--border-radius-lg)', textAlign: 'center' }}>
                <h2 style={{ fontSize: '2.5rem', marginBottom: '3rem' }}>Our Core Values</h2>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
                    <div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Uncompromising Quality</h3>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>We source only the finest materials, ensuring every product is built to last a lifetime.</p>
                    </div>
                    <div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Relentless Minimalism</h3>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>If a feature doesn't serve a distinct purpose or elevate the aesthetic, it doesn't make the cut.</p>
                    </div>
                    <div>
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>Sustainable Innovation</h3>
                        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>We are committed to reducing our carbon footprint through eco-friendly packaging and ethical sourcing.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
