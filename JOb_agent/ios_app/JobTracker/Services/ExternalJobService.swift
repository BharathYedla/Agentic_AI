//
//  ExternalJobService.swift
//  JobTracker
//
//  Service for fetching real-time jobs from LinkedIn, Google, and other sources
//

import Foundation

class ExternalJobService {
    static let shared = ExternalJobService()
    
    private let session: URLSession
    
    // API Keys - These should be configured in backend
    private let serpApiKey: String?
    private let clearbitApiKey: String?
    
    private init() {
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: configuration)
        
        // These will be fetched from backend config
        self.serpApiKey = nil // Backend will handle this
        self.clearbitApiKey = nil // Backend will handle this
    }
    
    // MARK: - LinkedIn Jobs Integration
    
    /// Fetch jobs from LinkedIn via backend proxy
    /// Backend will use RapidAPI LinkedIn Jobs API or similar
    func fetchLinkedInJobs(
        keywords: String,
        location: String? = nil,
        experienceLevel: ExperienceLevel? = nil,
        limit: Int = 20
    ) async throws -> [JobRecommendation] {
        // This will call our backend which proxies to LinkedIn API
        let endpoint = "/jobs/external/linkedin"
        
        var params: [String: Any] = [
            "keywords": keywords,
            "limit": limit
        ]
        
        if let location = location {
            params["location"] = location
        }
        
        if let experienceLevel = experienceLevel {
            params["experience_level"] = experienceLevel.rawValue
        }
        
        return try await callBackendJobAPI(endpoint: endpoint, params: params)
    }
    
    // MARK: - Google Jobs Integration
    
    /// Fetch jobs from Google Jobs via SerpAPI
    /// Backend will use SerpAPI Google Jobs API
    func fetchGoogleJobs(
        query: String,
        location: String? = nil,
        limit: Int = 20
    ) async throws -> [JobRecommendation] {
        // This will call our backend which uses SerpAPI
        let endpoint = "/jobs/external/google"
        
        var params: [String: Any] = [
            "query": query,
            "limit": limit
        ]
        
        if let location = location {
            params["location"] = location
        }
        
        return try await callBackendJobAPI(endpoint: endpoint, params: params)
    }
    
    // MARK: - Indeed Jobs Integration
    
    /// Fetch jobs from Indeed
    func fetchIndeedJobs(
        keywords: String,
        location: String? = nil,
        limit: Int = 20
    ) async throws -> [JobRecommendation] {
        let endpoint = "/jobs/external/indeed"
        
        var params: [String: Any] = [
            "keywords": keywords,
            "limit": limit
        ]
        
        if let location = location {
            params["location"] = location
        }
        
        return try await callBackendJobAPI(endpoint: endpoint, params: params)
    }
    
    // MARK: - Aggregated Search
    
    /// Search across all job sources (LinkedIn, Google, Indeed)
    func searchAllSources(
        keywords: String,
        location: String? = nil,
        experienceLevel: ExperienceLevel? = nil,
        useSemanticMatch: Bool = true,
        limit: Int = 50
    ) async throws -> [JobRecommendation] {
        // Backend will aggregate from multiple sources
        let endpoint = "/jobs/external/aggregate"
        
        var params: [String: Any] = [
            "keywords": keywords,
            "limit": limit,
            "use_semantic_match": useSemanticMatch
        ]
        
        if let location = location {
            params["location"] = location
        }
        
        if let experienceLevel = experienceLevel {
            params["experience_level"] = experienceLevel.rawValue
        }
        
        return try await callBackendJobAPI(endpoint: endpoint, params: params)
    }
    
    // MARK: - Company Logo Fetching
    
    /// Fetch company logo URL from Clearbit or similar service
    /// Backend will handle this to avoid exposing API keys
    func fetchCompanyLogo(companyName: String, domain: String? = nil) async throws -> String? {
        let endpoint = "/jobs/company-logo"
        
        var params: [String: Any] = [
            "company_name": companyName
        ]
        
        if let domain = domain {
            params["domain"] = domain
        }
        
        struct LogoResponse: Codable {
            let logoUrl: String?
            
            enum CodingKeys: String, CodingKey {
                case logoUrl = "logo_url"
            }
        }
        
        let response: LogoResponse = try await callBackendAPI(endpoint: endpoint, params: params)
        return response.logoUrl
    }
    
    // MARK: - Semantic Resume Matching
    
    /// Get job recommendations based on resume using semantic search
    /// Uses OpenAI embeddings for matching
    func getResumeBasedRecommendations(
        resumeId: String,
        location: String? = nil,
        limit: Int = 20
    ) async throws -> [JobRecommendation] {
        let endpoint = "/jobs/recommendations/semantic"
        
        var params: [String: Any] = [
            "resume_id": resumeId,
            "limit": limit
        ]
        
        if let location = location {
            params["location"] = location
        }
        
        return try await callBackendJobAPI(endpoint: endpoint, params: params)
    }
    
    // MARK: - Helper Methods
    
    private func callBackendJobAPI(
        endpoint: String,
        params: [String: Any]
    ) async throws -> [JobRecommendation] {
        guard let accessToken = KeychainManager.shared.getAccessToken() else {
            throw NetworkError.unauthorized
        }
        
        #if DEBUG
        let baseURL = "http://localhost:8000/api/v1"
        #else
        let baseURL = "https://api.jobtracker.app/api/v1"
        #endif
        
        guard var urlComponents = URLComponents(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        // Add query parameters
        urlComponents.queryItems = params.map { key, value in
            URLQueryItem(name: key, value: "\(value)")
        }
        
        guard let url = urlComponents.url else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        struct JobsResponse: Codable {
            let jobs: [JobRecommendation]
            let total: Int
            let source: String
        }
        
        let jobsResponse = try decoder.decode(JobsResponse.self, from: data)
        return jobsResponse.jobs
    }
    
    private func callBackendAPI<T: Decodable>(
        endpoint: String,
        params: [String: Any]
    ) async throws -> T {
        guard let accessToken = KeychainManager.shared.getAccessToken() else {
            throw NetworkError.unauthorized
        }
        
        #if DEBUG
        let baseURL = "http://localhost:8000/api/v1"
        #else
        let baseURL = "https://api.jobtracker.app/api/v1"
        #endif
        
        guard var urlComponents = URLComponents(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        urlComponents.queryItems = params.map { key, value in
            URLQueryItem(name: key, value: "\(value)")
        }
        
        guard let url = urlComponents.url else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        return try decoder.decode(T.self, from: data)
    }
}

// MARK: - Job Source

enum JobSource: String, Codable {
    case linkedin = "linkedin"
    case google = "google"
    case indeed = "indeed"
    case internal = "internal"
    case aggregated = "aggregated"
    
    var displayName: String {
        switch self {
        case .linkedin: return "LinkedIn"
        case .google: return "Google Jobs"
        case .indeed: return "Indeed"
        case .internal: return "JobTracker"
        case .aggregated: return "All Sources"
        }
    }
    
    var icon: String {
        switch self {
        case .linkedin: return "link.circle.fill"
        case .google: return "g.circle.fill"
        case .indeed: return "i.circle.fill"
        case .internal: return "star.circle.fill"
        case .aggregated: return "globe"
        }
    }
    
    var color: String {
        switch self {
        case .linkedin: return "blue"
        case .google: return "red"
        case .indeed: return "blue"
        case .internal: return "purple"
        case .aggregated: return "green"
        }
    }
}
