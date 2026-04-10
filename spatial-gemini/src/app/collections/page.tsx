import Link from "next/link";
import Image from "next/image";

export default function Collections() {
    const collections = [
        {
            id: "minimalist-office",
            name: "The Minimalist Office",
            description: "Everything you need for a distraction-free, aesthetically pleasing workspace.",
            image: "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?q=80&w=1200&auto=format&fit=crop"
        },
        {
            id: "travel-ready",
            name: "Travel Ready",
            description: "Durable, high-performance gear built for the modern digital nomad.",
            image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=1200&auto=format&fit=crop"
        },
        {
            id: "audiophile",
            name: "Audiophile Essentials",
            description: "Uncompromising sound quality for those who refuse to settle.",
            image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?q=80&w=1200&auto=format&fit=crop"
        }
    ];

    return (
        <div className="container" style={{ padding: '6rem 2rem', minHeight: '80vh' }}>
            <header style={{ marginBottom: '4rem', textAlign: 'center' }}>
                <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem' }}>Collections</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
                    Curated sets of our finest gear, designed to work perfectly in tandem.
                </p>
            </header>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '4rem' }}>
                {collections.map((collection, index) => (
                    <div key={collection.id} style={{ display: 'grid', gridTemplateColumns: index % 2 === 0 ? '1fr 1fr' : '1fr 1fr', gap: '4rem', alignItems: 'center' }}>
                        <div style={{ order: index % 2 === 0 ? 1 : 2, position: 'relative', width: '100%', height: '400px', borderRadius: 'var(--border-radius-lg)', overflow: 'hidden' }}>
                            <Image src={collection.image} alt={collection.name} fill style={{ objectFit: 'cover' }} sizes="(max-width: 768px) 100vw, 50vw" />
                        </div>

                        <div style={{ order: index % 2 === 0 ? 2 : 1, padding: '2rem' }}>
                            <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>{collection.name}</h2>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', lineHeight: '1.8', marginBottom: '2rem' }}>
                                {collection.description}
                            </p>
                            <Link href={`/shop?collection=${collection.id}`} className="btn btn-secondary" style={{ padding: '1rem 2rem' }}>
                                Explore Collection
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
