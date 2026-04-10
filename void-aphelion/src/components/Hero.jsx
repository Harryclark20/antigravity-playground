import { useState, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { HiArrowDown } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

function TypeWriter({ words, speed = 100, deleteSpeed = 50, pauseTime = 2000 }) {
    const [text, setText] = useState('');
    const [wordIndex, setWordIndex] = useState(0);
    const [isDeleting, setIsDeleting] = useState(false);

    useEffect(() => {
        const currentWord = words[wordIndex];
        let timeout;

        if (!isDeleting && text === currentWord) {
            timeout = setTimeout(() => setIsDeleting(true), pauseTime);
        } else if (isDeleting && text === '') {
            setIsDeleting(false);
            setWordIndex((prev) => (prev + 1) % words.length);
        } else {
            timeout = setTimeout(() => {
                setText(currentWord.substring(0, isDeleting ? text.length - 1 : text.length + 1));
            }, isDeleting ? deleteSpeed : speed);
        }

        return () => clearTimeout(timeout);
    }, [text, isDeleting, wordIndex, words, speed, deleteSpeed, pauseTime]);

    return (
        <span>
            {text}
            <span className="animate-pulse text-primary">|</span>
        </span>
    );
}

function StarField() {
    const stars = useMemo(() => (
        Array.from({ length: 60 }, (_, i) => ({
            id: i,
            x: Math.random() * 100,
            y: Math.random() * 100,
            size: Math.random() * 2 + 0.5,
            delay: Math.random() * 5,
            duration: Math.random() * 3 + 2,
        }))
    ), []);

    return (
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
            {stars.map((star) => (
                <div
                    key={star.id}
                    className="absolute rounded-full bg-white"
                    style={{
                        left: `${star.x}%`,
                        top: `${star.y}%`,
                        width: `${star.size}px`,
                        height: `${star.size}px`,
                        animation: `twinkle ${star.duration}s ease-in-out ${star.delay}s infinite`,
                    }}
                />
            ))}
        </div>
    );
}

export default function Hero() {
    const { isDark } = useTheme();
    const roles = [
        'DevOps Engineer',
        'Cloud Solutions Architect',
        'IT Support Specialist',
        'Web Developer',
    ];

    return (
        <section id="home" className="animated-gradient min-h-screen flex items-center justify-center relative overflow-hidden">
            {isDark && <StarField />}

            {/* Floating orbs */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <motion.div
                    animate={{ x: [0, 40, 0], y: [0, -30, 0] }}
                    transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute top-1/5 left-1/5 w-80 h-80 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(6,182,212,0.15), transparent 70%)',
                        filter: 'blur(40px)',
                    }}
                />
                <motion.div
                    animate={{ x: [0, -30, 0], y: [0, 40, 0] }}
                    transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute bottom-1/5 right-1/5 w-96 h-96 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(139,92,246,0.12), transparent 70%)',
                        filter: 'blur(50px)',
                    }}
                />
                <motion.div
                    animate={{ x: [0, 20, 0], y: [0, 20, 0] }}
                    transition={{ duration: 14, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute top-2/3 left-1/2 w-64 h-64 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(236,72,153,0.08), transparent 70%)',
                        filter: 'blur(40px)',
                    }}
                />
            </div>

            <div className="max-w-5xl mx-auto text-center px-4 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <span className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold tracking-wider uppercase mb-8 ${isDark
                        ? 'bg-primary/10 text-primary border border-primary/20'
                        : 'bg-primary/10 text-primary-dark border border-primary/20'
                        }`}>
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                        Available for Opportunities
                    </span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                    className="text-5xl sm:text-6xl md:text-8xl font-black mb-4 leading-[1.1] tracking-tight"
                >
                    Hi, I&apos;m{' '}
                    <span className="gradient-text">Oliver</span>
                </motion.h1>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.55 }}
                    className={`text-xl sm:text-2xl md:text-3xl font-medium mb-8 h-10 ${isDark ? 'text-dark-muted' : 'text-light-muted'
                        }`}
                >
                    <TypeWriter words={roles} speed={80} deleteSpeed={40} pauseTime={2500} />
                </motion.div>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.7 }}
                    className={`text-base sm:text-lg max-w-2xl mx-auto mb-12 leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'
                        }`}
                >
                    Microsoft Azure certified professional with a passion for DevOps,
                    infrastructure design, and building scalable CI/CD solutions that make a difference.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.85 }}
                    className="flex flex-col sm:flex-row items-center justify-center gap-4"
                >
                    <a
                        href="#projects"
                        className="group px-8 py-4 bg-gradient-to-r from-primary to-accent text-white rounded-xl font-semibold text-sm transition-all duration-300 hover:shadow-lg hover:shadow-primary/30 hover:scale-105 flex items-center gap-2"
                    >
                        View My Projects
                        <span className="group-hover:translate-x-1 transition-transform">→</span>
                    </a>
                    <a
                        href="#contact"
                        className={`px-8 py-4 rounded-xl font-semibold text-sm transition-all duration-300 hover:scale-105 border ${isDark
                            ? 'border-dark-border text-dark-text hover:bg-white/5 hover:border-primary/40'
                            : 'border-light-border text-light-text hover:bg-black/5 hover:border-primary/40'
                            }`}
                    >
                        Let&apos;s Connect
                    </a>
                </motion.div>

                {/* Stats bar */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 1.0 }}
                    className={`flex items-center justify-center gap-8 sm:gap-14 mt-16 pt-8 border-t ${isDark ? 'border-dark-border/50' : 'border-light-border/50'
                        }`}
                >
                    {[
                        { value: '1+', label: 'Years Experience' },
                        { value: '5+', label: 'Projects Built' },
                        { value: 'AZ-900', label: 'Certified' },
                    ].map((stat) => (
                        <div key={stat.label} className="text-center">
                            <div className="text-2xl sm:text-3xl font-bold gradient-text">{stat.value}</div>
                            <div className={`text-xs sm:text-sm mt-1 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                {stat.label}
                            </div>
                        </div>
                    ))}
                </motion.div>
            </div>

            <motion.div
                animate={{ y: [0, 8, 0] }}
                transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute bottom-8 left-1/2 -translate-x-1/2"
            >
                <a href="#about" className={`flex flex-col items-center gap-1 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                    <span className="text-xs">Scroll Down</span>
                    <HiArrowDown className="text-lg" />
                </a>
            </motion.div>
        </section>
    );
}
