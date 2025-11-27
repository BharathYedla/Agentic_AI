const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface Job {
    id: string;
    title: string;
    company: string;
    location?: string;
    description?: string;
    url?: string;
    posted_at?: string;
    source: string;
    match_score?: number;
    company_logo?: string;
}

export interface Application {
    id: number;
    company_name: string;
    role_title: string;
    status: string;
    job_description?: string;
    location?: string;
    salary_min?: number;
    salary_max?: number;
    application_url?: string;
    company_website?: string;
    notes?: string;
    priority: number;
    created_at: string;
    updated_at: string;
}

export interface DashboardStats {
    total_applications: number;
    interviews: number;
    offers: number;
    response_rate: number;
    recent_activity: Application[];
}

/**
 * API service for interacting with the backend.
 */
export const api = {
    /**
     * Check if the backend is reachable.
     */
    async healthCheck(): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE_URL}/health`);
            return res.ok;
        } catch {
            return false;
        }
    },

    // --- Jobs ---

    /**
     * Search for jobs based on keywords and optional location.
     */
    async searchJobs(keywords: string, location?: string): Promise<{ jobs: Job[], total: number }> {
        const params = new URLSearchParams({ keywords });
        if (location) params.append('location', location);

        const res = await fetch(`${API_BASE_URL}/jobs/search?${params.toString()}`);
        if (!res.ok) throw new Error(`Failed to fetch jobs: ${res.statusText}`);
        return res.json();
    },

    // --- Applications ---

    /**
     * Fetch all tracked applications.
     */
    async getApplications(): Promise<Application[]> {
        const res = await fetch(`${API_BASE_URL}/applications/`);
        if (!res.ok) throw new Error(`Failed to fetch applications: ${res.statusText}`);
        return res.json();
    },

    /**
     * Create a new application record.
     */
    async createApplication(data: Partial<Application>): Promise<Application> {
        const res = await fetch(`${API_BASE_URL}/applications/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(`Failed to create application: ${res.statusText}`);
        return res.json();
    },

    /**
     * Update an existing application record.
     */
    async updateApplication(id: number, data: Partial<Application>): Promise<Application> {
        const res = await fetch(`${API_BASE_URL}/applications/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(`Failed to update application: ${res.statusText}`);
        return res.json();
    },

    // --- Analytics ---

    /**
     * Get dashboard statistics.
     */
    async getDashboardStats(): Promise<DashboardStats> {
        const res = await fetch(`${API_BASE_URL}/analytics/dashboard`);
        if (!res.ok) throw new Error(`Failed to fetch dashboard stats: ${res.statusText}`);
        return res.json();
    },

    // --- Sync ---

    /**
     * Trigger the email sync process.
     */
    async triggerSync(): Promise<{ message: string, status: string }> {
        const res = await fetch(`${API_BASE_URL}/sync/run`, {
            method: 'POST',
        });
        if (!res.ok) {
            if (res.status === 409) {
                throw new Error('Sync already in progress');
            }
            throw new Error(`Failed to trigger sync: ${res.statusText}`);
        }
        return res.json();
    },

    /**
     * Get the current status of the sync process.
     */
    async getSyncStatus(): Promise<{ is_running: boolean, last_status: string }> {
        const res = await fetch(`${API_BASE_URL}/sync/`);
        if (!res.ok) throw new Error(`Failed to get sync status: ${res.statusText}`);
        return res.json();
    }
};
