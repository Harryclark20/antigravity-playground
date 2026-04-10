import Link from "next/link";
import Image from "next/image";
import { products } from "@/data/products";

export default function Home() {
  const featuredProducts = products.filter(p => p.isNewArrival).slice(0, 4);

  return (
    <>
      <section className="hero">
        <div className="hero-bg">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
        </div>
        <div className="container hero-content">
          <span className="hero-badge">NEW COLLECTION 2026</span>
          <h1 className="hero-title">Experience <br />The Future of Minimal.</h1>
          <p className="hero-subtitle">Premium tech and apparel curated for the modern aesthete. Discover striking designs that blend seamlessly into your lifestyle.</p>
          <div className="hero-actions">
            <Link href="/shop" className="btn btn-primary">Shop Now</Link>
            <Link href="/collections" className="btn btn-secondary">Explore</Link>
          </div>
        </div>
      </section>

      <section className="featured-section">
        <div className="container">
          <div className="section-header">
            <h2>New Arrivals</h2>
            <Link href="/shop?category=new" className="view-all-link">View All</Link>
          </div>
          <div className="product-grid">
            {featuredProducts.map((product) => (
              <Link href={`/product/${product.id}`} key={product.id} className="product-card">
                <div className="product-image-container">
                  <Image src={product.image} alt={product.name} fill className="product-image" sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw" />
                  <span style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'var(--accent-color)', color: '#fff', fontSize: '0.7rem', fontWeight: 'bold', padding: '0.3rem 0.6rem', borderRadius: '4px', textTransform: 'uppercase' }}>
                    New
                  </span>
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
      </section>

      <section className="manifesto-section">
        <div className="container manifesto-container">
          <h2 className="manifesto-title">Designed for distinction.</h2>
          <p className="manifesto-text">We believe in fewer, but better things. Every product in the Aura collection is rigorously selected for its uncompromising quality and stunning aesthetic.</p>
        </div>
      </section>
    </>
  );
}
