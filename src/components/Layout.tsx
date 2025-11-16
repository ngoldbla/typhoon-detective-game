import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useLanguage } from '@/contexts/LanguageContext';
import { useGame } from '@/contexts/GameContext';
import {
    FaHome,
    FaClipboardList,
    FaCog,
    FaQuestionCircle,
    FaCogs
} from 'react-icons/fa';
import ProgressBar from './ProgressBar';

// Define type for navigation items
interface NavItem {
    href: string;
    icon: React.ReactNode;
    label: string;
    isExternal?: boolean;
}

export default function Layout({ children, title }: { children: React.ReactNode, title?: string }) {
    const pathname = usePathname();
    const { t } = useLanguage();
    const { state } = useGame();
    const { gameState } = state;
    const [progress, setProgress] = useState(0);
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 10);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    useEffect(() => {
        if (gameState.activeCase) {
            setProgress(gameState.gameProgress);
        } else {
            setProgress(0);
        }
    }, [gameState]);

    // Create nav items with useMemo to prevent unnecessary re-renders
    const navItems = useMemo<NavItem[]>(() => {
        const items: NavItem[] = [
            { href: '/', icon: <FaHome className="text-lg" />, label: t('nav.home') },
            { href: '/cases', icon: <FaClipboardList className="text-lg" />, label: t('nav.cases') },
            { href: '/how-to-play', icon: <FaQuestionCircle className="text-lg" />, label: t('nav.howToPlay') || 'How to Play' },
            { href: '/how-it-works', icon: <FaCogs className="text-lg" />, label: t('nav.howItWorks') || 'How It Works' },
            { href: '/settings', icon: <FaCog className="text-lg" />, label: t('nav.settings') }
        ];

        return items;
    }, [t]); // Only recalculate when language (affects t) changes

    // Create a safe wrapper for the Link component to handle any potential errors
    const SafeLink = ({ item }: { item: NavItem }) => {
        try {
            // For external links (like GitHub)
            if (item.isExternal) {
                return (
                    <a
                        href={item.href}
                        className={`flex flex-col items-center p-2 rounded-lg transition-all text-surface-400 hover:text-[var(--borderlands-orange)]`}
                        data-gtm-id={item.href.includes('github') ? 'nav-github-source' : `nav-link-external`}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <div className="mb-1 text-surface-400">
                            {item.icon}
                        </div>
                        <span className="text-xs font-bold comic-text">{item.label}</span>
                    </a>
                );
            }

            // For internal navigation links
            return (
                <Link
                    href={item.href}
                    className={`flex flex-col items-center p-2 rounded-lg transition-all ${pathname === item.href
                        ? 'text-[var(--borderlands-yellow)]'
                        : 'text-surface-400 hover:text-[var(--borderlands-orange)]'
                        }`}
                    data-gtm-id={`nav-${item.href.replace(/\//g, '') || 'home'}`}
                >
                    <div className={`mb-1 ${pathname === item.href
                        ? 'scale-125 text-[var(--borderlands-yellow)]'
                        : 'text-surface-400'
                        }`}>
                        {item.icon}
                    </div>
                    <span className="text-xs font-bold comic-text">{item.label}</span>
                    {pathname === item.href && (
                        <div className="h-1 w-6 bg-[var(--borderlands-orange)] rounded-full mt-1"></div>
                    )}
                </Link>
            );
        } catch (error) {
            console.error('Error rendering navigation link:', error);
            // Fallback rendering in case of error
            return (
                <span className="flex flex-col items-center p-2 text-surface-400">
                    <div className="mb-1">{item.icon}</div>
                    <span className="text-xs font-bold comic-text">{item.label}</span>
                </span>
            );
        }
    };

    return (
        <div className="flex flex-col min-h-screen bg-grid bg-surface-900">
            <header
                className={`sticky top-0 z-50 borderlands-panel transition-all duration-300 ${isScrolled ? 'bg-surface-900 shadow-md' : 'bg-surface-900'}`}
                data-gtm-id="main-header"
            >
                <div className="container mx-auto px-4 py-3 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <Link href="/" className="text-3xl font-black comic-text text-yellow-300 transform -rotate-1 drop-shadow-[0_1px_3px_rgba(0,0,0,0.8)]" data-gtm-id="header-logo">
                            {t('app.title')}
                        </Link>
                        <span className="text-xs font-bold borderlands-panel px-2 py-1 bg-surface-800 rotate-2">
                            {t('app.subtitle')}
                        </span>
                        <span className="text-xs font-bold borderlands-panel px-2 py-1 bg-red-600 -rotate-3 animate-pulse">
                            DEMO
                        </span>
                    </div>
                </div>

                {gameState.activeCase && (
                    <div className="container mx-auto px-4 pb-2">
                        <div className="flex items-center justify-between">
                            <div className="w-full max-w-3xl mx-auto">
                                <ProgressBar
                                    progress={progress}
                                    showText={true}
                                    showSteps={true}
                                    size="md"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </header>

            <main className="flex-grow container mx-auto px-4 py-6" data-gtm-id="main-content">
                <div className="borderlands-panel p-6">
                    {children}
                </div>
            </main>

            <nav className="sticky bottom-0 borderlands-panel bg-surface-900 py-2 px-4" data-gtm-id="bottom-nav">
                <div className="container mx-auto flex justify-between items-center max-w-md">
                    {navItems.map((item) => (
                        <SafeLink key={item.href} item={item} />
                    ))}
                </div>
            </nav>
        </div>
    );
}