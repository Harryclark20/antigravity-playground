import { motion } from 'framer-motion';
import { HiAcademicCap, HiBadgeCheck, HiLightningBolt, HiHeart } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

export default function About() {
    const { isDark } = useTheme();

    const highlights = [
        {
            icon: <HiAcademicCap className="text-2xl" />,
            title: 'Education',
            text: 'B.Sc Computer Science from Augustine University — Second Class Upper Division.',
            color: 'from-blue-500 to-cyan-400',
        },
        {
            icon: <HiBadgeCheck className="text-2xl" />,
            title: 'Certification',
            text: 'Microsoft Certified: Azure Fundamentals (AZ-900)',
            color: 'from-violet-500 to-purple-400',
        },
        {
            icon: <HiLightningBolt className="text-2xl" />,
            title: 'Career Goal',
            text: 'To become a DevOps Engineer focusing on CI/CD pipelines, automation, and scalable infrastructure.',
            color: 'from-amber-500 to-orange-400',
        },
        {
            icon: <HiHeart className="text-2xl" />,
            title: 'Passion',
            text: 'I love fixing laptops and mobile devices, and I enjoy building web applications that solve real problems.',
            color: 'from-pink-500 to-rose-400',
        },
    ];

    return (
        <section id="about" className="section-padding relative">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        Get to know me
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        About <span className="gradient-text">Me</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full mb-8" />
                    <p className={`max-w-2xl mx-auto text-base sm:text-lg leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                        I&apos;m <strong>Revilo</strong>, a passionate Computer Science graduate
                        currently working as an IT Support Specialist at Pan-Atlantic University.
                        With hands-on experience in troubleshooting hardware, software issues, and
                        cloud technologies, I&apos;m building my path toward becoming a DevOps
                        Engineer with a strong focus on automation and continuous delivery.
                    </p>
                </motion.div>

                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {highlights.map((card, i) => (
                        <motion.div
                            key={card.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: '-80px' }}
                            transition={{ duration: 0.5, delay: i * 0.1 }}
                            className="glass rounded-2xl p-6 glow glow-hover hover:scale-[1.03] transition-all duration-300 group relative overflow-hidden"
                        >
                            {/* Accent top border */}
                            <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${card.color} opacity-70 group-hover:opacity-100 transition-opacity`} />

                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 bg-gradient-to-br ${card.color} text-white`}>
                                {card.icon}
                            </div>
                            <h3 className="text-lg font-semibold mb-2">{card.title}</h3>
                            <p className={`text-sm leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                {card.text}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
