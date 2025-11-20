//
//  AnalyticsView.swift
//  JobTracker
//
//  Analytics view - Placeholder for Phase 6
//

import SwiftUI

struct AnalyticsView: View {
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Summary Cards
                    VStack(spacing: 16) {
                        Text("Overview")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)
                        
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 16) {
                            AnalyticsCard(
                                title: "Success Rate",
                                value: "12%",
                                icon: "chart.line.uptrend.xyaxis",
                                color: .green
                            )
                            
                            AnalyticsCard(
                                title: "Avg Response Time",
                                value: "7 days",
                                icon: "clock.fill",
                                color: .orange
                            )
                            
                            AnalyticsCard(
                                title: "Active Applications",
                                value: "8",
                                icon: "doc.text.fill",
                                color: .blue
                            )
                            
                            AnalyticsCard(
                                title: "Interview Rate",
                                value: "25%",
                                icon: "person.2.fill",
                                color: .purple
                            )
                        }
                    }
                    
                    // Placeholder for charts
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Application Timeline")
                            .font(.headline)
                        
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color(.systemGray6))
                            .frame(height: 200)
                            .overlay(
                                Text("Chart Coming Soon")
                                    .foregroundColor(.secondary)
                            )
                    }
                    
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Status Distribution")
                            .font(.headline)
                        
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color(.systemGray6))
                            .frame(height: 200)
                            .overlay(
                                Text("Chart Coming Soon")
                                    .foregroundColor(.secondary)
                            )
                    }
                }
                .padding()
            }
            .navigationTitle("Analytics")
        }
    }
}

struct AnalyticsCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                
                Spacer()
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text(value)
                    .font(.system(size: 24, weight: .bold))
                    .foregroundColor(.primary)
                
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(Color(.systemBackground))
                .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
        )
    }
}

#Preview {
    AnalyticsView()
}
