import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HiArrowUp } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

export default function ScrollToTop() {
    const [visible, setVisible] = useState(false);
    const { isDark } = useTheme();

    useEffect(() => {
        const handleScroll = () => setVisible(window.scrollY > 400);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <AnimatePresence>
            {visible && (
                <motion.button
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    className="fixed bottom-8 right-8 z-40 w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent text-white flex items-center justify-center shadow-lg shadow-primary/25 hover:scale-110 hover:shadow-xl transition-all duration-300"
                    aria-label="Scroll to top"
                >
                    <HiArrowUp className="text-xl" />
                </motion.button>
            )}
        </AnimatePresence>
    );
}
