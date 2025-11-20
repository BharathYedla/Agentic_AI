//
//  AppState.swift
//  JobTracker
//
//  Global application state management
//

import Foundation
import Combine

@MainActor
class AppState: ObservableObject {
    // MARK: - Published Properties
    
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var isLoading = false
    @Published var showOnboarding = true
    @Published var errorMessage: String?
    
    // MARK: - Private Properties
    
    private let authService: AuthService
    private let keychainManager: KeychainManager
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Initialization
    
    init(authService: AuthService = AuthService.shared,
         keychainManager: KeychainManager = KeychainManager.shared) {
        self.authService = authService
        self.keychainManager = keychainManager
        
        // Check if user has completed onboarding
        self.showOnboarding = !UserDefaults.standard.bool(forKey: "hasCompletedOnboarding")
        
        // Check for existing authentication
        Task {
            await checkAuthentication()
        }
    }
    
    // MARK: - Authentication Methods
    
    func checkAuthentication() async {
        // Check if we have a valid access token
        if let accessToken = keychainManager.getAccessToken(),
           !accessToken.isEmpty {
            // Verify token is still valid
            do {
                let user = try await authService.getCurrentUser()
                self.currentUser = user
                self.isAuthenticated = true
            } catch {
                // Token is invalid, clear it
                await signOut()
            }
        }
    }
    
    func signIn(email: String, password: String) async throws {
        isLoading = true
        errorMessage = nil
        
        defer { isLoading = false }
        
        do {
            let response = try await authService.signIn(email: email, password: password)
            
            // Save tokens
            keychainManager.saveAccessToken(response.accessToken)
            keychainManager.saveRefreshToken(response.refreshToken)
            
            // Update state
            self.currentUser = response.user
            self.isAuthenticated = true
            
            // Mark onboarding as complete
            completeOnboarding()
            
        } catch {
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    func signUp(email: String, password: String, fullName: String) async throws {
        isLoading = true
        errorMessage = nil
        
        defer { isLoading = false }
        
        do {
            let response = try await authService.signUp(
                email: email,
                password: password,
                fullName: fullName
            )
            
            // Save tokens
            keychainManager.saveAccessToken(response.accessToken)
            keychainManager.saveRefreshToken(response.refreshToken)
            
            // Update state
            self.currentUser = response.user
            self.isAuthenticated = true
            
            // Mark onboarding as complete
            completeOnboarding()
            
        } catch {
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    func signOut() async {
        // Clear tokens
        keychainManager.clearTokens()
        
        // Clear state
        self.currentUser = nil
        self.isAuthenticated = false
    }
    
    func refreshToken() async throws {
        guard let refreshToken = keychainManager.getRefreshToken() else {
            throw AuthError.noRefreshToken
        }
        
        do {
            let response = try await authService.refreshToken(refreshToken)
            
            // Save new tokens
            keychainManager.saveAccessToken(response.accessToken)
            keychainManager.saveRefreshToken(response.refreshToken)
            
            // Update user
            self.currentUser = response.user
            
        } catch {
            // Refresh failed, sign out
            await signOut()
            throw error
        }
    }
    
    // MARK: - Onboarding
    
    func completeOnboarding() {
        UserDefaults.standard.set(true, forKey: "hasCompletedOnboarding")
        showOnboarding = false
    }
    
    func resetOnboarding() {
        UserDefaults.standard.set(false, forKey: "hasCompletedOnboarding")
        showOnboarding = true
    }
}

// MARK: - Auth Error

enum AuthError: LocalizedError {
    case noRefreshToken
    case invalidCredentials
    case networkError
    case serverError
    case unknown
    
    var errorDescription: String? {
        switch self {
        case .noRefreshToken:
            return "No refresh token available"
        case .invalidCredentials:
            return "Invalid email or password"
        case .networkError:
            return "Network connection error"
        case .serverError:
            return "Server error. Please try again later"
        case .unknown:
            return "An unknown error occurred"
        }
    }
}
