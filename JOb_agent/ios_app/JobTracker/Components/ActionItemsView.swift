//
//  ActionItemsView.swift
//  JobTracker
//
//  Action items section for home view
//

import SwiftUI

struct ActionItemsView: View {
    let items: [ActionItem]
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Text("Action Items")
                    .font(.headline)
                
                Spacer()
                
                if !items.isEmpty {
                    Text("\(items.count)")
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.red)
                        .cornerRadius(8)
                }
            }
            
            if items.isEmpty {
                EmptyStateView(
                    icon: "checkmark.circle",
                    title: "All Caught Up!",
                    description: "No pending action items"
                )
                .frame(height: 200)
            } else {
                VStack(spacing: 12) {
                    ForEach(items.prefix(5)) { item in
                        ActionItemRow(item: item)
                    }
                }
            }
        }
    }
}

struct ActionItemRow: View {
    let item: ActionItem
    
    var iconName: String {
        switch item.type {
        case .followUp:
            return "arrow.turn.up.right"
        case .interview:
            return "person.2.fill"
        case .offer:
            return "envelope.open.fill"
        case .deadline:
            return "clock.fill"
        }
    }
    
    var iconColor: Color {
        switch item.type {
        case .followUp:
            return .blue
        case .interview:
            return .orange
        case .offer:
            return .green
        case .deadline:
            return .red
        }
    }
    
    var body: some View {
        HStack(spacing: 16) {
            // Icon
            ZStack {
                Circle()
                    .fill(iconColor.opacity(0.1))
                    .frame(width: 44, height: 44)
                
                Image(systemName: iconName)
                    .font(.title3)
                    .foregroundColor(iconColor)
            }
            
            // Content
            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                    .foregroundColor(.primary)
                    .lineLimit(1)
                
                Text(item.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
            }
            
            Spacer()
            
            // Due date indicator
            if Calendar.current.isDateInToday(item.dueDate) {
                Text("Today")
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(.red)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.red.opacity(0.1))
                    .cornerRadius(6)
            }
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
    ActionItemsView(items: [
        ActionItem(
            id: "1",
            title: "Follow up with Apple",
            description: "Applied 7 days ago",
            type: .followUp,
            dueDate: Date(),
            applicationId: "1"
        ),
        ActionItem(
            id: "2",
            title: "Prepare for Google interview",
            description: "Interview tomorrow",
            type: .interview,
            dueDate: Date().addingTimeInterval(86400),
            applicationId: "2"
        )
    ])
    .padding()
}
