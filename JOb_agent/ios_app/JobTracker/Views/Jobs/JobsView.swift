import SwiftUI

struct JobsView: View {
    @StateObject private var jobService = ExternalJobService()
    @State private var searchText = "iOS Developer"
    
    var body: some View {
        NavigationView {
            ZStack {
                DesignSystem.Colors.background.ignoresSafeArea()
                
                VStack(spacing: 0) {
                    // Search Bar
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(.gray)
                        TextField("Search jobs...", text: $searchText)
                            .onSubmit {
                                jobService.fetchJobs(keywords: searchText)
                            }
                        
                        if !searchText.isEmpty {
                            Button(action: { searchText = "" }) {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundColor(.gray)
                            }
                        }
                    }
                    .padding()
                    .background(DesignSystem.Colors.surface)
                    .cornerRadius(10)
                    .padding()
                    
                    if jobService.isLoading {
                        ProgressView()
                            .scaleEffect(1.5)
                            .frame(maxHeight: .infinity)
                    } else if let error = jobService.errorMessage {
                        VStack {
                            Image(systemName: "exclamationmark.triangle")
                                .font(.largeTitle)
                                .foregroundColor(.orange)
                            Text(error)
                                .padding()
                            Button("Retry") {
                                jobService.fetchJobs(keywords: searchText)
                            }
                            .primaryButton()
                        }
                        .frame(maxHeight: .infinity)
                    } else if jobService.jobs.isEmpty {
                        VStack {
                            Image(systemName: "briefcase")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)
                            Text("No jobs found")
                                .font(DesignSystem.Typography.headline)
                                .padding(.top)
                        }
                        .frame(maxHeight: .infinity)
                    } else {
                        ScrollView {
                            LazyVStack(spacing: 16) {
                                ForEach(jobService.jobs) { job in
                                    JobCard(job: job)
                                }
                            }
                            .padding()
                        }
                    }
                }
            }
            .navigationTitle("Jobs")
            .onAppear {
                if jobService.jobs.isEmpty {
                    jobService.fetchJobs()
                }
            }
        }
    }
}

struct JobCard: View {
    let job: JobRecommendation
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                if let logoURL = job.companyLogoURL, let url = URL(string: logoURL) {
                    AsyncImage(url: url) { image in
                        image.resizable()
                    } placeholder: {
                        Color.gray.opacity(0.3)
                    }
                    .frame(width: 50, height: 50)
                    .cornerRadius(8)
                } else {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                        .frame(width: 50, height: 50)
                        .cornerRadius(8)
                        .overlay(Text(job.company.prefix(1)).bold())
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    Text(job.title)
                        .font(DesignSystem.Typography.headline)
                        .foregroundColor(DesignSystem.Colors.text)
                    
                    Text(job.company)
                        .font(DesignSystem.Typography.body)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                Text("\(Int(job.matchScore * 100))% Match")
                    .font(.caption)
                    .padding(6)
                    .background(Color.green.opacity(0.1))
                    .foregroundColor(.green)
                    .cornerRadius(4)
            }
            
            HStack {
                Label(job.location, systemImage: "mappin.circle")
                Spacer()
                if let salary = job.salary {
                    Label(salary.formatted, systemImage: "dollarsign.circle")
                }
            }
            .font(.caption)
            .foregroundColor(.secondary)
            
            HStack {
                Button(action: {}) {
                    Label("Save", systemImage: "bookmark")
                }
                .buttonStyle(.bordered)
                
                Spacer()
                
                if let urlStr = job.applicationURL, let url = URL(string: urlStr) {
                    Link(destination: url) {
                        Text("Apply Now")
                            .bold()
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 8)
                            .background(DesignSystem.Colors.primary)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                }
            }
        }
        .padding()
        .background(DesignSystem.Colors.surface)
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}
