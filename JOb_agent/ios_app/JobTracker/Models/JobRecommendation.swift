//
//  JobRecommendation.swift
//  JobTracker
//
//  Job recommendation model with semantic matching
//

import Foundation

// MARK: - Job Recommendation Model

struct JobRecommendation: Codable, Identifiable {
    let id: String
    let title: String
    let company: String
    let location: String
    let locationType: LocationType
    let salary: SalaryRange?
    let description: String
    let requirements: [String]
    let benefits: [String]
    let postedDate: Date
    let applicationUrl: String
    let matchScore: Double // 0.0 to 1.0
    let matchReasons: [String]
    let skills: [String]
    let experienceLevel: ExperienceLevel
    let employmentType: EmploymentType
    let companyLogo: String?
    let isRemote: Bool
    let isSaved: Bool
    
    enum CodingKeys: String, CodingKey {
        case id
        case title
        case company
        case location
        case locationType = "location_type"
        case salary
        case description
        case requirements
        case benefits
        case postedDate = "posted_date"
        case applicationUrl = "application_url"
        case matchScore = "match_score"
        case matchReasons = "match_reasons"
        case skills
        case experienceLevel = "experience_level"
        case employmentType = "employment_type"
        case companyLogo = "company_logo"
        case isRemote = "is_remote"
        case isSaved = "is_saved"
    }
}

// MARK: - Location Type

enum LocationType: String, Codable {
    case onsite = "onsite"
    case remote = "remote"
    case hybrid = "hybrid"
    
    var displayName: String {
        switch self {
        case .onsite: return "On-site"
        case .remote: return "Remote"
        case .hybrid: return "Hybrid"
        }
    }
    
    var icon: String {
        switch self {
        case .onsite: return "building.2.fill"
        case .remote: return "house.fill"
        case .hybrid: return "arrow.left.arrow.right"
        }
    }
}

// MARK: - Experience Level

enum ExperienceLevel: String, Codable {
    case internship = "internship"
    case entry = "entry"
    case mid = "mid"
    case senior = "senior"
    case lead = "lead"
    case executive = "executive"
    
    var displayName: String {
        switch self {
        case .internship: return "Internship"
        case .entry: return "Entry Level"
        case .mid: return "Mid Level"
        case .senior: return "Senior"
        case .lead: return "Lead"
        case .executive: return "Executive"
        }
    }
}

// MARK: - Employment Type

enum EmploymentType: String, Codable {
    case fullTime = "full_time"
    case partTime = "part_time"
    case contract = "contract"
    case freelance = "freelance"
    
    var displayName: String {
        switch self {
        case .fullTime: return "Full-time"
        case .partTime: return "Part-time"
        case .contract: return "Contract"
        case .freelance: return "Freelance"
        }
    }
}

// MARK: - Salary Range

struct SalaryRange: Codable {
    let min: Int
    let max: Int
    let currency: String
    let period: SalaryPeriod
    
    var displayString: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = currency
        formatter.maximumFractionDigits = 0
        
        let minStr = formatter.string(from: NSNumber(value: min)) ?? "\(min)"
        let maxStr = formatter.string(from: NSNumber(value: max)) ?? "\(max)"
        
        return "\(minStr) - \(maxStr) / \(period.displayName)"
    }
}

enum SalaryPeriod: String, Codable {
    case hour = "hour"
    case day = "day"
    case month = "month"
    case year = "year"
    
    var displayName: String {
        switch self {
        case .hour: return "hr"
        case .day: return "day"
        case .month: return "mo"
        case .year: return "yr"
        }
    }
}

// MARK: - Resume Model

struct Resume: Codable {
    let id: String
    let userId: String
    let fileName: String
    let fileUrl: String
    let parsedText: String
    let skills: [String]
    let experience: [WorkExperience]
    let education: [Education]
    let summary: String?
    let uploadedAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case fileName = "file_name"
        case fileUrl = "file_url"
        case parsedText = "parsed_text"
        case skills
        case experience
        case education
        case summary
        case uploadedAt = "uploaded_at"
        case updatedAt = "updated_at"
    }
}

struct WorkExperience: Codable {
    let company: String
    let title: String
    let startDate: String
    let endDate: String?
    let description: String
    let isCurrent: Bool
    
    enum CodingKeys: String, CodingKey {
        case company
        case title
        case startDate = "start_date"
        case endDate = "end_date"
        case description
        case isCurrent = "is_current"
    }
}

struct Education: Codable {
    let institution: String
    let degree: String
    let field: String
    let graduationYear: String
    
    enum CodingKeys: String, CodingKey {
        case institution
        case degree
        case field
        case graduationYear = "graduation_year"
    }
}

// MARK: - Job Search Request

struct JobSearchRequest: Codable {
    let query: String?
    let location: String?
    let locationType: LocationType?
    let experienceLevel: ExperienceLevel?
    let employmentType: EmploymentType?
    let minSalary: Int?
    let skills: [String]?
    let useSemanticSearch: Bool
    let limit: Int
    let offset: Int
    
    enum CodingKeys: String, CodingKey {
        case query
        case location
        case locationType = "location_type"
        case experienceLevel = "experience_level"
        case employmentType = "employment_type"
        case minSalary = "min_salary"
        case skills
        case useSemanticSearch = "use_semantic_search"
        case limit
        case offset
    }
}

// MARK: - Sample Data

