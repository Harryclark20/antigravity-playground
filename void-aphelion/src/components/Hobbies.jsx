import { motion } from 'framer-motion';
import { useTheme } from '../context/ThemeContext';

const hobbies = [
    { emoji: '📚', name: 'Reading', description: 'Books on tech, self-development, and cloud architecture.' },
    { emoji: '✍️', name: 'Writing', description: 'Technical articles and personal reflections.' },
    { emoji: '🎬', name: 'Movies', description: 'Sci-fi, tech thrillers, and documentaries.' },
    { emoji: '🎮', name: 'Gaming', description: 'Strategy and simulation games.' },
    { emoji: '🔧', name: 'Fixing Devices', description: 'Repairing laptops and mobile phones.' },
    { emoji: '💻', name: 'Coding', description: 'Building side projects and learning new tech.' },
];

export default function Hobbies() {
    const { isDark } = useTheme();

    return (
        <section className="section-padding">
            <div className="max-w-5xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-14"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        Beyond work
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        Hobbies & <span className="gradient-text">Interests</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full" />
                </motion.div>

                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                    {hobbies.map((hobby, i) => (
                        <motion.div
                            key={hobby.name}
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.4, delay: i * 0.06 }}
                            className="glass rounded-2xl p-5 text-center glow-hover hover:scale-105 transition-all duration-300 group cursor-default"
                        >
                            <div className="text-3xl mb-3 group-hover:scale-125 transition-transform duration-300">
                                {hobby.emoji}
                            </div>
                            <h3 className="text-sm font-bold mb-1">{hobby.name}</h3>
                            <p className={`text-xs leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                {hobby.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
