//
//  JobsView.swift
//  JobTracker
//
//  Job recommendations view with real-time LinkedIn/Google jobs and semantic search
//

import SwiftUI

struct JobsView: View {
    @StateObject private var viewModel = JobsViewModel()
    @State private var searchText = ""
    @State private var showingFilters = false
    @State private var showingResumeUpload = false
    @State private var selectedJob: JobRecommendation?
    
    var body: some View {
        NavigationView {
            ZStack {
                ScrollView {
                    VStack(spacing: 24) {
                        // Resume Status Banner
                        if viewModel.hasResume {
                            ResumeStatusBanner(
                                resumeName: viewModel.resume?.fileName ?? "Resume",
                                matchCount: viewModel.jobs.count,
                                onReupload: { showingResumeUpload = true }
                            )
                        } else {
                            ResumeUploadPrompt(
                                onUpload: { showingResumeUpload = true }
                            )
                        }
                        
                        // Job Source Selector
                        JobSourceSelector(
                            selectedSource: $viewModel.selectedSource,
                            onSourceChanged: {
                                Task {
                                    await viewModel.loadJobs()
                                }
                            }
                        )
                        
                        // Jobs List
                        if viewModel.isLoading && viewModel.jobs.isEmpty {
                            LoadingJobsView()
                        } else if viewModel.jobs.isEmpty {
                            EmptyStateView(
                                icon: "briefcase",
                                title: "No Jobs Found",
                                description: viewModel.hasResume
                                    ? "Try adjusting your search criteria"
                                    : "Upload your resume to get personalized recommendations",
                                actionTitle: viewModel.hasResume ? nil : "Upload Resume",
                                action: viewModel.hasResume ? nil : { showingResumeUpload = true }
                            )
                            .padding(.top, 40)
                        } else {
                            LazyVStack(spacing: 16) {
                                ForEach(filteredJobs) { job in
                                    JobCard(
                                        job: job,
                                        onTap: { selectedJob = job },
                                        onSave: {
                                            Task {
                                                await viewModel.toggleSaveJob(job)
                                            }
                                        },
                                        onApply: {
                                            if let url = URL(string: job.applicationUrl) {
                                                UIApplication.shared.open(url)
                                            }
                                        }
                                    )
                                }
                                
                                // Load more indicator
                                if viewModel.hasMore {
                                    ProgressView()
                                        .padding()
                                        .onAppear {
                                            Task {
                                                await viewModel.loadMoreJobs()
                                            }
                                        }
                                }
                            }
                        }
                    }
                    .padding()
                }
                .refreshable {
                    await viewModel.refresh()
                }
            }
            .navigationTitle("Jobs for You")
            .searchable(text: $searchText, prompt: "Search jobs")
            .onChange(of: searchText) { newValue in
                viewModel.searchQuery = newValue
                Task {
                    await viewModel.searchJobs()
                }
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingFilters = true }) {
                        Image(systemName: "slider.horizontal.3")
                            .font(.title3)
                            .foregroundColor(.blue)
                    }
                }
            }
            .sheet(isPresented: $showingFilters) {
                JobFiltersView(viewModel: viewModel)
            }
            .sheet(isPresented: $showingResumeUpload) {
                ResumeUploadView(viewModel: viewModel)
            }
            .sheet(item: $selectedJob) { job in
                JobDetailView(job: job, viewModel: viewModel)
            }
            .onAppear {
                Task {
                    await viewModel.initialize()
                }
            }
        }
    }
    
    private var filteredJobs: [JobRecommendation] {
        if searchText.isEmpty {
            return viewModel.jobs
        }
        return viewModel.jobs.filter { job in
            job.title.localizedCaseInsensitiveContains(searchText) ||
            job.company.localizedCaseInsensitiveContains(searchText) ||
            job.description.localizedCaseInsensitiveContains(searchText)
        }
    }
}

// MARK: - Resume Status Banner

