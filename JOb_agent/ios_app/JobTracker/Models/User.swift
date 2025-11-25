import Foundation

// MARK: - User
struct User: Codable, Identifiable {
    let id: String
    let email: String
    let firstName: String?
    let lastName: String?
    let profileImageURL: String?
    let jobPreferences: JobPreferences?
    
    var fullName: String {
        if let first = firstName, let last = lastName {
            return "\(first) \(last)"
        }
        return firstName ?? "User"
    }
}

struct JobPreferences: Codable {
    var jobTitles: [String]
    var locations: [String]
    var minSalary: Int?
    var remoteOnly: Bool
}

// MARK: - Auth Models
struct AuthResponse: Codable {
    let accessToken: String
    let refreshToken: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case user
    }
}
