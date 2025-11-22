import Foundation
import Combine

class ExternalJobService: ObservableObject {
    @Published var jobs: [JobRecommendation] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    // Use localhost for simulator
    private let baseURL = "http://localhost:8000/api/v1"
    
    func fetchJobs(keywords: String = "iOS Developer", location: String = "San Francisco") {
        // Construct URL safely
        var components = URLComponents(string: "\(baseURL)/jobs/search")
        components?.queryItems = [
            URLQueryItem(name: "keywords", value: keywords),
            URLQueryItem(name: "location", value: location),
            URLQueryItem(name: "limit", value: "20")
        ]
        
        guard let url = components?.url else {
            self.errorMessage = "Invalid URL"
            return
        }
        
        print("Fetching jobs from: \(url.absoluteString)")
        
        self.isLoading = true
        self.errorMessage = nil
        
        URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isLoading = false
                
                if let error = error {
                    print("Network error: \(error.localizedDescription)")
                    self?.errorMessage = "Network error: \(error.localizedDescription)"
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    self?.errorMessage = "Invalid response"
                    return
                }
                
                if httpResponse.statusCode != 200 {
                    self?.errorMessage = "Server error: \(httpResponse.statusCode)"
                    return
                }
                
                guard let data = data else {
                    self?.errorMessage = "No data received"
                    return
                }
                
                // Debug: Print JSON
                if let jsonStr = String(data: data, encoding: .utf8) {
                    print("Received JSON: \(jsonStr)")
                }
                
                do {
                    let response = try JSONDecoder().decode(JobSearchResponse.self, from: data)
                    self?.jobs = response.jobs
                } catch {
                    print("Decoding error: \(error)")
                    self?.errorMessage = "Failed to parse jobs"
                }
            }
        }.resume()
    }
}

struct JobSearchResponse: Codable {
    let jobs: [JobRecommendation]
    let total: Int
    let source: String
}
