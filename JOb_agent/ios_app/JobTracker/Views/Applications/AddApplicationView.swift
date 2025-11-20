//
//  AddApplicationView.swift
//  JobTracker
//
//  Add application view - Placeholder for Phase 3
//

import SwiftUI

struct AddApplicationView: View {
    @Environment(\.dismiss) var dismiss
    @State private var companyName = ""
    @State private var roleTitle = ""
    @State private var location = ""
    @State private var salary = ""
    @State private var url = ""
    @State private var notes = ""
    @State private var status: ApplicationStatus = .applied
    @State private var source: ApplicationSource = .manual
    
    var body: some View {
        NavigationView {
            Form {
                Section("Basic Information") {
                    TextField("Company Name", text: $companyName)
                    TextField("Role Title", text: $roleTitle)
                    TextField("Location", text: $location)
                }
                
                Section("Details") {
                    TextField("Salary Range", text: $salary)
                    TextField("Job URL", text: $url)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                    
                    Picker("Status", selection: $status) {
                        ForEach(ApplicationStatus.allCases, id: \.self) { status in
                            Text(status.displayName).tag(status)
                        }
                    }
                    
                    Picker("Source", selection: $source) {
                        ForEach([ApplicationSource.manual, .linkedin, .indeed, .other], id: \.self) { source in
                            Text(source.displayName).tag(source)
                        }
                    }
                }
                
                Section("Notes") {
                    TextEditor(text: $notes)
                        .frame(height: 100)
                }
            }
            .navigationTitle("Add Application")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        // TODO: Save application
                        dismiss()
                    }
                    .disabled(companyName.isEmpty || roleTitle.isEmpty)
                }
            }
        }
    }
}

#Preview {
    AddApplicationView()
}
