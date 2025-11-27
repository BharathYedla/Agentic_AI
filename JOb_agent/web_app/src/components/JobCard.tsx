import React from 'react';
import Image from 'next/image';
import styles from './JobCard.module.css';
import NeonButton from './ui/NeonButton';
import { motion } from 'framer-motion';

import { Job } from '@/services/api';

interface JobCardProps {
    job: Job;
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
    return (
        <motion.div
            className={styles.jobCard}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.01 }}
        >
            <div className={styles.companyLogo}>
                {job.company_logo ? (
                    <Image
                        src={job.company_logo}
                        alt={job.company}
                        fill
                        sizes="48px"
                        style={{ objectFit: 'cover', borderRadius: '50%' }}
                        unoptimized
                    />
                ) : (
                    job.company.substring(0, 2).toUpperCase()
                )}
            </div>
            <div className={styles.jobInfo}>
                <h3 className={styles.jobTitle}>{job.title}</h3>
                <p className={styles.companyName}>{job.company}</p>
            </div>

            <div className={styles.matchScore}>
                <div className={styles.scoreRing}>
                    {job.match_score || 0}%
                </div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Match</span>
            </div>

            <NeonButton variant="outline" style={{ padding: '8px 16px', fontSize: '0.9rem' }}>
                Apply
            </NeonButton>
        </motion.div>
    );
};

export default JobCard;
