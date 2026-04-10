import { motion } from 'framer-motion';
import {
    SiHtml5,
    SiCss,
    SiJavascript,
    SiReact,
    SiTailwindcss,
    SiGit,
    SiGithub,
} from 'react-icons/si';
import { HiCloud, HiCloudUpload, HiDesktopComputer, HiCog, HiSupport, HiShieldCheck } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

const skillCategories = [
    {
        title: 'Cloud Skills',
        color: 'from-cyan-500 to-blue-500',
        skills: [
            { name: 'Microsoft Azure', icon: <HiCloudUpload className="text-lg" /> },
            { name: 'Cloud Fundamentals', icon: <HiCloud className="text-lg" /> },
            { name: 'CI/CD Pipelines', icon: <HiShieldCheck className="text-lg" /> },
            { name: 'Infrastructure Design', icon: <HiCog className="text-lg" /> },
        ],
    },
    {
        title: 'IT Support',
        color: 'from-violet-500 to-purple-500',
        skills: [
            { name: 'Troubleshooting', icon: <HiDesktopComputer className="text-lg" /> },
            { name: 'Hardware Support', icon: <HiCog className="text-lg" /> },
            { name: 'System Maintenance', icon: <HiSupport className="text-lg" /> },
            { name: 'User Support', icon: <HiDesktopComputer className="text-lg" /> },
        ],
    },
    {
        title: 'Web Development',
        color: 'from-emerald-500 to-teal-500',
        skills: [
            { name: 'HTML5', icon: <SiHtml5 className="text-lg" /> },
            { name: 'CSS3', icon: <SiCss className="text-lg" /> },
            { name: 'JavaScript', icon: <SiJavascript className="text-lg" /> },
            { name: 'React', icon: <SiReact className="text-lg" /> },
            { name: 'Tailwind CSS', icon: <SiTailwindcss className="text-lg" /> },
        ],
    },
    {
        title: 'Tools & Technologies',
        color: 'from-orange-500 to-amber-500',
        skills: [
            { name: 'Git', icon: <SiGit className="text-lg" /> },
            { name: 'GitHub', icon: <SiGithub className="text-lg" /> },
        ],
    },
];

export default function Skills() {
    const { isDark } = useTheme();

    return (
        <section id="skills" className={`section-padding ${isDark ? 'bg-dark-surface' : 'bg-light-surface'}`}>
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        What I work with
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        My <span className="gradient-text">Skills</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full mb-6" />
                    <p className={`max-w-xl mx-auto ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                        A versatile blend of cloud computing, IT support, and modern web development.
                    </p>
                </motion.div>

                <div className="grid md:grid-cols-2 gap-6">
                    {skillCategories.map((cat, catIdx) => (
                        <motion.div
                            key={cat.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: '-80px' }}
                            transition={{ duration: 0.5, delay: catIdx * 0.1 }}
                            className="glass rounded-2xl p-7 glow glow-hover transition-all duration-300 relative overflow-hidden group"
                        >
                            <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${cat.color} opacity-60 group-hover:opacity-100 transition-opacity`} />

                            <div className="flex items-center gap-3 mb-6">
                                <div className={`w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br ${cat.color} text-white text-sm font-bold`}>
                                    {cat.skills.length}
                                </div>
                                <h3 className="text-lg font-bold">{cat.title}</h3>
                            </div>

                            <div className="flex flex-wrap gap-3">
                                {cat.skills.map((skill, skillIdx) => (
                                    <motion.div
                                        key={skill.name}
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        whileInView={{ opacity: 1, scale: 1 }}
                                        viewport={{ once: true }}
                                        transition={{ duration: 0.3, delay: catIdx * 0.05 + skillIdx * 0.05 }}
                                        className={`flex items-center gap-2.5 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 hover:scale-105 cursor-default ${isDark
                                            ? 'bg-white/[0.03] text-dark-text border border-white/[0.06] hover:border-primary/30 hover:bg-white/[0.06]'
                                            : 'bg-white text-light-text border border-black/[0.06] hover:border-primary/30 hover:shadow-sm'
                                            }`}
                                    >
                                        <span className="text-primary">{skill.icon}</span>
                                        {skill.name}
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
