//
//  UpcomingInterviewsView.swift
//  JobTracker
//
//  Upcoming interviews section for home view
//

import SwiftUI

struct UpcomingInterviewsView: View {
    let interviews: [JobApplication]
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Text("Upcoming Interviews")
                    .font(.headline)
                
                Spacer()
            }
            
            VStack(spacing: 12) {
                ForEach(interviews.prefix(3)) { interview in
                    InterviewCard(application: interview)
                }
            }
        }
    }
}

struct InterviewCard: View {
    let application: JobApplication
    
    var body: some View {
        HStack(spacing: 16) {
            // Date Badge
            VStack(spacing: 4) {
                if let interviewDate = application.interviewDate {
                    Text(interviewDate.formatted(.dateTime.day()))
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)
                    
                    Text(interviewDate.formatted(.dateTime.month(.abbreviated)))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .frame(width: 50)
            .padding(.vertical, 8)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.blue.opacity(0.1))
            )
            
            // Interview Info
            VStack(alignment: .leading, spacing: 4) {
                Text(application.roleTitle)
                    .font(.headline)
                    .foregroundColor(.primary)
                    .lineLimit(1)
                
                Text(application.companyName)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
                
                if let interviewDate = application.interviewDate {
                    Text(interviewDate.formatted(.dateTime.hour().minute()))
                        .font(.caption)
                        .foregroundColor(.blue)
                }
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(.systemBackground))
                .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
        )
    }
}

#Preview {
    UpcomingInterviewsView(interviews: JobApplication.sampleData.filter { $0.interviewDate != nil })
        .padding()
}
