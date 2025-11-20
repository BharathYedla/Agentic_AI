//
//  JobFiltersView.swift
//  JobTracker
//
//  Job filters view with realistic filter options
//

import SwiftUI

struct JobFiltersView: View {
    @ObservedObject var viewModel: JobsViewModel
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            Form {
                // Location
                Section("Location") {
                    TextField("City, State or Remote", text: Binding(
                        get: { viewModel.selectedLocation ?? "" },
                        set: { viewModel.selectedLocation = $0.isEmpty ? nil : $0 }
                    ))
                    .textContentType(.addressCity)
                    
                    Picker("Location Type", selection: $viewModel.selectedLocationType) {
                        Text("Any").tag(nil as LocationType?)
                        ForEach([LocationType.onsite, .remote, .hybrid], id: \.self) { type in
                            Text(type.displayName).tag(type as LocationType?)
                        }
                    }
                }
                
                // Experience Level
                Section("Experience Level") {
                    Picker("Experience", selection: $viewModel.selectedExperienceLevel) {
                        Text("Any").tag(nil as ExperienceLevel?)
                        ForEach([
                            ExperienceLevel.internship,
                            .entry,
                            .mid,
                            .senior,
                            .lead,
                            .executive
                        ], id: \.self) { level in
                            Text(level.displayName).tag(level as ExperienceLevel?)
                        }
                    }
                }
                
                // Employment Type
                Section("Employment Type") {
                    Picker("Type", selection: $viewModel.selectedEmploymentType) {
                        Text("Any").tag(nil as EmploymentType?)
                        ForEach([
                            EmploymentType.fullTime,
                            .partTime,
                            .contract,
                            .freelance
                        ], id: \.self) { type in
                            Text(type.displayName).tag(type as EmploymentType?)
                        }
                    }
                }
                
                // Salary
                Section("Minimum Salary") {
                    HStack {
                        Text("$")
                            .foregroundColor(AppColors.textSecondary)
                        
                        TextField("Minimum", value: $viewModel.minSalary, format: .number)
                            .keyboardType(.numberPad)
                    }
                    
                    if let minSalary = viewModel.minSalary {
                        Text("Minimum: $\(minSalary.formatted())/year")
                            .font(Typography.caption1)
                            .foregroundColor(AppColors.textSecondary)
                    }
                }
                
                // Actions
                Section {
                    Button(action: {
                        Task {
                            await viewModel.clearFilters()
                            dismiss()
                        }
                    }) {
                        HStack {
                            Spacer()
                            Text("Clear All Filters")
                                .foregroundColor(AppColors.error)
                            Spacer()
                        }
                    }
                }
            }
            .navigationTitle("Filters")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Apply") {
                        Task {
                            await viewModel.applyFilters()
                            dismiss()
                        }
                    }
                    .fontWeight(.semibold)
                }
            }
        }
    }
}

#Preview {
    JobFiltersView(viewModel: JobsViewModel())
}
