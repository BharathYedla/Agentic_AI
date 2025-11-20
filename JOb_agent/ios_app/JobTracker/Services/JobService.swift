//
//  JobService.swift
//  JobTracker
//
//  Job recommendation service with semantic search
//

import Foundation

class JobService {
    static let shared = JobService()
    
    private let baseURL: String
    private let session: URLSession
    
    private init() {
        #if DEBUG
        self.baseURL = "http://localhost:8000/api/v1"
        #else
        self.baseURL = "https://api.jobtracker.app/api/v1"
        #endif
        
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 30
        configuration.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: configuration)
    }
    
    // MARK: - Job Recommendations
    
    func getRecommendations(
        query: String? = nil,
        location: String? = nil,
        useSemanticSearch: Bool = true,
        limit: Int = 20,
        offset: Int = 0
    ) async throws -> [JobRecommendation] {
        let request = JobSearchRequest(
            query: query,
            location: location,
            locationType: nil,
            experienceLevel: nil,
            employmentType: nil,
            minSalary: nil,
            skills: nil,
            useSemanticSearch: useSemanticSearch,
            limit: limit,
            offset: offset
        )
        
        return try await performAuthenticatedRequest(
            endpoint: "/jobs/recommendations",
            method: "POST",
            body: request
        )
    }
    
    func searchJobs(request: JobSearchRequest) async throws -> [JobRecommendation] {
        return try await performAuthenticatedRequest(
            endpoint: "/jobs/search",
            method: "POST",
            body: request
        )
    }
    
    func getJobDetails(jobId: String) async throws -> JobRecommendation {
        return try await performAuthenticatedRequest(
            endpoint: "/jobs/\(jobId)",
            method: "GET"
        )
    }
    
    func saveJob(jobId: String) async throws {
        let _: EmptyResponse = try await performAuthenticatedRequest(
            endpoint: "/jobs/\(jobId)/save",
            method: "POST"
        )
    }
    
    func unsaveJob(jobId: String) async throws {
        let _: EmptyResponse = try await performAuthenticatedRequest(
            endpoint: "/jobs/\(jobId)/save",
            method: "DELETE"
        )
    }
    
    func getSavedJobs() async throws -> [JobRecommendation] {
        return try await performAuthenticatedRequest(
            endpoint: "/jobs/saved",
            method: "GET"
        )
    }
    
    // MARK: - Resume Management
    
    func uploadResume(fileData: Data, fileName: String) async throws -> Resume {
        guard let accessToken = KeychainManager.shared.getAccessToken() else {
            throw NetworkError.unauthorized
        }
        
        guard let url = URL(string: baseURL + "/resume/upload") else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add file data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/pdf\r\n\r\n".data(using: .utf8)!)
        body.append(fileData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        return try decoder.decode(Resume.self, from: data)
    }
    
    func getResume() async throws -> Resume? {
        do {
            return try await performAuthenticatedRequest(
                endpoint: "/resume",
                method: "GET"
            )
        } catch NetworkError.httpError(404) {
            return nil
        }
    }
    
    func deleteResume() async throws {
        let _: EmptyResponse = try await performAuthenticatedRequest(
            endpoint: "/resume",
            method: "DELETE"
        )
    }
    
    // MARK: - Generic Request Methods
    
    private func performAuthenticatedRequest<T: Decodable, B: Encodable>(
        endpoint: String,
        method: String,
        body: B? = nil
    ) async throws -> T {
        guard let accessToken = KeychainManager.shared.getAccessToken() else {
            throw NetworkError.unauthorized
        }
        
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        
        if let body = body {
            let encoder = JSONEncoder()
            encoder.keyEncodingStrategy = .convertToSnakeCase
            request.httpBody = try encoder.encode(body)
        }
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            if httpResponse.statusCode == 401 {
                throw NetworkError.unauthorized
            }
            
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.detail)
            }
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        
        return try decoder.decode(T.self, from: data)
    }
    
    private func performAuthenticatedRequest<T: Decodable>(
        endpoint: String,
        method: String
    ) async throws -> T {
        let emptyBody: EmptyRequest? = nil
        return try await performAuthenticatedRequest(
            endpoint: endpoint,
            method: method,
            body: emptyBody
        )
    }
}

// MARK: - Helper Models

struct EmptyRequest: Codable {}