struct ResumeStatusBanner: View {
    let resumeName: String
    let matchCount: Int
    let onReupload: () -> Void
    
    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                Circle()
                    .fill(Color.green.opacity(0.1))
                    .frame(width: 50, height: 50)
                
                Image(systemName: "doc.text.fill")
                    .font(.title3)
                    .foregroundColor(.green)
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text("Resume Active")
                    .font(.headline)
                    .foregroundColor(.primary)
                
                Text("\(matchCount) jobs matched to your profile")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Button(action: onReupload) {
                Image(systemName: "arrow.triangle.2.circlepath")
                    .font(.title3)
                    .foregroundColor(.blue)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.green.opacity(0.05))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(Color.green.opacity(0.2), lineWidth: 1)
                )
        )
    }
}

// MARK: - Resume Upload Prompt

struct ResumeUploadPrompt: View {
    let onUpload: () -> Void
    
    var body: some View {
        VStack(spacing: 16) {
            HStack(spacing: 16) {
                ZStack {
                    Circle()
                        .fill(Color.blue.opacity(0.1))
                        .frame(width: 50, height: 50)
                    
                    Image(systemName: "doc.badge.plus")
                        .font(.title3)
                        .foregroundColor(.blue)
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    Text("Upload Your Resume")
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    Text("Get AI-powered job recommendations")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Button(action: onUpload) {
                    Text("Upload")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 10)
                        .background(Color.blue)
                        .cornerRadius(10)
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color.blue.opacity(0.05))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(Color.blue.opacity(0.2), lineWidth: 1)
                )
        )
    }
}

// MARK: - Job Source Selector

struct JobSourceSelector: View {
    @Binding var selectedSource: JobSource
    let onSourceChanged: () -> Void
    
    let sources: [JobSource] = [.aggregated, .linkedin, .google, .indeed]
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(sources, id: \.self) { source in
                    Button(action: {
                        selectedSource = source
                        onSourceChanged()
                    }) {
                        HStack(spacing: 8) {
                            Image(systemName: source.icon)
                                .font(.caption)
                            
                            Text(source.displayName)
                                .font(.subheadline)
                                .fontWeight(.medium)
                        }
                        .foregroundColor(selectedSource == source ? .white : .primary)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(
                            Capsule()
                                .fill(selectedSource == source ? Color.blue : Color(.systemGray6))
                        )
                    }
                }
            }
        }
    }
}

// MARK: - Job Card

