const API_BASE_URL = 'http://localhost:8000/api/v1';

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

export const api = {
    // Jobs
    async searchJobs(keywords: string, location?: string): Promise<{ jobs: Job[], total: number }> {
        const params = new URLSearchParams({ keywords });
        if (location) params.append('location', location);

        const res = await fetch(`${API_BASE_URL}/jobs/search?${params.toString()}`);
        if (!res.ok) throw new Error('Failed to fetch jobs');
        return res.json();
    },

    // Applications
    async getApplications(): Promise<Application[]> {
        const res = await fetch(`${API_BASE_URL}/applications/`);
        if (!res.ok) throw new Error('Failed to fetch applications');
        return res.json();
    },

    async createApplication(data: Partial<Application>): Promise<Application> {
        const res = await fetch(`${API_BASE_URL}/applications/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to create application');
        return res.json();
    },

    async updateApplication(id: number, data: Partial<Application>): Promise<Application> {
        const res = await fetch(`${API_BASE_URL}/applications/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to update application');
        return res.json();
    },

    // Analytics
    async getDashboardStats(): Promise<DashboardStats> {
        const res = await fetch(`${API_BASE_URL}/analytics/dashboard`);
        if (!res.ok) throw new Error('Failed to fetch dashboard stats');
        return res.json();
    }
};
