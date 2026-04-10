export interface Product {
    id: string;
    name: string;
    price: number;
    category: string;
    description: string;
    features: string[];
    image: string;
    isNewArrival?: boolean;
}

export const products: Product[] = [
    {
        id: "prod_1",
        name: "Aura Noise-Cancelling Headphones",
        price: 299.00,
        category: "Audio",
        description: "Experience silence like never before with our industry-leading noise cancellation technology. Crafted from premium materials for all-day comfort, the Aura Headphones deliver uncompromising audio fidelity in a remarkably sleek silhouette.",
        features: ["Active Noise Cancellation", "40-Hour Battery Life", "Spatial Audio Support", "Memory Foam Earcups"],
        image: "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_2",
        name: "Minimalist Smartwatch Series X",
        price: 199.00,
        category: "Wearables",
        description: "Stay connected without the distraction. The Series X seamlessly blends a classic timepiece aesthetic with state-of-the-art health tracking and notification capabilities.",
        features: ["Always-On OLED Display", "Heart Rate & Sleep Monitoring", "7-Day Battery", "Water Resistant (5ATM)"],
        image: "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_3",
        name: "Ergonomic Mechanical Keyboard",
        price: 149.00,
        category: "Peripherals",
        description: "Type with unprecedented comfort and speed. Our custom-designed tactile switches provide the perfect balance of feedback and silence, housed in a machined aluminum chassis.",
        features: ["Custom Tactile Switches", "Hot-Swappable PCB", "RGB Backlighting", "Wireless Bluetooth 5.0"],
        image: "https://images.unsplash.com/photo-1595225476474-87563907a212?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: true
    },
    {
        id: "prod_4",
        name: "Ultra-Thin Laptop Sleeve",
        price: 49.00,
        category: "Accessories",
        description: "Protect your device in style. This sleeve is crafted from water-resistant vegan leather and features a soft microfiber interior to prevent scratches.",
        features: ["Water-Resistant Exterior", "Microfiber Lining", "Magnetic Closure", "Fits up to 14-inch laptops"],
        image: "https://images.unsplash.com/photo-1603313011101-320f26a4f6f6?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_5",
        name: "Studio Condenser Microphone",
        price: 159.00,
        category: "Audio",
        description: "Elevate your voice. Whether you are podcasting, streaming, or recording vocals, this studio-grade condenser microphone ensures crystal clear capture.",
        features: ["Cardioid Polar Pattern", "Internal Pop Filter", "USB-C Connectivity", "Zero-Latency Monitoring"],
        image: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: true
    },
    {
        id: "prod_6",
        name: "Wireless Charging Pad",
        price: 39.00,
        category: "Accessories",
        description: "Fast wire-free power in a minimalist package. Its sleek glass surface and weighted aluminum base make it a beautiful addition to any desk or nightstand.",
        features: ["15W Fast Charging", "Qi-Compatible", "Non-Slip Base", "LED Indicator"],
        image: "https://images.unsplash.com/photo-1622445275463-afa2ab738c34?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_7",
        name: "Aura Soundbar Pro",
        price: 349.00,
        category: "Audio",
        description: "Cinematic sound for your living room. The Aura Soundbar Pro delivers immersive 3D audio in an unbelievably slim profile.",
        features: ["Dolby Atmos Support", "Wireless Subwoofer Included", "HDMI eARC", "Bluetooth 5.2"],
        image: "https://images.unsplash.com/photo-1545454675-3531b543be5d?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: true
    },
    {
        id: "prod_8",
        name: "Nomad Travel Backpack",
        price: 129.00,
        category: "Accessories",
        description: "The ultimate companion for the modern commuter. Features a dedicated laptop compartment, weather-resistant zippers, and hidden security pockets.",
        features: ["25L Capacity", "Waterproof Nylon", "TSA-Approved Laptop Sleeve", "Ergonomic Straps"],
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_9",
        name: "Precision Wireless Mouse",
        price: 89.00,
        category: "Peripherals",
        description: "Engineered for maximum productivity. Seamlessly sculpts to your hand and features customizable buttons and multi-device connection limits.",
        features: ["4000 DPI Sensor", "Rechargeable Battery (70 days)", "Scroll Wheel with Free-Spin", "Connects to 3 Devices"],
        image: "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: true
    },
    {
        id: "prod_10",
        name: "Fitness Tracker Band",
        price: 79.00,
        category: "Wearables",
        description: "Simply discreet health monitoring. It goes unnoticed on your wrist while keeping exact track of your daily activity, heart rate, and sleep quality.",
        features: ["14-Day Battery", "SpO2 Tracking", "Swimproof Design", "Auto-Workout Detection"],
        image: "https://images.unsplash.com/photo-1557438159-51eec7a6c9e8?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    },
    {
        id: "prod_11",
        name: "Smart Desk Lamp",
        price: 69.00,
        category: "Accessories",
        description: "Illumination adapted to your focus. Adjustable color temperature and brightness via touch controls or our companion app.",
        features: ["Auto-Dimming Sensor", "Color Temp: 2700K - 6500K", "Wireless Charging Base", "Voice Assistant Compatible"],
        image: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: true
    },
    {
        id: "prod_12",
        name: "Pro Gaming Headset",
        price: 179.00,
        category: "Audio",
        description: "Hear every footstep. Featuring ultra-low latency wireless technology and THX Spatial Audio for the ultimate competitive advantage.",
        features: ["THX Spatial Audio", "Detachable Noise-Cancelling Mic", "Cooling Gel Ear Cushions", "2.4GHz Wireless"],
        image: "https://images.unsplash.com/photo-1599669454699-248893623440?q=80&w=1200&auto=format&fit=crop",
        isNewArrival: false
    }
];

export const getProductById = (id: string) => {
    return products.find(p => p.id === id);
};
