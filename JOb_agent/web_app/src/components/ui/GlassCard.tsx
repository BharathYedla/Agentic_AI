import React from 'react';
import styles from './GlassCard.module.css';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface GlassCardProps {
    children: React.ReactNode;
    className?: string;
    hoverEffect?: boolean;
}

const GlassCard: React.FC<GlassCardProps> = ({ children, className, hoverEffect = true }) => {
    return (
        <motion.div
            className={clsx(styles.card, className)}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            whileHover={hoverEffect ? { scale: 1.02 } : {}}
        >
            <div className={styles.glow} />
            {children}
        </motion.div>
    );
};

export default GlassCard;
