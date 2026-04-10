import { motion } from 'framer-motion';
import { HiBadgeCheck, HiCloudUpload, HiExternalLink } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

export default function Certifications() {
    const { isDark } = useTheme();

    return (
        <section id="certifications" className="section-padding">
            <div className="max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-16"
                >
                    <span className={`text-sm font-semibold tracking-wider uppercase ${isDark ? 'text-primary' : 'text-primary-dark'}`}>
                        Credentials
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold mt-3 mb-5">
                        My <span className="gradient-text">Certifications</span>
                    </h2>
                    <div className="w-20 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full" />
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-80px' }}
                    transition={{ duration: 0.5 }}
                    className="glass rounded-2xl overflow-hidden glow glow-hover max-w-xl mx-auto group transition-all duration-300"
                >
                    {/* Azure gradient header */}
                    <div className="h-3 bg-gradient-to-r from-[#0078d4] via-[#00bcf2] to-[#0078d4]" />

                    <div className="p-8 md:p-10">
                        <div className="flex flex-col sm:flex-row items-center gap-6">
                            <div className={`w-20 h-20 rounded-2xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br from-[#0078d4] to-[#00bcf2] text-white`}>
                                <HiCloudUpload className="text-4xl" />
                            </div>
                            <div className="text-center sm:text-left flex-1">
                                <div className="flex items-center justify-center sm:justify-start gap-2 mb-2">
                                    <h3 className="text-xl font-bold">Azure Fundamentals</h3>
                                    <HiBadgeCheck className="text-[#0078d4] text-xl" />
                                </div>
                                <p className="text-sm font-semibold text-[#0078d4] mb-2">
                                    Microsoft Certified: AZ-900
                                </p>
                                <p className={`text-sm leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                                    Demonstrates foundational knowledge of cloud concepts, core Azure services,
                                    privacy, compliance, pricing, and support.
                                </p>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Future certifications teaser */}
                <motion.p
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className={`text-center text-sm mt-8 ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}
                >
                    🚀 Currently pursuing more cloud and DevOps certifications
                </motion.p>
            </div>
        </section>
    );
}
