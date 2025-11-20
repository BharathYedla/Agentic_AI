//
//  MainTabView.swift
//  JobTracker
//
//  Main tab bar interface
//

import SwiftUI

struct MainTabView: View {
    @State private var selectedTab = 0
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // Home Tab
            HomeView()
                .tabItem {
                    Label("Home", systemImage: selectedTab == 0 ? "house.fill" : "house")
                }
                .tag(0)
            
            // Applications Tab
            ApplicationsListView()
                .tabItem {
                    Label("Applications", systemImage: selectedTab == 1 ? "doc.text.fill" : "doc.text")
                }
                .tag(1)
            
            // Jobs Tab - NEW!
            JobsView()
                .tabItem {
                    Label("Jobs", systemImage: selectedTab == 2 ? "briefcase.fill" : "briefcase")
                }
                .tag(2)
            
            // Analytics Tab
            AnalyticsView()
                .tabItem {
                    Label("Analytics", systemImage: selectedTab == 3 ? "chart.bar.fill" : "chart.bar")
                }
                .tag(3)
            
            // Profile Tab
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: selectedTab == 4 ? "person.fill" : "person")
                }
                .tag(4)
        }
        .accentColor(.blue)
        .onChange(of: selectedTab) { newValue in
            // Haptic feedback on tab change
            let impact = UIImpactFeedbackGenerator(style: .light)
            impact.impactOccurred()
        }
    }
}

// MARK: - Home View

struct HomeView: View {
    @StateObject private var viewModel = HomeViewModel()
    @State private var showingAddApplication = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Header with greeting
                    HeaderView()
                    
                    // Quick stats
                    QuickStatsView(stats: viewModel.stats)
                    
                    // Recent activity
                    RecentActivityView(applications: viewModel.recentApplications)
                    
                    // Upcoming interviews
                    if !viewModel.upcomingInterviews.isEmpty {
                        UpcomingInterviewsView(interviews: viewModel.upcomingInterviews)
                    }
                    
                    // Action items
                    ActionItemsView(items: viewModel.actionItems)
                }
                .padding(.horizontal)
                .padding(.top, 8)
            }
            .navigationTitle("Home")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddApplication = true }) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                            .foregroundColor(.blue)
                    }
                }
            }
            .refreshable {
                await viewModel.refresh()
            }
        }
        .sheet(isPresented: $showingAddApplication) {
            AddApplicationView()
        }
        .onAppear {
            Task {
                await viewModel.loadData()
            }
        }
    }
}

// MARK: - Header View

struct HeaderView: View {
    @State private var currentHour = Calendar.current.component(.hour, from: Date())
    
    var greeting: String {
        switch currentHour {
        case 0..<12:
            return "Good Morning"
        case 12..<17:
            return "Good Afternoon"
        default:
            return "Good Evening"
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(greeting)
                .font(.title2)
                .fontWeight(.semibold)
                .foregroundColor(.primary)
            
            Text("Let's track your job search")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.vertical, 8)
    }
}

// MARK: - Quick Stats View

struct QuickStatsView: View {
    let stats: HomeStats
    
    var body: some View {
        VStack(spacing: 16) {
            Text("Overview")
                .font(.headline)
                .frame(maxWidth: .infinity, alignment: .leading)
            
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 16) {
                StatCard(
                    title: "Total Applications",
                    value: "\(stats.totalApplications)",
                    icon: "doc.text.fill",
                    color: .blue
                )
                
                StatCard(
                    title: "Interviews",
                    value: "\(stats.interviews)",
                    icon: "person.2.fill",
                    color: .orange
                )
                
                StatCard(
                    title: "Offers",
                    value: "\(stats.offers)",
                    icon: "star.fill",
                    color: .green
                )
                
                StatCard(
                    title: "This Week",
                    value: "\(stats.thisWeek)",
                    icon: "calendar.fill",
                    color: .purple
                )
            }
        }
    }
}

// MARK: - Stat Card

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                
                Spacer()
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text(value)
                    .font(.system(size: 28, weight: .bold))
                    .foregroundColor(.primary)
                
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color(.systemBackground))
                .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
        )
    }
}

// MARK: - Recent Activity View

struct RecentActivityView: View {
    let applications: [JobApplication]
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Text("Recent Activity")
                    .font(.headline)
                
                Spacer()
                
                NavigationLink(destination: ApplicationsListView()) {
                    Text("See All")
                        .font(.subheadline)
                        .foregroundColor(.blue)
                }
            }
            
            if applications.isEmpty {
                EmptyStateView(
                    icon: "doc.text",
                    title: "No applications yet",
                    description: "Start tracking your job applications"
                )
                .padding(.vertical, 32)
            } else {
                VStack(spacing: 12) {
                    ForEach(applications.prefix(5)) { application in
                        NavigationLink(destination: ApplicationDetailView(application: application)) {
                            ApplicationRowView(application: application)
                        }
                        .buttonStyle(PlainButtonStyle())
                    }
                }
            }
        }
    }
}

// MARK: - Application Row View

struct ApplicationRowView: View {
    let application: JobApplication
    
    var body: some View {
        HStack(spacing: 16) {
            // Company logo placeholder
            ZStack {
                Circle()
                    .fill(Color.blue.opacity(0.1))
                    .frame(width: 50, height: 50)
                
                Text(application.companyName.prefix(1))
                    .font(.title3)
                    .fontWeight(.semibold)
                    .foregroundColor(.blue)
            }
            
            // Application info
            VStack(alignment: .leading, spacing: 4) {
                Text(application.roleTitle)
                    .font(.headline)
                    .foregroundColor(.primary)
                    .lineLimit(1)
                
                Text(application.companyName)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
            }
            
            Spacer()
            
            // Status badge
            StatusBadge(status: application.status)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(.systemBackground))
                .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
        )
    }
}

// MARK: - Status Badge

struct StatusBadge: View {
    let status: ApplicationStatus
    
    var statusColor: Color {
        switch status {
        case .applied, .inProgress:
            return .blue
        case .interviewScheduled, .interviewCompleted:
            return .orange
        case .offerReceived, .offerAccepted:
            return .green
        case .rejected, .offerDeclined:
            return .red
        case .withdrawn:
            return .gray
        }
    }
    
    var statusText: String {
        switch status {
        case .applied:
            return "Applied"
        case .inProgress:
            return "In Progress"
        case .interviewScheduled:
            return "Interview"
        case .interviewCompleted:
            return "Interviewed"
        case .offerReceived:
            return "Offer"
        case .offerAccepted:
            return "Accepted"
        case .offerDeclined:
            return "Declined"
        case .rejected:
            return "Rejected"
        case .withdrawn:
            return "Withdrawn"
        }
    }
    
    var body: some View {
        Text(statusText)
            .font(.caption)
            .fontWeight(.medium)
            .foregroundColor(statusColor)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(
                Capsule()
                    .fill(statusColor.opacity(0.15))
            )
    }
}

// MARK: - Models

struct HomeStats {
    var totalApplications: Int = 0
    var interviews: Int = 0
    var offers: Int = 0
    var thisWeek: Int = 0
}

// MARK: - Preview

#Preview {
    MainTabView()
        .environmentObject(AppState())
}
