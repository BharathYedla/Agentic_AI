//
//  HomeViewModel.swift
//  JobTracker
//
//  View model for home dashboard
//

import Foundation

@MainActor
class HomeViewModel: ObservableObject {
    @Published var stats = HomeStats()
    @Published var recentApplications: [JobApplication] = []
    @Published var upcomingInterviews: [JobApplication] = []
    @Published var actionItems: [ActionItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    // MARK: - Data Loading
    
    func loadData() async {
        isLoading = true
        errorMessage = nil
        
        do {
            // TODO: Replace with actual API calls
            // Simulate network delay
            try await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
            
            // Load sample data
            loadSampleData()
            
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func refresh() async {
        await loadData()
    }
    
    // MARK: - Sample Data
    
    private func loadSampleData() {
        let applications = JobApplication.sampleData
        
        // Calculate stats
        stats = HomeStats(
            totalApplications: applications.count,
            interviews: applications.filter {
                $0.status == .interviewScheduled || $0.status == .interviewCompleted
            }.count,
            offers: applications.filter {
                $0.status == .offerReceived || $0.status == .offerAccepted
            }.count,
            thisWeek: applications.filter {
                Calendar.current.isDate($0.appliedDate, equalTo: Date(), toGranularity: .weekOfYear)
            }.count
        )
        
        // Recent applications (last 5)
        recentApplications = Array(applications.sorted { $0.appliedDate > $1.appliedDate }.prefix(5))
        
        // Upcoming interviews
        upcomingInterviews = applications.filter {
            if let interviewDate = $0.interviewDate {
                return interviewDate > Date()
            }
            return false
        }.sorted { $0.interviewDate! < $1.interviewDate! }
        
        // Action items
        actionItems = generateActionItems(from: applications)
    }
    
    private func generateActionItems(from applications: [JobApplication]) -> [ActionItem] {
        var items: [ActionItem] = []
        
        // Check for applications needing follow-up
        for app in applications where app.status == .applied {
            let daysSinceApplied = Calendar.current.dateComponents([.day], from: app.appliedDate, to: Date()).day ?? 0
            if daysSinceApplied >= 7 {
                items.append(ActionItem(
                    id: UUID().uuidString,
                    title: "Follow up with \(app.companyName)",
                    description: "Applied \(daysSinceApplied) days ago",
                    type: .followUp,
                    dueDate: Date(),
                    applicationId: app.id
                ))
            }
        }
        
        // Check for upcoming interviews
        for app in applications where app.status == .interviewScheduled {
            if let interviewDate = app.interviewDate {
                items.append(ActionItem(
                    id: UUID().uuidString,
                    title: "Prepare for \(app.companyName) interview",
                    description: "Interview on \(interviewDate.formatted(date: .abbreviated, time: .shortened))",
                    type: .interview,
                    dueDate: interviewDate,
                    applicationId: app.id
                ))
            }
        }
        
        return items.sorted { $0.dueDate < $1.dueDate }
    }
}

// MARK: - Action Item

struct ActionItem: Identifiable {
    let id: String
    let title: String
    let description: String
    let type: ActionItemType
    let dueDate: Date
    let applicationId: String
}

enum ActionItemType {
    case followUp
    case interview
    case offer
    case deadline
}
