import SwiftUI

struct MainTabView: View {
    var body: some View {
        TabView {
            Text("Home")
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }
            
            JobsView()
                .tabItem {
                    Label("Jobs", systemImage: "briefcase.fill")
                }
            
            Text("Applications")
                .tabItem {
                    Label("Applications", systemImage: "doc.text.fill")
                }
            
            Text("Analytics")
                .tabItem {
                    Label("Analytics", systemImage: "chart.bar.fill")
                }
            
            Text("Profile")
                .tabItem {
                    Label("Profile", systemImage: "person.fill")
                }
        }
        .accentColor(DesignSystem.Colors.primary)
    }
}