extension JobRecommendation {
    static var sampleData: [JobRecommendation] {
        [
            JobRecommendation(
                id: "1",
                title: "Senior iOS Engineer",
                company: "Apple",
                location: "Cupertino, CA",
                locationType: .hybrid,
                salary: SalaryRange(min: 150000, max: 220000, currency: "USD", period: .year),
                description: "Join our team building the next generation of iOS applications. Work on cutting-edge features used by millions of users worldwide.",
                requirements: [
                    "5+ years iOS development experience",
                    "Expert in Swift and SwiftUI",
                    "Strong understanding of iOS frameworks",
                    "Experience with CI/CD pipelines"
                ],
                benefits: [
                    "Health insurance",
                    "401k matching",
                    "Stock options",
                    "Flexible hours"
                ],
                postedDate: Date().addingTimeInterval(-86400 * 2),
                applicationUrl: "https://apple.com/careers/job1",
                matchScore: 0.95,
                matchReasons: [
                    "Strong match with your iOS development experience",
                    "Your SwiftUI skills align perfectly",
                    "Location preference matches"
                ],
                skills: ["Swift", "SwiftUI", "iOS", "Xcode", "Git"],
                experienceLevel: .senior,
                employmentType: .fullTime,
                companyLogo: nil,
                isRemote: false,
                isSaved: false
            ),
            JobRecommendation(
                id: "2",
                title: "Mobile Software Engineer",
                company: "Google",
                location: "Remote",
                locationType: .remote,
                salary: SalaryRange(min: 140000, max: 200000, currency: "USD", period: .year),
                description: "Build innovative mobile applications that impact billions of users. Work with cutting-edge technology and talented engineers.",
                requirements: [
                    "3+ years mobile development",
                    "Experience with iOS or Android",
                    "Strong CS fundamentals",
                    "Passion for user experience"
                ],
                benefits: [
                    "Competitive salary",
                    "Remote work",
                    "Learning budget",
                    "Top-tier benefits"
                ],
                postedDate: Date().addingTimeInterval(-86400 * 5),
                applicationUrl: "https://google.com/careers/job2",
                matchScore: 0.88,
                matchReasons: [
                    "Your mobile development background is a great fit",
                    "Remote work preference matches",
                    "Skills align with requirements"
                ],
                skills: ["iOS", "Swift", "Mobile Development", "API Integration"],
                experienceLevel: .mid,
                employmentType: .fullTime,
                companyLogo: nil,
                isRemote: true,
                isSaved: false
            ),
            JobRecommendation(
                id: "3",
                title: "iOS Developer",
                company: "Meta",
                location: "Menlo Park, CA",
                locationType: .onsite,
                salary: SalaryRange(min: 130000, max: 190000, currency: "USD", period: .year),
                description: "Create amazing mobile experiences for Facebook, Instagram, and WhatsApp. Join a team of world-class engineers.",
                requirements: [
                    "2+ years iOS development",
                    "Proficiency in Swift",
                    "Understanding of mobile architecture",
                    "Team collaboration skills"
                ],
                benefits: [
                    "Equity grants",
                    "Free meals",
                    "Gym membership",
                    "Career development"
                ],
                postedDate: Date().addingTimeInterval(-86400 * 1),
                applicationUrl: "https://meta.com/careers/job3",
                matchScore: 0.82,
                matchReasons: [
                    "Your iOS skills match well",
                    "Experience level aligns",
                    "Tech stack compatibility"
                ],
                skills: ["Swift", "iOS", "UIKit", "Networking"],
                experienceLevel: .mid,
                employmentType: .fullTime,
                companyLogo: nil,
                isRemote: false,
                isSaved: true
            ),
            JobRecommendation(
                id: "4",
                title: "Lead Mobile Engineer",
                company: "Airbnb",
                location: "San Francisco, CA",
                locationType: .hybrid,
                salary: SalaryRange(min: 180000, max: 250000, currency: "USD", period: .year),
                description: "Lead our mobile engineering team in building world-class travel experiences. Mentor engineers and drive technical excellence.",
                requirements: [
                    "7+ years mobile development",
                    "Leadership experience",
                    "iOS and Android expertise",
                    "System design skills"
                ],
                benefits: [
                    "Travel credits",
                    "Stock options",
                    "Premium benefits",
                    "Flexible schedule"
                ],
                postedDate: Date().addingTimeInterval(-86400 * 7),
                applicationUrl: "https://airbnb.com/careers/job4",
                matchScore: 0.78,
                matchReasons: [
                    "Your technical skills are strong",
                    "Experience level is close",
                    "Location works well"
                ],
                skills: ["iOS", "Android", "Leadership", "Architecture"],
                experienceLevel: .lead,
                employmentType: .fullTime,
                companyLogo: nil,
                isRemote: false,
                isSaved: false
            ),
            JobRecommendation(
                id: "5",
                title: "iOS Engineer - Remote",
                company: "Stripe",
                location: "Remote (US)",
                locationType: .remote,
                salary: SalaryRange(min: 150000, max: 210000, currency: "USD", period: .year),
                description: "Build the future of online payments. Work on iOS SDKs and applications used by millions of businesses worldwide.",
                requirements: [
                    "4+ years iOS development",
                    "Experience with payment systems",
                    "Strong Swift skills",
                    "API design experience"
                ],
                benefits: [
                    "Remote-first culture",
                    "Unlimited PTO",
                    "Home office setup",
                    "Professional development"
                ],
                postedDate: Date().addingTimeInterval(-86400 * 3),
                applicationUrl: "https://stripe.com/careers/job5",
                matchScore: 0.91,
                matchReasons: [
                    "Excellent match with your iOS expertise",
                    "Remote work preference aligns",
                    "Skills are highly relevant"
                ],
                skills: ["Swift", "iOS", "API Design", "Payments"],
                experienceLevel: .senior,
                employmentType: .fullTime,
                companyLogo: nil,
                isRemote: true,
                isSaved: false
            )
        ]
    }
}
