//
//  JobTrackerApp.swift
//  JobTracker
//
//  Main app entry point
//

import SwiftUI

@main
struct JobTrackerApp: App {
    // App state
    @StateObject private var appState = AppState()
    @StateObject private var authViewModel = AuthenticationViewModel()
    @StateObject private var themeManager = ThemeManager()
    
    // Scene phase for app lifecycle
    @Environment(\.scenePhase) private var scenePhase
    
    init() {
        // Configure app appearance
        configureAppearance()
        
        // Setup notifications
        NotificationManager.shared.requestAuthorization()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environmentObject(authViewModel)
                .environmentObject(themeManager)
                .preferredColorScheme(themeManager.colorScheme)
                .onAppear {
                    // Check authentication status
                    authViewModel.checkAuthStatus()
                }
                .onChange(of: scenePhase) { newPhase in
                    handleScenePhaseChange(newPhase)
                }
        }
    }
    
    // MARK: - Private Methods
    
    private func configureAppearance() {
        // Configure navigation bar appearance
        let appearance = UINavigationBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor(named: "BackgroundPrimary")
        appearance.titleTextAttributes = [
            .foregroundColor: UIColor(named: "TextPrimary") ?? .label,
            .font: UIFont.systemFont(ofSize: 18, weight: .semibold)
        ]
        appearance.largeTitleTextAttributes = [
            .foregroundColor: UIColor(named: "TextPrimary") ?? .label,
            .font: UIFont.systemFont(ofSize: 34, weight: .bold)
        ]
        
        UINavigationBar.appearance().standardAppearance = appearance
        UINavigationBar.appearance().scrollEdgeAppearance = appearance
        UINavigationBar.appearance().compactAppearance = appearance
        
        // Configure tab bar appearance
        let tabBarAppearance = UITabBarAppearance()
        tabBarAppearance.configureWithOpaqueBackground()
        tabBarAppearance.backgroundColor = UIColor(named: "BackgroundPrimary")
        
        UITabBar.appearance().standardAppearance = tabBarAppearance
        UITabBar.appearance().scrollEdgeAppearance = tabBarAppearance
    }
    
    private func handleScenePhaseChange(_ phase: ScenePhase) {
        switch phase {
        case .active:
            // App became active
            appState.isActive = true
            // Sync data if needed
            if authViewModel.isAuthenticated {
                Task {
                    await appState.syncData()
                }
            }
        case .inactive:
            // App became inactive
            appState.isActive = false
        case .background:
            // App went to background
            appState.saveState()
        @unknown default:
            break
        }
    }
}

// MARK: - Content View

struct ContentView: View {
    @EnvironmentObject var authViewModel: AuthenticationViewModel
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        Group {
            if authViewModel.isLoading {
                // Loading screen
                LoadingView()
            } else if authViewModel.isAuthenticated {
                // Main app interface
                MainTabView()
                    .transition(.opacity)
            } else {
                // Authentication flow
                OnboardingView()
                    .transition(.opacity)
            }
        }
        .animation(.easeInOut, value: authViewModel.isAuthenticated)
    }
}

// MARK: - App State

class AppState: ObservableObject {
    @Published var isActive: bool = true
    @Published var isSyncing: Bool = false
    @Published var lastSyncDate: Date?
    
    // Sync data from backend
    func syncData() async {
        guard !isSyncing else { return }
        
        await MainActor.run {
            isSyncing = true
        }
        
        // Perform sync operations
        do {
            // Sync applications, emails, etc.
            try await APIService.shared.syncAllData()
            
            await MainActor.run {
                lastSyncDate = Date()
                isSyncing = false
            }
        } catch {
            print("Sync error: \(error)")
            await MainActor.run {
                isSyncing = false
            }
        }
    }
    
    // Save app state
    func saveState() {
        // Save any pending data
        UserDefaults.standard.set(lastSyncDate, forKey: "lastSyncDate")
    }
}

// MARK: - Theme Manager

class ThemeManager: ObservableObject {
    @Published var colorScheme: ColorScheme?
    @Published var accentColor: Color = .blue
    
    init() {
        loadThemePreferences()
    }
    
    private func loadThemePreferences() {
        // Load from UserDefaults
        if let themeString = UserDefaults.standard.string(forKey: "theme") {
            switch themeString {
            case "light":
                colorScheme = .light
            case "dark":
                colorScheme = .dark
            default:
                colorScheme = nil // System
            }
        }
        
        // Load accent color
        if let colorData = UserDefaults.standard.data(forKey: "accentColor"),
           let color = try? JSONDecoder().decode(CodableColor.self, from: colorData) {
            accentColor = color.color
        }
    }
    
    func setTheme(_ theme: String) {
        UserDefaults.standard.set(theme, forKey: "theme")
        switch theme {
        case "light":
            colorScheme = .light
        case "dark":
            colorScheme = .dark
        default:
            colorScheme = nil
        }
    }
}

// MARK: - Preview

#Preview {
    ContentView()
        .environmentObject(AppState())
        .environmentObject(AuthenticationViewModel())
        .environmentObject(ThemeManager())
}
