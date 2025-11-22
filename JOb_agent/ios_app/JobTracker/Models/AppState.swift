import Foundation
import Combine

class AppState: ObservableObject {
    @Published var isAuthenticated: Bool = false
    @Published var currentUser: User?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    
    static let shared = AppState()
    
    private init() {}
    
    func logout() {
        self.isAuthenticated = false
        self.currentUser = nil
        // Clear tokens from Keychain
    }
}
