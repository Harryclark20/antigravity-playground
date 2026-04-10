import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HiMenu, HiX } from 'react-icons/hi';
import { BsSunFill, BsMoonStarsFill } from 'react-icons/bs';
import { useTheme } from '../context/ThemeContext';

const navLinks = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Skills', href: '#skills' },
    { name: 'Projects', href: '#projects' },
    { name: 'Experience', href: '#experience' },
    { name: 'Certifications', href: '#certifications' },
    { name: 'Contact', href: '#contact' },
];

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
    const [hidden, setHidden] = useState(false);
    const { isDark, toggleTheme } = useTheme();

    useEffect(() => {
        const handleScroll = () => {
            const currentScrollY = window.scrollY;

            // Add background after scrolling 20px
            setScrolled(currentScrollY > 20);

            // Hide navbar completely if not at the top (past 100px)
            if (currentScrollY > 100) {
                setHidden(true);
                setIsOpen(false); // Close mobile menu if open
            } else {
                setHidden(false);
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <motion.nav
            initial={{ y: -100 }}
            animate={{ y: hidden ? -100 : 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className={`fixed top-0 left-0 right-0 z-50 transition-colors duration-300 ${scrolled ? 'glass shadow-lg' : 'bg-transparent'
                }`}
        >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 lg:h-18">
                    <a href="#home" className="text-xl font-bold gradient-text tracking-tight">
                        Oliver.dev
                    </a>

                    <div className="hidden md:flex items-center gap-1">
                        {navLinks.map((link) => (
                            <a
                                key={link.name}
                                href={link.href}
                                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:text-primary ${isDark
                                    ? 'text-dark-muted hover:bg-white/5'
                                    : 'text-light-muted hover:bg-black/5'
                                    }`}
                            >
                                {link.name}
                            </a>
                        ))}
                        <div className={`w-px h-6 mx-2 ${isDark ? 'bg-dark-border' : 'bg-light-border'}`} />
                        <button
                            onClick={toggleTheme}
                            className={`p-2.5 rounded-xl transition-all duration-300 hover:scale-110 ${isDark
                                ? 'hover:bg-white/10 text-yellow-400'
                                : 'hover:bg-black/5 text-indigo-500'
                                }`}
                            aria-label="Toggle theme"
                        >
                            {isDark ? <BsSunFill size={16} /> : <BsMoonStarsFill size={16} />}
                        </button>
                    </div>

                    <div className="flex md:hidden items-center gap-1">
                        <button
                            onClick={toggleTheme}
                            className={`p-2 rounded-lg ${isDark ? 'text-yellow-400' : 'text-indigo-500'}`}
                            aria-label="Toggle theme"
                        >
                            {isDark ? <BsSunFill size={16} /> : <BsMoonStarsFill size={16} />}
                        </button>
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className={`p-2 rounded-lg ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}
                            aria-label="Menu"
                        >
                            {isOpen ? <HiX size={22} /> : <HiMenu size={22} />}
                        </button>
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className={`md:hidden border-t ${isDark ? 'border-dark-border bg-dark-surface/95 backdrop-blur-xl' : 'border-light-border bg-light-surface/95 backdrop-blur-xl'
                            }`}
                    >
                        <div className="px-4 py-3 space-y-1">
                            {navLinks.map((link) => (
                                <a
                                    key={link.name}
                                    href={link.href}
                                    onClick={() => setIsOpen(false)}
                                    className={`block px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200 ${isDark ? 'text-dark-muted hover:text-primary hover:bg-white/5' : 'text-light-muted hover:text-primary hover:bg-black/5'
                                        }`}
                                >
                                    {link.name}
                                </a>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.nav>
    );
}
