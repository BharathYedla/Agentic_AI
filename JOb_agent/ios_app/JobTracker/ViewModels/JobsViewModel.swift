//
//  JobsViewModel.swift
//  JobTracker
//
//  View model for job recommendations with real-time data
//

import Foundation
import Combine

@MainActor
class JobsViewModel: ObservableObject {
    @Published var jobs: [JobRecommendation] = []
    @Published var savedJobs: Set<String> = []
    @Published var resume: Resume?
    @Published var isLoading = false
    @Published var hasMore = true
    @Published var errorMessage: String?
    @Published var selectedSource: JobSource = .aggregated
    @Published var searchQuery: String = ""
    
    // Filters
    @Published var selectedLocation: String?
    @Published var selectedExperienceLevel: ExperienceLevel?
    @Published var selectedEmploymentType: EmploymentType?
    @Published var selectedLocationType: LocationType?
    @Published var minSalary: Int?
    
    private var currentOffset = 0
    private let pageSize = 20
    
    private let jobService = JobService.shared
    private let externalJobService = ExternalJobService.shared
    
    var hasResume: Bool {
        resume != nil
    }
    
    // MARK: - Initialization
    
    func initialize() async {
        await loadResume()
        await loadJobs()
    }
    
    // MARK: - Resume Management
    
    func loadResume() async {
        do {
            resume = try await jobService.getResume()
        } catch {
            // No resume uploaded yet
            resume = nil
        }
    }
    
    func uploadResume(fileData: Data, fileName: String) async throws {
        isLoading = true
        defer { isLoading = false }
        
        do {
            resume = try await jobService.uploadResume(fileData: fileData, fileName: fileName)
            
            // Reload jobs with resume-based recommendations
            await loadJobs()
        } catch {
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    func deleteResume() async {
        do {
            try await jobService.deleteResume()
            resume = nil
            await loadJobs()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
    
    // MARK: - Job Loading
    
    func loadJobs() async {
        isLoading = true
        currentOffset = 0
        errorMessage = nil
        
        defer { isLoading = false }
        
        do {
            let newJobs: [JobRecommendation]
            
            // Use appropriate service based on source
            switch selectedSource {
            case .linkedin:
                newJobs = try await externalJobService.fetchLinkedInJobs(
                    keywords: searchQuery.isEmpty ? "iOS Developer" : searchQuery,
                    location: selectedLocation,
                    experienceLevel: selectedExperienceLevel,
                    limit: pageSize
                )
                
            case .google:
                newJobs = try await externalJobService.fetchGoogleJobs(
                    query: searchQuery.isEmpty ? "iOS Developer" : searchQuery,
                    location: selectedLocation,
                    limit: pageSize
                )
                
            case .indeed:
                newJobs = try await externalJobService.fetchIndeedJobs(
                    keywords: searchQuery.isEmpty ? "iOS Developer" : searchQuery,
                    location: selectedLocation,
                    limit: pageSize
                )
                
            case .aggregated:
                if let resume = resume {
                    // Use semantic search with resume
                    newJobs = try await externalJobService.getResumeBasedRecommendations(
                        resumeId: resume.id,
                        location: selectedLocation,
                        limit: pageSize
                    )
                } else {
                    // Aggregate from all sources
                    newJobs = try await externalJobService.searchAllSources(
                        keywords: searchQuery.isEmpty ? "iOS Developer" : searchQuery,
                        location: selectedLocation,
                        experienceLevel: selectedExperienceLevel,
                        useSemanticMatch: true,
                        limit: pageSize
                    )
                }
                
            case .internal:
                // Use internal job service
                newJobs = try await jobService.getRecommendations(
                    query: searchQuery.isEmpty ? nil : searchQuery,
                    location: selectedLocation,
                    useSemanticSearch: hasResume,
                    limit: pageSize,
                    offset: 0
                )
            }
            
            jobs = newJobs
            currentOffset = pageSize
            hasMore = newJobs.count >= pageSize
            
            // Load saved jobs status
            await loadSavedJobsStatus()
            
        } catch {
            // On error, use sample data for demo
            jobs = JobRecommendation.sampleData
            errorMessage = "Using sample data. \(error.localizedDescription)"
        }
    }
    
    func loadMoreJobs() async {
        guard !isLoading && hasMore else { return }
        
        isLoading = true
        defer { isLoading = false }
        
        do {
            let newJobs: [JobRecommendation]
            
            switch selectedSource {
            case .internal:
                newJobs = try await jobService.getRecommendations(
                    query: searchQuery.isEmpty ? nil : searchQuery,
                    location: selectedLocation,
                    useSemanticSearch: hasResume,
                    limit: pageSize,
                    offset: currentOffset
                )
            default:
                // External sources don't support pagination in this implementation
                hasMore = false
                return
            }
            
            if newJobs.isEmpty {
                hasMore = false
            } else {
                jobs.append(contentsOf: newJobs)
                currentOffset += pageSize
            }
            
        } catch {
            errorMessage = error.localizedDescription
            hasMore = false
        }
    }
    
    func refresh() async {
        await loadJobs()
    }
    
    func searchJobs() async {
        // Debounce search
        try? await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
        await loadJobs()
    }
    
    // MARK: - Job Actions
    
    func toggleSaveJob(_ job: JobRecommendation) async {
        let jobId = job.id
        
        if savedJobs.contains(jobId) {
            // Unsave
            savedJobs.remove(jobId)
            
            do {
                try await jobService.unsaveJob(jobId: jobId)
            } catch {
                // Revert on error
                savedJobs.insert(jobId)
                errorMessage = error.localizedDescription
            }
        } else {
            // Save
            savedJobs.insert(jobId)
            
            do {
                try await jobService.saveJob(jobId: jobId)
            } catch {
                // Revert on error
                savedJobs.remove(jobId)
                errorMessage = error.localizedDescription
            }
        }
        
        // Update jobs array
        if let index = jobs.firstIndex(where: { $0.id == jobId }) {
            var updatedJob = jobs[index]
            // Note: This requires JobRecommendation to be mutable or we need to recreate it
            jobs[index] = updatedJob
        }
    }
    
    private func loadSavedJobsStatus() async {
        do {
            let saved = try await jobService.getSavedJobs()
            savedJobs = Set(saved.map { $0.id })
        } catch {
            // Ignore error, just don't show saved status
        }
    }
    
    // MARK: - Filters
    
    func applyFilters() async {
        await loadJobs()
    }
    
    func clearFilters() async {
        selectedLocation = nil
        selectedExperienceLevel = nil
        selectedEmploymentType = nil
        selectedLocationType = nil
        minSalary = nil
        await loadJobs()
    }
}
