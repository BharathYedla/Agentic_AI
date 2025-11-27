'use client';

import React, { useState, useEffect } from 'react';
import styles from './page.module.css';
import JobCard from '@/components/JobCard';
import GlassCard from '@/components/ui/GlassCard';
import { Search, Filter, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { api, Job } from '@/services/api';
import NeonButton from '@/components/ui/NeonButton';

export default function JobsPage() {
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState('iOS Developer');
    // Location feature pending implementation
    const [location] = useState('');

    const performSearch = async (query: string, loc: string) => {
        setLoading(true);
        try {
            const data = await api.searchJobs(query, loc);
            setJobs(data.jobs);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        performSearch(searchQuery, location);
    };

    useEffect(() => {
        performSearch('iOS Developer', '');
    }, []);

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1 className={styles.title}>Explore Opportunities</h1>
                <div className={styles.searchBar}>
                    <Search className={styles.searchIcon} size={20} />
                    <input
                        type="text"
                        placeholder="Search by role, company, or keywords..."
                        className={styles.searchInput}
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && searchJobs()}
                    />
                    <NeonButton
                        variant="ghost"
                        className={styles.searchButton}
                        onClick={searchJobs}
                        disabled={loading}
                    >
                        {loading ? <Loader2 className="animate-spin" /> : 'Search'}
                    </NeonButton>
                </div>
            </div>

            <div className={styles.content}>
                {/* Filters Sidebar */}
                <aside className={styles.filters}>
                    <GlassCard>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20 }}>
                            <Filter size={18} className="text-primary" />
                            <h2 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Filters</h2>
                        </div>

                        <div className={styles.filterSection}>
                            <h3 className={styles.filterTitle}>Job Type</h3>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Full-time
                            </div>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Contract
                            </div>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Remote
                            </div>
                        </div>

                        <div className={styles.filterSection}>
                            <h3 className={styles.filterTitle}>Experience</h3>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Entry Level
                            </div>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Senior
                            </div>
                            <div className={styles.filterOption}>
                                <div className={styles.checkbox} /> Lead
                            </div>
                        </div>
                    </GlassCard>
                </aside>

                {/* Job List */}
                <div className={styles.jobList}>
                    {loading ? (
                        <div className="flex-center" style={{ padding: 40 }}>
                            <Loader2 className="animate-spin text-primary" size={40} />
                        </div>
                    ) : jobs.length > 0 ? (
                        jobs.map((job, index) => (
                            <motion.div
                                key={job.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                <JobCard job={job} />
                            </motion.div>
                        ))
                    ) : (
                        <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-secondary)' }}>
                            No jobs found. Try adjusting your search.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
