'use client';

import React, { useEffect, useState } from 'react';
import styles from './page.module.css';
import GlassCard from '@/components/ui/GlassCard';
import NeonButton from '@/components/ui/NeonButton';
import { ArrowRight, Clock, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';
import { api, DashboardStats } from '@/services/api';
import Link from 'next/link';

export default function Home() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);

  const loadStats = async () => {
    try {
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error(err);
      setError('Failed to load dashboard data. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await api.triggerSync();

      // Poll for status
      const interval = setInterval(async () => {
        try {
          const status = await api.getSyncStatus();
          if (!status.is_running) {
            clearInterval(interval);
            setSyncing(false);
            loadStats(); // Reload data when done
          }
        } catch (e) {
          console.error("Error polling sync status", e);
          clearInterval(interval);
          setSyncing(false);
        }
      }, 2000);

    } catch (err) {
      console.error(err);
      setSyncing(false);
    }
  };

  if (loading) {
    return (
      <div className="container flex-center" style={{ minHeight: '60vh' }}>
        <div className="text-gradient" style={{ fontSize: '1.5rem' }}>Loading Mission Control...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container flex-center" style={{ minHeight: '60vh', flexDirection: 'column', gap: 20 }}>
        <AlertCircle size={48} color="var(--accent)" />
        <div style={{ color: 'var(--accent)' }}>{error}</div>
        <NeonButton onClick={() => window.location.reload()}>Retry Connection</NeonButton>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Hero Section */}
      <section className={styles.hero}>
        <motion.h1
          className={styles.heroTitle}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Find Your Next <span className="text-gradient">Mission</span>
        </motion.h1>
        <motion.p
          className={styles.heroSubtitle}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          AI-powered job tracking and analysis to supercharge your career growth.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center' }}>
            <Link href="/jobs">
              <NeonButton icon={<ArrowRight size={20} />}>
                Get Started
              </NeonButton>
            </Link>
            <NeonButton
              variant="outline"
              icon={<RefreshCw size={20} className={syncing ? "animate-spin" : ""} />}
              onClick={handleSync}
              disabled={syncing}
            >
              {syncing ? 'Syncing...' : 'Sync Emails'}
            </NeonButton>
          </div>
        </motion.div>
      </section>

      {/* Stats Row */}
      <section className={styles.statsGrid}>
        <GlassCard>
          <div className={styles.statValue}>{stats?.total_applications || 0}</div>
          <div className={styles.statLabel}>Jobs Applied</div>
        </GlassCard>
        <GlassCard>
          <div className={styles.statValue}>{stats?.interviews || 0}</div>
          <div className={styles.statLabel}>Interviews</div>
        </GlassCard>
        <GlassCard>
          <div className={styles.statValue}>{stats?.offers || 0}</div>
          <div className={styles.statLabel}>Offers</div>
        </GlassCard>
      </section>

      {/* Recent Activity */}
      <section>
        <h2 className={styles.sectionTitle}>
          <Clock size={28} className="text-gradient" />
          Recent Activity
        </h2>
        {stats?.recent_activity && stats.recent_activity.length > 0 ? (
          <GlassCard className={styles.activityList}>
            {stats.recent_activity.map((app) => (
              <div key={app.id} className={styles.activityItem}>
                <div>
                  <h3 style={{ fontWeight: 600, marginBottom: 4 }}>{app.role_title}</h3>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    {app.company_name} • Updated {new Date(app.updated_at || app.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--primary)' }}>
                  <CheckCircle size={16} />
                  <span style={{ fontSize: '0.9rem', textTransform: 'capitalize' }}>{app.status.replace('_', ' ')}</span>
                </div>
              </div>
            ))}
          </GlassCard>
        ) : (
          <GlassCard>
            <div style={{ padding: 20, textAlign: 'center', color: 'var(--text-secondary)' }}>
              No recent activity. Start applying!
            </div>
          </GlassCard>
        )}
      </section>
    </div>
  );
}
