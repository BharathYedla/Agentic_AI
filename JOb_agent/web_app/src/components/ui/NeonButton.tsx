import React from 'react';
import styles from './NeonButton.module.css';
import { motion, HTMLMotionProps } from 'framer-motion';
import clsx from 'clsx';

interface NeonButtonProps extends HTMLMotionProps<"button"> {
    variant?: 'primary' | 'outline' | 'ghost';
    icon?: React.ReactNode;
    children: React.ReactNode;
}

const NeonButton: React.FC<NeonButtonProps> = ({ children, className, variant = 'primary', icon, ...props }) => {
    return (
        <motion.button
            className={clsx(styles.button, styles[variant], className)}
            whileTap={{ scale: 0.95 }}
            {...props}
        >
            {icon && <span className={styles.icon}>{icon}</span>}
            {children}
        </motion.button>
    );
};

export default NeonButton;
