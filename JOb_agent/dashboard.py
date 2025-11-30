"""
Streamlit Dashboard for Job Application Tracker
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime, timedelta
from models.database import get_session, JobApplication, EmailLog
from sqlalchemy import func


# Page configuration
st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-applied { color: #2196F3; }
    .status-interview { color: #FF9800; }
    .status-offer { color: #4CAF50; }
    .status-rejected { color: #F44336; }
</style>
""", unsafe_allow_html=True)


def get_all_applications():
    """Fetch all applications from database"""
    session = get_session()
    try:
        apps = session.query(JobApplication).all()
        return [app.to_dict() for app in apps]
    finally:
        session.close()


def get_statistics():
    """Get statistics from database"""
    session = get_session()
    try:
        total = session.query(JobApplication).count()
        
        # Count by status
        status_counts = session.query(
            JobApplication.status,
            func.count(JobApplication.id)
        ).group_by(JobApplication.status).all()
        
        # Recent applications (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent = session.query(JobApplication).filter(
            JobApplication.last_updated >= week_ago
        ).count()
        
        # Total emails processed
        total_emails = session.query(EmailLog).count()
        job_emails = session.query(EmailLog).filter_by(is_job_related=1).count()
        
        return {
            'total': total,
            'status_counts': dict(status_counts),
            'recent': recent,
            'total_emails': total_emails,
            'job_emails': job_emails,
        }
    finally:
        session.close()


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<div class="main-header">💼 Job Application Tracker Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["Overview", "Applications", "Analytics", "Settings"]
    )
    
    # Get data
    stats = get_statistics()
    applications = get_all_applications()
    
    if page == "Overview":
        show_overview(stats, applications)
    elif page == "Applications":
        show_applications(applications)
    elif page == "Analytics":
        show_analytics(applications, stats)
    elif page == "Settings":
        show_settings()


def show_overview(stats, applications):
    """Show overview page"""
    st.header("📈 Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Applications",
            value=stats['total'],
            delta=f"+{stats['recent']} this week"
        )
    
    with col2:
        st.metric(
            label="Emails Processed",
            value=stats['total_emails'],
            delta=f"{stats['job_emails']} job-related"
        )
    
    with col3:
        interviews = stats['status_counts'].get('interview_scheduled', 0)
        st.metric(
            label="Interviews",
            value=interviews
        )
    
    with col4:
        offers = stats['status_counts'].get('offer_received', 0)
        st.metric(
            label="Offers",
            value=offers
        )
    
    st.markdown("---")
    
    # Status breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Applications by Status")
        if stats['status_counts']:
            df_status = pd.DataFrame(
                list(stats['status_counts'].items()),
                columns=['Status', 'Count']
            )
            fig = px.pie(
                df_status,
                values='Count',
                names='Status',
                title='Status Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No applications yet")
    
    with col2:
        st.subheader("📅 Recent Activity")
        if applications:
            df = pd.DataFrame(applications)
            df['last_updated'] = pd.to_datetime(df['last_updated'])
            df_recent = df.nlargest(10, 'last_updated')[['company_name', 'role_title', 'status', 'last_updated']]
            df_recent['last_updated'] = df_recent['last_updated'].dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df_recent, use_container_width=True, hide_index=True)
        else:
            st.info("No recent activity")


def show_applications(applications):
    """Show applications page"""
    st.header("📋 All Applications")
    
    if not applications:
        st.info("No applications found. Run the tracker to start collecting data!")
        return
    
    df = pd.DataFrame(applications)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    
    with col2:
        companies = ['All'] + sorted(df['company_name'].dropna().unique().tolist())
        company_filter = st.selectbox("Filter by Company", companies)
    
    with col3:
        search = st.text_input("Search", placeholder="Search role or company...")
    
    # Apply filters
    filtered_df = df[df['status'].isin(status_filter)]
    
    if company_filter != 'All':
        filtered_df = filtered_df[filtered_df['company_name'] == company_filter]
    
    if search:
        mask = (
            filtered_df['company_name'].str.contains(search, case=False, na=False) |
            filtered_df['role_title'].str.contains(search, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Display results
    st.write(f"Showing {len(filtered_df)} of {len(df)} applications")
    
    # Format dates
    if 'application_date' in filtered_df.columns:
        filtered_df['application_date'] = pd.to_datetime(filtered_df['application_date']).dt.strftime('%Y-%m-%d')
    if 'last_updated' in filtered_df.columns:
        filtered_df['last_updated'] = pd.to_datetime(filtered_df['last_updated']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Select columns to display
    display_cols = ['company_name', 'role_title', 'status', 'location', 'application_date', 'last_updated']
    display_cols = [col for col in display_cols if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
        hide_index=True
    )
    
    # Export button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"job_applications_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def show_analytics(applications, stats):
    """Show analytics page"""
    st.header("📊 Analytics")
    
    if not applications:
        st.info("No data available for analytics yet.")
        return
    
    df = pd.DataFrame(applications)
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    
    # Timeline
    st.subheader("📈 Application Timeline")
    df_timeline = df.groupby(df['last_updated'].dt.date).size().reset_index()
    df_timeline.columns = ['Date', 'Count']
    
    fig = px.line(
        df_timeline,
        x='Date',
        y='Count',
        title='Applications Over Time',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Company breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Top Companies")
        company_counts = df['company_name'].value_counts().head(10)
        fig = px.bar(
            x=company_counts.values,
            y=company_counts.index,
            orientation='h',
            title='Applications by Company',
            labels={'x': 'Count', 'y': 'Company'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📍 Locations")
        location_counts = df['location'].dropna().value_counts().head(10)
        if not location_counts.empty:
            fig = px.bar(
                x=location_counts.values,
                y=location_counts.index,
                orientation='h',
                title='Applications by Location',
                labels={'x': 'Count', 'y': 'Location'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No location data available")
    
    # Success metrics
    st.subheader("🎯 Success Metrics")
    
    total = len(df)
    interviews = len(df[df['status'] == 'interview_scheduled'])
    offers = len(df[df['status'] == 'offer_received'])
    rejected = len(df[df['status'] == 'rejected'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interview_rate = (interviews / total * 100) if total > 0 else 0
        st.metric("Interview Rate", f"{interview_rate:.1f}%")
    
    with col2:
        offer_rate = (offers / total * 100) if total > 0 else 0
        st.metric("Offer Rate", f"{offer_rate:.1f}%")
    
    with col3:
        rejection_rate = (rejected / total * 100) if total > 0 else 0
        st.metric("Rejection Rate", f"{rejection_rate:.1f}%")


def show_settings():
    """Show settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Configuration")
    st.info("Configuration is managed through the .env file. See .env.example for reference.")
    
    st.subheader("🗄️ Database")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    with col2:
        if st.button("📊 View Database Stats"):
            stats = get_statistics()
            st.json(stats)
    
    st.subheader("ℹ️ About")
    st.markdown("""
    **Job Application Email Tracker** is a multi-agent AI system that automatically 
    tracks and analyzes your job application emails.
    
    **Features:**
    - Automatic email monitoring
    - AI-powered classification
    - Data extraction and storage
    - Analytics and insights
    
    **Agents:**
    1. Email Monitor Agent
    2. Email Classifier Agent
    3. Data Extractor Agent
    4. Database Manager Agent
    5. Orchestrator Agent
    """)


if __name__ == "__main__":
    main()
