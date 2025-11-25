import Foundation

struct JobRecommendation: Identifiable, Codable {
    let id: String
    let title: String
    let company: String
    let location: String
    let locationType: String // remote, onsite, hybrid
    let salary: Salary?
    let matchScore: Double
    let postedDate: String
    let companyLogoURL: String?
    let applicationURL: String?
    let description: String?
    let employmentType: String? // full_time, contract, etc.
    let experienceLevel: String? // senior, entry, etc.
    
    struct Salary: Codable {
        let min: Int
        let max: Int
        let currency: String
        let period: String // year, hour, month
        
        var formatted: String {
            let formatter = NumberFormatter()
            formatter.numberStyle = .currency
            formatter.currencyCode = currency
            formatter.maximumFractionDigits = 0
            
            if let minStr = formatter.string(from: NSNumber(value: min)),
               let maxStr = formatter.string(from: NSNumber(value: max)) {
                return "\(minStr) - \(maxStr) / \(period)"
            }
            return "$\(min) - $\(max)"
        }
    }
}
