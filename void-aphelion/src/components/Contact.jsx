import { useState } from 'react';
import { motion } from 'framer-motion';
import { HiMail, HiLocationMarker, HiPaperAirplane } from 'react-icons/hi';
import { SiGithub } from 'react-icons/si';
import { FaLinkedin } from 'react-icons/fa';
import { useTheme } from '../context/ThemeContext';

export default function Contact() {
    const { isDark } = useTheme();
    const [formData, setFormData] = useState({ name: '', email: '', message: '' });
    const [submitted, setSubmitted] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setSubmitted(true);
        setTimeout(() => setSubmitted(false), 4000);
        setFormData({ name: '', email: '', message: '' });
    };

    const contactInfo = [
        {
            icon: <HiMail className="text-xl" />,
            label: 'Email',
            value: 'oliverobiwulu158@gmail.com',
            href: 'mailto:oliverobiwulu158@gmail.com',
            color: 'from-cyan-500 to-blue-500',
        },
        {
            icon: <FaLinkedin className="text-lg" />,
            label: 'LinkedIn',
            value: 'Revilo',
            href: 'https://linkedin.com/in/oliver-obiwulu',
            color: 'from-blue-600 to-blue-700',
        },
        {
            icon: <SiGithub className="text-lg" />,
            label: 'GitHub',
            value: 'HarryClark20',
            href: 'https://github.com/HarryClark20',
            color: 'from-gray-600 to-gray-800',
        },
        {
            icon: <HiLocationMarker className="text-xl" />,
            label: 'Location',
            value: 'Lagos, Nigeria',
            href: null,
            color: 'from-rose-500 to-pink-500',
        },
    ];

    return (
        <section id="contact" className={`section-padding ${isDark ? 'bg-dark-surface' : 'bg-light-surface'}`}>
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        Let&apos;s talk
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        Get In <span className="gradient-text">Touch</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full mb-6" />
                    <p className={`max-w-xl mx-auto ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                        I&apos;m open to collaboration, job opportunities, and networking.
                        Let&apos;s build something great together!
                    </p>
                </motion.div>

                <div className="grid lg:grid-cols-5 gap-8">
                    {/* Contact Info */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, margin: '-80px' }}
                        transition={{ duration: 0.5 }}
                        className="lg:col-span-2 space-y-5"
                    >
                        <h3 className="text-xl font-bold mb-6">Contact Information</h3>
                        {contactInfo.map((info) => (
                            <div key={info.label} className="flex items-center gap-4 group">
                                <div className={`w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br ${info.color} text-white group-hover:scale-110 transition-transform duration-300`}>
                                    {info.icon}
                                </div>
                                <div>
                                    <p className={`text-xs uppercase tracking-wider font-medium ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                        {info.label}
                                    </p>
                                    {info.href ? (
                                        <a
                                            href={info.href}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-sm font-medium hover:text-primary transition-colors"
                                        >
                                            {info.value}
                                        </a>
                                    ) : (
                                        <p className="text-sm font-medium">{info.value}</p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </motion.div>

                    {/* Contact Form */}
                    <motion.form
                        initial={{ opacity: 0, x: 30 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true, margin: '-80px' }}
                        transition={{ duration: 0.5 }}
                        onSubmit={handleSubmit}
                        className="lg:col-span-3 glass rounded-2xl p-7 glow"
                    >
                        <div className="space-y-5">
                            <div className="grid sm:grid-cols-2 gap-5">
                                <div>
                                    <label htmlFor="name" className={`block text-sm font-medium mb-2 ${isDark ? 'text-dark-muted' : 'text-light-muted'
                                        }`}>
                                        Your Name
                                    </label>
                                    <input
                                        type="text"
                                        id="name"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        required
                                        className={`w-full px-4 py-3 rounded-xl text-sm outline-none transition-all duration-200 ${isDark
                                            ? 'bg-white/[0.03] border border-white/[0.08] text-dark-text focus:border-primary/50 focus:bg-white/[0.05]'
                                            : 'bg-white border border-black/[0.08] text-light-text focus:border-primary/50'
                                            }`}
                                        placeholder="Revilo"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="email" className={`block text-sm font-medium mb-2 ${isDark ? 'text-dark-muted' : 'text-light-muted'
                                        }`}>
                                        Your Email
                                    </label>
                                    <input
                                        type="email"
                                        id="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                        className={`w-full px-4 py-3 rounded-xl text-sm outline-none transition-all duration-200 ${isDark
                                            ? 'bg-white/[0.03] border border-white/[0.08] text-dark-text focus:border-primary/50 focus:bg-white/[0.05]'
                                            : 'bg-white border border-black/[0.08] text-light-text focus:border-primary/50'
                                            }`}
                                        placeholder="you@example.com"
                                    />
                                </div>
                            </div>
                            <div>
                                <label htmlFor="message" className={`block text-sm font-medium mb-2 ${isDark ? 'text-dark-muted' : 'text-light-muted'
                                    }`}>
                                    Your Message
                                </label>
                                <textarea
                                    id="message"
                                    name="message"
                                    rows={5}
                                    value={formData.message}
                                    onChange={handleChange}
                                    required
                                    className={`w-full px-4 py-3 rounded-xl text-sm outline-none resize-none transition-all duration-200 ${isDark
                                        ? 'bg-white/[0.03] border border-white/[0.08] text-dark-text focus:border-primary/50 focus:bg-white/[0.05]'
                                        : 'bg-white border border-black/[0.08] text-light-text focus:border-primary/50'
                                        }`}
                                    placeholder="Tell me about your project or opportunity..."
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={submitted}
                                className={`w-full py-4 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all duration-300 ${submitted
                                    ? 'bg-emerald-500 text-white'
                                    : 'bg-gradient-to-r from-primary to-accent text-white hover:shadow-lg hover:shadow-primary/30 hover:scale-[1.01]'
                                    }`}
                            >
                                {submitted ? (
                                    '✓ Message Sent Successfully!'
                                ) : (
                                    <>
                                        <HiPaperAirplane className="rotate-90" /> Send Message
                                    </>
                                )}
                            </button>
                        </div>
                    </motion.form>
                </div>
            </div>
        </section>
    );
}
