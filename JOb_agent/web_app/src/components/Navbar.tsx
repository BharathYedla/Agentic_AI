"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Briefcase, LayoutDashboard, FileText, User } from "lucide-react";
import styles from "./Navbar.module.css";
import clsx from "clsx";

const navItems = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Jobs", href: "/jobs", icon: Briefcase },
    { name: "Applications", href: "/applications", icon: FileText },
    { name: "Profile", href: "/profile", icon: User },
];

export default function Navbar() {
    const pathname = usePathname();

    return (
        <nav className={styles.navbar}>
            <div className={styles.container}>
                <Link href="/" className={styles.logo}>
                    Job<span className={styles.logoHighlight}>Tracker</span>
                </Link>

                <div className={styles.links}>
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;
                        const Icon = item.icon;

                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={clsx(styles.link, isActive && styles.active)}
                            >
                                {isActive && (
                                    <motion.div
                                        layoutId="nav-pill"
                                        className={styles.activeBackground}
                                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                    />
                                )}
                                <span className={styles.linkContent}>
                                    <Icon size={18} />
                                    <span className={styles.linkText}>{item.name}</span>
                                </span>
                            </Link>
                        );
                    })}
                </div>
            </div>
        </nav>
    );
}
