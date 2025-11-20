//
//  ApplicationDetailView.swift
//  JobTracker
//
//  Application detail view - Placeholder for Phase 3
//

import SwiftUI

struct ApplicationDetailView: View {
    let application: JobApplication
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // Header
                VStack(alignment: .leading, spacing: 12) {
                    Text(application.roleTitle)
                        .font(.title)
                        .fontWeight(.bold)
                    
                    Text(application.companyName)
                        .font(.title3)
                        .foregroundColor(.secondary)
                    
                    StatusBadge(status: application.status)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(
                    RoundedRectangle(cornerRadius: 16)
                        .fill(Color(.systemBackground))
                        .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
                )
                
                // Details
                VStack(alignment: .leading, spacing: 16) {
                    if let location = application.location {
                        DetailRow(icon: "location.fill", title: "Location", value: location)
                    }
                    
                    if let salary = application.salary {
                        DetailRow(icon: "dollarsign.circle.fill", title: "Salary", value: salary)
                    }
                    
                    DetailRow(
                        icon: "calendar.fill",
                        title: "Applied",
                        value: application.appliedDate.formatted(date: .long, time: .omitted)
                    )
                    
                    DetailRow(
                        icon: "link.circle.fill",
                        title: "Source",
                        value: application.source.displayName
                    )
                }
                .padding()
                .background(
                    RoundedRectangle(cornerRadius: 16)
                        .fill(Color(.systemBackground))
                        .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
                )
                
                // Notes
                if let notes = application.notes {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Notes")
                            .font(.headline)
                        
                        Text(notes)
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color(.systemBackground))
                            .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
                    )
                }
            }
            .padding()
        }
        .navigationTitle("Application Details")
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct DetailRow: View {
    let icon: String
    let title: String
    let value: String
    
    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(.blue)
                .frame(width: 24)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Text(value)
                    .font(.body)
                    .foregroundColor(.primary)
            }
            
            Spacer()
        }
    }
}

#Preview {
    NavigationView {
        ApplicationDetailView(application: JobApplication.sampleData[0])
    }
}
