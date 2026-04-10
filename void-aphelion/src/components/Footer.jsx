import { SiGithub } from 'react-icons/si';
import { FaLinkedin } from 'react-icons/fa';
import { HiMail, HiHeart } from 'react-icons/hi';
import { useTheme } from '../context/ThemeContext';

const quickLinks = [
    { name: 'Home', href: '#home' },
    { name: 'About', href: '#about' },
    { name: 'Skills', href: '#skills' },
    { name: 'Projects', href: '#projects' },
    { name: 'Experience', href: '#experience' },
    { name: 'Contact', href: '#contact' },
];

const socialLinks = [
    { icon: <SiGithub />, href: 'https://github.com/HarryClark20', label: 'GitHub' },
    { icon: <FaLinkedin />, href: 'https://linkedin.com/in/oliver-obiwulu', label: 'LinkedIn' },
    { icon: <HiMail />, href: 'mailto:oliverobiwulu158@gmail.com', label: 'Email' },
];

export default function Footer() {
    const { isDark } = useTheme();

    return (
        <footer className={`py-12 px-6 border-t ${isDark ? 'border-dark-border/50 bg-dark-bg' : 'border-light-border bg-light-card'
            }`}>
            <div className="max-w-6xl mx-auto">
                <div className="grid sm:grid-cols-3 gap-8 items-start">
                    {/* Brand */}
                    <div>
                        <a href="#home" className="text-xl font-bold gradient-text">
                            Oliver.dev
                        </a>
                        <p className={`text-sm mt-2 leading-relaxed ${isDark ? 'text-dark-muted' : 'text-light-muted'}`}>
                            Aspiring DevOps Engineer
                            <br />& IT Support Specialist
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="text-sm font-bold uppercase tracking-wider mb-4">Quick Links</h4>
                        <div className="grid grid-cols-2 gap-2">
                            {quickLinks.map((link) => (
                                <a
                                    key={link.name}
                                    href={link.href}
                                    className={`text-sm transition-colors hover:text-primary ${isDark ? 'text-dark-muted' : 'text-light-muted'
                                        }`}
                                >
                                    {link.name}
                                </a>
                            ))}
                        </div>
                    </div>

                    {/* Socials */}
                    <div>
                        <h4 className="text-sm font-bold uppercase tracking-wider mb-4">Connect</h4>
                        <div className="flex gap-3">
                            {socialLinks.map((link) => (
                                <a
                                    key={link.label}
                                    href={link.href}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className={`w-10 h-10 rounded-xl flex items-center justify-center text-lg transition-all duration-300 hover:text-white hover:bg-gradient-to-br hover:from-primary hover:to-accent hover:scale-110 hover:shadow-lg hover:shadow-primary/20 ${isDark ? 'bg-white/5 text-dark-muted' : 'bg-black/5 text-light-muted'
                                        }`}
                                    aria-label={link.label}
                                >
                                    {link.icon}
                                </a>
                            ))}
                        </div>
                    </div>
                </div>

                <div className={`text-center mt-10 pt-6 border-t text-sm ${isDark ? 'border-dark-border/30 text-dark-muted' : 'border-light-border text-light-muted'
                    }`}>
                    <p className="flex items-center justify-center gap-1">
                        © {new Date().getFullYear()} Revilo. Crafted with{' '}
                        <HiHeart className="text-red-500 animate-pulse" /> using React & Tailwind CSS
                    </p>
                </div>
            </div>
        </footer>
    );
}
