//
//  JobApplication.swift
//  JobTracker
//
//  Job application model
//

import Foundation

// MARK: - Job Application Model

struct JobApplication: Codable, Identifiable {
    let id: String
    let userId: String
    let companyName: String
    let roleTitle: String
    let jobDescription: String?
    let location: String?
    let salary: String?
    let status: ApplicationStatus
    let appliedDate: Date
    let source: ApplicationSource
    let url: String?
    let notes: String?
    let interviewDate: Date?
    let offerDate: Date?
    let responseDate: Date?
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case companyName = "company_name"
        case roleTitle = "role_title"
        case jobDescription = "job_description"
        case location
        case salary
        case status
        case appliedDate = "applied_date"
        case source
        case url
        case notes
        case interviewDate = "interview_date"
        case offerDate = "offer_date"
        case responseDate = "response_date"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

// MARK: - Application Status

enum ApplicationStatus: String, Codable, CaseIterable {
    case applied = "applied"
    case inProgress = "in_progress"
    case interviewScheduled = "interview_scheduled"
    case interviewCompleted = "interview_completed"
    case offerReceived = "offer_received"
    case offerAccepted = "offer_accepted"
    case offerDeclined = "offer_declined"
    case rejected = "rejected"
    case withdrawn = "withdrawn"
    
    var displayName: String {
        switch self {
        case .applied:
            return "Applied"
        case .inProgress:
            return "In Progress"
        case .interviewScheduled:
            return "Interview Scheduled"
        case .interviewCompleted:
            return "Interview Completed"
        case .offerReceived:
            return "Offer Received"
        case .offerAccepted:
            return "Offer Accepted"
        case .offerDeclined:
            return "Offer Declined"
        case .rejected:
            return "Rejected"
        case .withdrawn:
            return "Withdrawn"
        }
    }
    
    var icon: String {
        switch self {
        case .applied:
            return "paperplane.fill"
        case .inProgress:
            return "hourglass"
        case .interviewScheduled:
            return "calendar.badge.clock"
        case .interviewCompleted:
            return "checkmark.circle"
        case .offerReceived:
            return "envelope.open.fill"
        case .offerAccepted:
            return "hand.thumbsup.fill"
        case .offerDeclined:
            return "hand.thumbsdown.fill"
        case .rejected:
            return "xmark.circle.fill"
        case .withdrawn:
            return "arrow.uturn.backward"
        }
    }
}

// MARK: - Application Source

enum ApplicationSource: String, Codable {
    case email = "email"
    case manual = "manual"
    case linkedin = "linkedin"
    case indeed = "indeed"
    case other = "other"
    
    var displayName: String {
        switch self {
        case .email:
            return "Email"
        case .manual:
            return "Manual Entry"
        case .linkedin:
            return "LinkedIn"
        case .indeed:
            return "Indeed"
        case .other:
            return "Other"
        }
    }
}

// MARK: - Sample Data

extension JobApplication {
    static var sampleData: [JobApplication] {
        [
            JobApplication(
                id: "1",
                userId: "user1",
                companyName: "Apple",
                roleTitle: "iOS Engineer",
                jobDescription: "Build amazing iOS apps",
                location: "Cupertino, CA",
                salary: "$150,000 - $200,000",
                status: .interviewScheduled,
                appliedDate: Date().addingTimeInterval(-86400 * 7),
                source: .linkedin,
                url: "https://apple.com/jobs",
                notes: "Great opportunity!",
                interviewDate: Date().addingTimeInterval(86400 * 3),
                offerDate: nil,
                responseDate: Date().addingTimeInterval(-86400 * 3),
                createdAt: Date().addingTimeInterval(-86400 * 7),
                updatedAt: Date()
            ),
            JobApplication(
                id: "2",
                userId: "user1",
                companyName: "Google",
                roleTitle: "Senior Software Engineer",
                jobDescription: "Work on cutting-edge technology",
                location: "Mountain View, CA",
                salary: "$180,000 - $250,000",
                status: .applied,
                appliedDate: Date().addingTimeInterval(-86400 * 3),
                source: .email,
                url: "https://google.com/careers",
                notes: nil,
                interviewDate: nil,
                offerDate: nil,
                responseDate: nil,
                createdAt: Date().addingTimeInterval(-86400 * 3),
                updatedAt: Date()
            ),
            JobApplication(
                id: "3",
                userId: "user1",
                companyName: "Meta",
                roleTitle: "Product Engineer",
                jobDescription: "Build products used by billions",
                location: "Menlo Park, CA",
                salary: "$170,000 - $230,000",
                status: .offerReceived,
                appliedDate: Date().addingTimeInterval(-86400 * 14),
                source: .linkedin,
                url: "https://meta.com/careers",
                notes: "Exciting role!",
                interviewDate: Date().addingTimeInterval(-86400 * 5),
                offerDate: Date().addingTimeInterval(-86400 * 1),
                responseDate: Date().addingTimeInterval(-86400 * 10),
                createdAt: Date().addingTimeInterval(-86400 * 14),
                updatedAt: Date()
            ),
            JobApplication(
                id: "4",
                userId: "user1",
                companyName: "Amazon",
                roleTitle: "Software Development Engineer",
                jobDescription: "Build scalable systems",
                location: "Seattle, WA",
                salary: "$160,000 - $220,000",
                status: .rejected,
                appliedDate: Date().addingTimeInterval(-86400 * 21),
                source: .indeed,
                url: "https://amazon.jobs",
                notes: "Not a good fit",
                interviewDate: Date().addingTimeInterval(-86400 * 14),
                offerDate: nil,
                responseDate: Date().addingTimeInterval(-86400 * 7),
                createdAt: Date().addingTimeInterval(-86400 * 21),
                updatedAt: Date()
            ),
            JobApplication(
                id: "5",
                userId: "user1",
                companyName: "Microsoft",
                roleTitle: "Principal Engineer",
                jobDescription: "Lead technical initiatives",
                location: "Redmond, WA",
                salary: "$200,000 - $280,000",
                status: .inProgress,
                appliedDate: Date().addingTimeInterval(-86400 * 5),
                source: .email,
                url: "https://microsoft.com/careers",
                notes: "Promising opportunity",
                interviewDate: nil,
                offerDate: nil,
                responseDate: Date().addingTimeInterval(-86400 * 2),
                createdAt: Date().addingTimeInterval(-86400 * 5),
                updatedAt: Date()
            )
        ]
    }
}