struct JobCard: View {
    let job: JobRecommendation
    let onTap: () -> Void
    let onSave: () -> Void
    let onApply: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            VStack(alignment: .leading, spacing: 16) {
                // Header with company logo and save button
                HStack(spacing: 12) {
                    // Company Logo
                    if let logoUrl = job.companyLogo, let url = URL(string: logoUrl) {
                        AsyncImage(url: url) { image in
                            image
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                        } placeholder: {
                            CompanyLogoPlaceholder(company: job.company)
                        }
                        .frame(width: 50, height: 50)
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                    } else {
                        CompanyLogoPlaceholder(company: job.company)
                    }
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text(job.company)
                            .font(.subheadline)
                            .fontWeight(.semibold)
                            .foregroundColor(.primary)
                        
                        HStack(spacing: 4) {
                            Image(systemName: job.locationType.icon)
                                .font(.caption2)
                            Text(job.locationType.displayName)
                                .font(.caption)
                        }
                        .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                    
                    // Save button
                    Button(action: onSave) {
                        Image(systemName: job.isSaved ? "bookmark.fill" : "bookmark")
                            .font(.title3)
                            .foregroundColor(job.isSaved ? .blue : .secondary)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
                
                // Job Title
                Text(job.title)
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)
                    .lineLimit(2)
                
                // Match Score (if available)
                if job.matchScore > 0 {
                    MatchScoreBadge(score: job.matchScore)
                }
                
                // Location and Salary
                HStack(spacing: 16) {
                    HStack(spacing: 6) {
                        Image(systemName: "location.fill")
                            .font(.caption)
                        Text(job.location)
                            .font(.subheadline)
                    }
                    .foregroundColor(.secondary)
                    
                    if let salary = job.salary {
                        HStack(spacing: 6) {
                            Image(systemName: "dollarsign.circle.fill")
                                .font(.caption)
                            Text(salary.displayString)
                                .font(.subheadline)
                        }
                        .foregroundColor(.green)
                    }
                }
                
                // Skills
                if !job.skills.isEmpty {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(job.skills.prefix(5), id: \.self) { skill in
                                Text(skill)
                                    .font(.caption)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.blue.opacity(0.1))
                                    .foregroundColor(.blue)
                                    .cornerRadius(8)
                            }
                        }
                    }
                }
                
                // Posted Date and Apply Button
                HStack {
                    Text(job.postedDate.timeAgoDisplay())
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Spacer()
                    
                    Button(action: onApply) {
                        HStack(spacing: 6) {
                            Text("Apply")
                                .font(.subheadline)
                                .fontWeight(.semibold)
                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                        }
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.blue)
                        .cornerRadius(10)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(Color(.systemBackground))
                    .shadow(color: Color.black.opacity(0.08), radius: 12, x: 0, y: 4)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - Company Logo Placeholder

struct CompanyLogoPlaceholder: View {
    let company: String
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 10)
                .fill(
                    LinearGradient(
                        colors: [.blue.opacity(0.6), .purple.opacity(0.6)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 50, height: 50)
            
            Text(company.prefix(1))
                .font(.title3)
                .fontWeight(.bold)
                .foregroundColor(.white)
        }
    }
}

// MARK: - Match Score Badge

struct MatchScoreBadge: View {
    let score: Double
    
    private var scoreColor: Color {
        if score >= 0.8 { return .green }
        if score >= 0.6 { return .orange }
        return .gray
    }
    
    private var scoreText: String {
        "\(Int(score * 100))% Match"
    }
    
    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: "sparkles")
                .font(.caption2)
            Text(scoreText)
                .font(.caption)
                .fontWeight(.semibold)
        }
        .foregroundColor(scoreColor)
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .background(scoreColor.opacity(0.15))
        .cornerRadius(8)
    }
}

// MARK: - Loading View

struct LoadingJobsView: View {
    var body: some View {
        VStack(spacing: 16) {
            ForEach(0..<3) { _ in
                JobCardSkeleton()
            }
        }
    }
}

struct JobCardSkeleton: View {
    @State private var isAnimating = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack(spacing: 12) {
                RoundedRectangle(cornerRadius: 10)
                    .fill(Color(.systemGray5))
                    .frame(width: 50, height: 50)
                
                VStack(alignment: .leading, spacing: 8) {
                    RoundedRectangle(cornerRadius: 4)
                        .fill(Color(.systemGray5))
                        .frame(width: 120, height: 12)
                    
                    RoundedRectangle(cornerRadius: 4)
                        .fill(Color(.systemGray5))
                        .frame(width: 80, height: 10)
                }
                
                Spacer()
            }
            
            RoundedRectangle(cornerRadius: 4)
                .fill(Color(.systemGray5))
                .frame(height: 20)
            
            RoundedRectangle(cornerRadius: 4)
                .fill(Color(.systemGray5))
                .frame(height: 16)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color(.systemBackground))
                .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
        )
        .opacity(isAnimating ? 0.5 : 1.0)
        .animation(.easeInOut(duration: 1.0).repeatForever(autoreverses: true), value: isAnimating)
        .onAppear {
            isAnimating = true
        }
    }
}

// MARK: - Date Extension

extension Date {
    func timeAgoDisplay() -> String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: self, relativeTo: Date())
    }
}

// MARK: - Preview

#Preview {
    JobsView()
        .environmentObject(AppState())
}
