import Foundation
import Combine

class AuthService: ObservableObject {
    @Published var isAuthenticated = false
    
    static let shared = AuthService()
    
    private init() {}
    
    func signIn(email: String, password: String) async throws {
        // Simulate network delay
        try await Task.sleep(nanoseconds: 1_000_000_000)
        
        // Mock success
        DispatchQueue.main.async {
            self.isAuthenticated = true
            AppState.shared.isAuthenticated = true
        }
    }
    
    func signUp(email: String, password: String) async throws {
        // Simulate network delay
        try await Task.sleep(nanoseconds: 1_000_000_000)
        
        // Mock success
        DispatchQueue.main.async {
            self.isAuthenticated = true
            AppState.shared.isAuthenticated = true
        }
    }
    
    func signOut() {
        self.isAuthenticated = false
        AppState.shared.isAuthenticated = false
    }
}
