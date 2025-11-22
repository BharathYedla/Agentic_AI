import Foundation

struct JobApplication: Identifiable, Codable {
    let id: String
    let company: String
    let role: String
    let status: ApplicationStatus
    let appliedDate: Date
    let url: String?
    
    enum ApplicationStatus: String, Codable {
        case applied
        case interviewing
        case offer
        case rejected
    }
}
