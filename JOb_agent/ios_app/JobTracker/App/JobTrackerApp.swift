import SwiftUI

@main
struct JobTrackerApp: App {
    @StateObject private var appState = AppState.shared
    
    var body: some Scene {
        WindowGroup {
            if appState.isAuthenticated {
                MainTabView()
            } else {
                // For now, bypass auth for testing
                MainTabView()
                // SignInView()
            }
        }
    }
}
