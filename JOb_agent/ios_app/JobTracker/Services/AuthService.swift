//
//  AuthService.swift
//  JobTracker
//
//  Authentication API service
//

import Foundation

class AuthService {
    static let shared = AuthService()
    
    private let baseURL: String
    private let session: URLSession
    
    private init() {
        // TODO: Move to configuration file
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
    
    // MARK: - Authentication Methods
    
    func signUp(email: String, password: String, fullName: String) async throws -> AuthResponse {
        let request = SignUpRequest(email: email, password: password, fullName: fullName)
        
        return try await performRequest(
            endpoint: "/auth/signup",
            method: "POST",
            body: request
        )
    }
    
    func signIn(email: String, password: String) async throws -> AuthResponse {
        let request = SignInRequest(email: email, password: password)
        
        return try await performRequest(
            endpoint: "/auth/signin",
            method: "POST",
            body: request
        )
    }
    
    func refreshToken(_ refreshToken: String) async throws -> AuthResponse {
        let request = RefreshTokenRequest(refreshToken: refreshToken)
        
        return try await performRequest(
            endpoint: "/auth/refresh",
            method: "POST",
            body: request
        )
    }
    
    func getCurrentUser() async throws -> User {
        return try await performAuthenticatedRequest(
            endpoint: "/auth/me",
            method: "GET"
        )
    }
    
    func requestPasswordReset(email: String) async throws {
        let request = PasswordResetRequest(email: email)
        
        let _: EmptyResponse = try await performRequest(
            endpoint: "/auth/password-reset",
            method: "POST",
            body: request
        )
    }
    
    func confirmPasswordReset(token: String, newPassword: String) async throws {
        let request = PasswordResetConfirm(token: token, newPassword: newPassword)
        
        let _: EmptyResponse = try await performRequest(
            endpoint: "/auth/password-reset/confirm",
            method: "POST",
            body: request
        )
    }
    
    // MARK: - Generic Request Methods
    
    private func performRequest<T: Decodable, B: Encodable>(
        endpoint: String,
        method: String,
        body: B? = nil
    ) async throws -> T {
        guard let url = URL(string: baseURL + endpoint) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            // Try to decode error response
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.detail)
            }
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        return try decoder.decode(T.self, from: data)
    }
    
    private func performAuthenticatedRequest<T: Decodable>(
        endpoint: String,
        method: String
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
        
        return try decoder.decode(T.self, from: data)
    }
}

// MARK: - Network Error

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case httpError(Int)
    case serverError(String)
    case decodingError
    case unknown
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .unauthorized:
            return "Unauthorized. Please sign in again"
        case .httpError(let code):
            return "HTTP error: \(code)"
        case .serverError(let message):
            return message
        case .decodingError:
            return "Failed to decode response"
        case .unknown:
            return "An unknown error occurred"
        }
    }
}

// MARK: - Response Models

struct ErrorResponse: Codable {
    let detail: String
}

struct EmptyResponse: Codable {}
