import { motion } from 'framer-motion';
import { HiCloud, HiSupport, HiCode, HiShieldCheck } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

const services = [
    {
        icon: <HiCloud className="text-3xl" />,
        title: 'Cloud Solutions',
        description: 'Designing and implementing scalable cloud architectures on Microsoft Azure with a focus on high availability and cost optimization.',
        color: 'from-cyan-500 to-blue-500',
    },
    {
        icon: <HiSupport className="text-3xl" />,
        title: 'IT Support',
        description: 'Comprehensive technical support including hardware repair, software troubleshooting, and network configuration for organizations.',
        color: 'from-violet-500 to-purple-500',
    },
    {
        icon: <HiCode className="text-3xl" />,
        title: 'Web Development',
        description: 'Building responsive, modern web applications using React, Tailwind CSS, JavaScript, and other modern technologies.',
        color: 'from-emerald-500 to-teal-500',
    },
    {
        icon: <HiShieldCheck className="text-3xl" />,
        title: 'DevOps & CI/CD',
        description: 'Automating deployment pipelines, managing containerized applications, and scaling infrastructure using modern DevOps tools.',
        color: 'from-orange-500 to-amber-500',
    },
];

export default function WhatIDo() {
    const { isDark } = useTheme();

    return (
        <section className={`section-padding ${isDark ? 'bg-dark-surface' : 'bg-light-surface'}`}>
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        Services
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        What I <span className="gradient-text">Do</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full mb-6" />
                    <p className={`max-w-xl mx-auto ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                        Combining cloud expertise with hands-on IT support and web development skills.
                    </p>
                </motion.div>

                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
                    {services.map((service, i) => (
                        <motion.div
                            key={service.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: '-80px' }}
                            transition={{ duration: 0.5, delay: i * 0.1 }}
                            className="glass rounded-2xl p-6 text-center glow glow-hover hover:scale-[1.03] transition-all duration-300 group relative overflow-hidden"
                        >
                            <div className={`absolute inset-0 bg-gradient-to-br ${service.color} opacity-0 group-hover:opacity-[0.03] transition-opacity duration-500`} />

                            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 bg-gradient-to-br ${service.color} text-white group-hover:scale-110 transition-transform duration-300`}>
                                {service.icon}
                            </div>
                            <h3 className="text-base font-bold mb-2">{service.title}</h3>
                            <p className={`text-sm leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                {service.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
