'use client';

import React from 'react';
import styles from './page.module.css';
import GlassCard from '@/components/ui/GlassCard';
import NeonButton from '@/components/ui/NeonButton';
import { User, Mail, Settings, Upload } from 'lucide-react';

export default function ProfilePage() {
    return (
        <div className={styles.container}>
            <GlassCard className={styles.header}>
                <div className={styles.avatar}>JD</div>
                <div className={styles.userInfo}>
                    <h1 className={styles.name}>John Doe</h1>
                    <p className={styles.role}>Senior Software Engineer</p>
                </div>
                <NeonButton variant="outline" icon={<Settings size={18} />}>
                    Settings
                </NeonButton>
            </GlassCard>

            <div className={styles.section}>
                <h2 className={styles.sectionTitle}>
                    <User size={20} className="text-primary" />
                    Personal Information
                </h2>
                <GlassCard>
                    <div style={{ display: 'grid', gap: 16 }}>
                        <div>
                            <label style={{ display: 'block', color: 'var(--text-secondary)', marginBottom: 4, fontSize: '0.9rem' }}>Email</label>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <Mail size={16} />
                                john.doe@example.com
                            </div>
                        </div>
                        <div>
                            <label style={{ display: 'block', color: 'var(--text-secondary)', marginBottom: 4, fontSize: '0.9rem' }}>Location</label>
                            <div>San Francisco, CA</div>
                        </div>
                    </div>
                </GlassCard>
            </div>

            <div className={styles.section}>
                <h2 className={styles.sectionTitle}>
                    <Upload size={20} className="text-primary" />
                    Resumes
                </h2>
                <GlassCard>
                    <div style={{ padding: 20, textAlign: 'center', border: '1px dashed var(--border-light)', borderRadius: 'var(--radius-sm)' }}>
                        <p style={{ marginBottom: 16, color: 'var(--text-secondary)' }}>Upload your resume to get AI-powered matching</p>
                        <NeonButton icon={<Upload size={18} />}>Upload Resume</NeonButton>
                    </div>
                </GlassCard>
            </div>
        </div>
    );
}
