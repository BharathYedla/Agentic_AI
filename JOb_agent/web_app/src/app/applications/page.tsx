'use client';

import React, { useEffect, useState } from 'react';
import styles from './page.module.css';
import JobCard from '@/components/JobCard';
import NeonButton from '@/components/ui/NeonButton';
import { Plus, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { api, Application } from '@/services/api';

const COLUMNS = [
    { id: 'applied', title: 'Applied', color: '#00E5FF' },
    { id: 'interview_scheduled', title: 'Interview', color: '#7C4DFF' },
    { id: 'offer_received', title: 'Offer', color: '#00FF94' },
];

export default function ApplicationsPage() {
    const [applications, setApplications] = useState<Application[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadApplications = async () => {
            try {
                const data = await api.getApplications();
                setApplications(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadApplications();
    }, []);

    if (loading) {
        return (
            <div className="container flex-center" style={{ height: '80vh' }}>
                <Loader2 className="animate-spin text-primary" size={48} />
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Applications Board</h1>
                <NeonButton icon={<Plus size={18} />}>Add Application</NeonButton>
            </div>

            <div className={styles.board}>
                {COLUMNS.map((column) => {
                    // Map status to column (handling variations)
                    const columnApps = applications.filter(app => {
                        if (column.id === 'interview_scheduled') {
                            return app.status.includes('interview');
                        }
                        if (column.id === 'offer_received') {
                            return app.status.includes('offer');
                        }
                        return app.status === column.id;
                    });

                    return (
                        <div key={column.id} className={styles.column}>
                            <div className={styles.columnHeader}>
                                <div className={styles.columnTitle}>
                                    <div style={{ width: 8, height: 8, borderRadius: '50%', background: column.color }} />
                                    {column.title}
                                </div>
                                <span className={styles.count}>{columnApps.length}</span>
                            </div>

                            <div className={styles.cardList}>
                                {columnApps.map((app, index) => (
                                    <motion.div
                                        key={app.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <JobCard job={{
                                            id: app.id.toString(),
                                            title: app.role_title,
                                            company: app.company_name,
                                            matchScore: 0 // TODO: Add match score to application model
                                        }} />
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
