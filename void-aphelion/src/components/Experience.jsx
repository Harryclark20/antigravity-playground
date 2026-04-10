import { motion } from 'framer-motion';
import { HiBriefcase, HiCalendar, HiLocationMarker } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

const experiences = [
    {
        title: 'IT Support Specialist',
        company: 'Pan-Atlantic University',
        period: 'January 2026 – Present',
        location: 'Lagos, Nigeria',
        type: 'Full-time',
        description: [
            'Providing comprehensive IT support including troubleshooting laptops, desktops, and mobile devices.',
            'Managing and maintaining campus IT infrastructure for optimal performance.',
            'Assisting faculty and staff with software installations, network issues, and system configurations.',
            'Repairing hardware faults in laptops and phones, including component-level fixes.',
        ],
        color: 'from-cyan-500 to-blue-500',
        current: true,
    },
    {
        title: 'IT Support Analyst (NYSC)',
        company: 'National Youth Service Corps',
        period: 'March 2025 – December 2025',
        location: 'Nigeria',
        type: 'NYSC Service',
        description: [
            'Served as an IT Support Analyst during the National Youth Service Corps program.',
            'Troubleshot technical issues across hardware and software systems.',
            'Provided end-user support and training for office technology tools.',
            'Contributed to IT operations and helped maintain network infrastructure.',
        ],
        color: 'from-emerald-500 to-teal-500',
        current: false,
    },
    {
        title: 'IT Intern',
        company: 'Pan-Atlantic University',
        period: 'April 2023 – October 2023',
        location: 'Lagos, Nigeria',
        type: 'Internship',
        description: [
            'Assisted IT staff with day-to-day technical support operations and service desk management.',
            'Resolved user technical issues including software installation and network connectivity.',
            'Supported campus-wide IT operations and infrastructure maintenance.',
            'Gained hands-on experience with enterprise IT systems and best practices.',
        ],
        color: 'from-violet-500 to-purple-500',
        current: false,
    },
];

export default function Experience() {
    const { isDark } = useTheme();

    return (
        <section id="experience" className={`section-padding ${isDark ? 'bg-dark-surface' : 'bg-light-surface'}`}>
            <div className="max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        My journey
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        Work <span className="gradient-text">Experience</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full" />
                </motion.div>

                <div className="relative">
                    {/* Timeline line */}
                    <div className={`absolute left-7 md:left-8 top-0 bottom-0 w-px ${isDark ? 'bg-gradient-to-b from-primary/50 via-accent/30 to-transparent' : 'bg-gradient-to-b from-primary/30 via-accent/20 to-transparent'
                        }`} />

                    <div className="space-y-8">
                        {experiences.map((exp, i) => (
                            <motion.div
                                key={exp.title + exp.company}
                                initial={{ opacity: 0, x: -20 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true, margin: '-80px' }}
                                transition={{ duration: 0.5, delay: i * 0.15 }}
                                className="relative pl-16 md:pl-20"
                            >
                                {/* Timeline dot */}
                                <div className={`absolute left-5 md:left-6 w-5 h-5 rounded-full bg-gradient-to-br ${exp.color} border-4 z-10`}
                                    style={{ borderColor: isDark ? '#030712' : '#f8fafc' }}
                                />
                                {exp.current && (
                                    <div className={`absolute left-5 md:left-6 w-5 h-5 rounded-full bg-gradient-to-br ${exp.color} z-5`}
                                        style={{ animation: 'pulse-ring 2s ease-in-out infinite' }}
                                    />
                                )}

                                <div className="glass rounded-2xl p-6 glow glow-hover transition-all duration-300 relative overflow-hidden group">
                                    <div className={`absolute top-0 left-0 w-1 h-full bg-gradient-to-b ${exp.color} opacity-60 group-hover:opacity-100 transition-opacity`} />

                                    <div className="flex flex-wrap items-center gap-2 mb-3">
                                        <h3 className="text-lg font-bold">{exp.title}</h3>
                                        {exp.current && (
                                            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                                Current
                                            </span>
                                        )}
                                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${isDark ? 'bg-white/5 text-dark-muted' : 'bg-black/5 text-light-muted'
                                            }`}>
                                            {exp.type}
                                        </span>
                                    </div>

                                    <p className={`text-sm font-semibold mb-2 ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                                        {exp.company}
                                    </p>

                                    <div className={`flex flex-wrap gap-4 text-xs mb-4 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                        <span className="flex items-center gap-1.5">
                                            <HiCalendar className="text-sm" /> {exp.period}
                                        </span>
                                        <span className="flex items-center gap-1.5">
                                            <HiLocationMarker className="text-sm" /> {exp.location}
                                        </span>
                                    </div>

                                    <ul className="space-y-2">
                                        {exp.description.map((item, j) => (
                                            <li key={j} className={`text-sm flex items-start gap-2.5 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                                <span className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 bg-gradient-to-r ${exp.color}`} />
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
