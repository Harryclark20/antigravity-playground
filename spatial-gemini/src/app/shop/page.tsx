import Link from "next/link";
import Image from "next/image";
import { products } from "@/data/products";

export default function Shop({ searchParams }: { searchParams?: { category?: string } }) {
    // Extract unique categories
    const categories = ["All", ...Array.from(new Set(products.map(p => p.category)))];

    // Allow filtering (client-side simple version or just visually present it for now, 
    // currently we'll just display all for visual density since there are 12 items).
    const displayedProducts = products;

    return (
        <div className="container" style={{ padding: '4rem 2rem' }}>
            <header style={{ marginBottom: '3rem' }}>
                <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Shop All</h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>
                    Explore our complete collection of premium tech and lifestyle products.
                </p>
            </header>

            <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap', marginBottom: '3rem' }}>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    {categories.map(cat => (
                        <button key={cat} className="btn btn-secondary" style={{ padding: '0.4rem 1rem', fontSize: '0.85rem' }}>
                            {cat}
                        </button>
                    ))}
                </div>
            </div>

            <div className="product-grid">
                {displayedProducts.map((product) => (
                    <Link href={`/product/${product.id}`} key={product.id} className="product-card">
                        <div className="product-image-container">
                            <Image src={product.image} alt={product.name} fill className="product-image" sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw" />
                            {product.isNewArrival && (
                                <span style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'var(--accent-color)', color: '#fff', fontSize: '0.7rem', fontWeight: 'bold', padding: '0.3rem 0.6rem', borderRadius: '4px', textTransform: 'uppercase' }}>
                                    New
                                </span>
                            )}
                        </div>
                        <div className="product-info">
                            <span className="product-category">{product.category}</span>
                            <h3 className="product-name">{product.name}</h3>
                            <p className="product-price">${product.price.toFixed(2)}</p>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
