import { motion } from 'framer-motion';
import { HiExternalLink, HiCode } from 'react-icons/hi';
import { SiGithub } from 'react-icons/si';
import { useTheme } from '../context/ThemeContext';

const projects = [
    {
        title: 'Revils Tech',
        description:
            'A modern tech e-commerce website featuring product listings, shopping cart, user authentication, and a sleek interface for browsing and purchasing tech products.',
        tech: ['React', 'Tailwind CSS', 'JavaScript'],
        github: 'https://github.com/HarryClark20',
        demo: '#',
        color: 'from-cyan-500 to-blue-600',
        emoji: '🛒',
    },
    {
        title: 'Sweetone',
        description:
            'An intuitive food ordering portal featuring a diverse menu, seamless checkout flow, and elegant responsive design for an optimized user experience.',
        tech: ['HTML', 'CSS', 'JavaScript'],
        github: 'https://github.com/HarryClark20',
        demo: '#',
        color: 'from-orange-500 to-red-500',
        emoji: '🍔',
    },
    {
        title: 'Asset Management System',
        description:
            'A web-based asset tracking system for organizations to manage, track, and maintain assets with real-time Firebase database updates and reporting.',
        tech: ['HTML', 'CSS', 'JavaScript', 'Firebase'],
        github: 'https://github.com/HarryClark20',
        demo: '#',
        color: 'from-violet-500 to-purple-600',
        emoji: '📊',
    },
];

export default function Projects() {
    const { isDark } = useTheme();

    return (
        <section id="projects" className="section-padding">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        My work
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        Featured <span className="gradient-text">Projects</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full mb-6" />
                    <p className={`max-w-xl mx-auto ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                        A collection of projects showcasing my skills in web development and machine learning.
                    </p>
                </motion.div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {projects.map((project, i) => (
                        <motion.div
                            key={project.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: '-80px' }}
                            transition={{ duration: 0.5, delay: i * 0.08 }}
                            className="glass rounded-2xl overflow-hidden glow glow-hover group hover:scale-[1.02] transition-all duration-300 relative"
                        >
                            {/* Gradient header */}
                            <div className={`h-32 bg-gradient-to-br ${project.color} flex items-center justify-center relative overflow-hidden`}>
                                <div className="absolute inset-0 bg-black/10" />
                                <span className="text-5xl relative z-10">{project.emoji}</span>
                                {/* Dots pattern */}
                                <div className="absolute inset-0 opacity-20" style={{
                                    backgroundImage: 'radial-gradient(circle, white 1px, transparent 1px)',
                                    backgroundSize: '16px 16px',
                                }} />
                            </div>

                            <div className="p-6">
                                <div className="flex items-start justify-between mb-3">
                                    <h3 className="text-lg font-bold">{project.title}</h3>
                                    <div className="flex gap-1.5">
                                        <a
                                            href={project.github}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${isDark ? 'hover:bg-white/10 text-dark-muted hover:text-white' : 'hover:bg-black/5 text-light-muted hover:text-black'
                                                }`}
                                            aria-label={`${project.title} GitHub`}
                                        >
                                            <SiGithub size={16} />
                                        </a>
                                        <a
                                            href={project.demo}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className={`p-2 rounded-lg transition-all duration-200 hover:scale-110 ${isDark ? 'hover:bg-white/10 text-dark-muted hover:text-white' : 'hover:bg-black/5 text-light-muted hover:text-black'
                                                }`}
                                            aria-label={`${project.title} Live Demo`}
                                        >
                                            <HiExternalLink size={16} />
                                        </a>
                                    </div>
                                </div>

                                <p className={`text-sm leading-relaxed mb-5 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                    {project.description}
                                </p>

                                <div className="flex flex-wrap gap-2">
                                    {project.tech.map((t) => (
                                        <span
                                            key={t}
                                            className={`px-3 py-1 rounded-full text-xs font-medium ${isDark
                                                ? 'bg-white/[0.05] text-primary border border-white/[0.08]'
                                                : 'bg-primary/5 text-primary-dark border border-primary/10'
                                                }`}
                                        >
                                            {t}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
