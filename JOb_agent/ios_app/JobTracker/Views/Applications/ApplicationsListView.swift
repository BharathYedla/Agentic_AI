//
//  ApplicationsListView.swift
//  JobTracker
//
//  Applications list view - Placeholder for Phase 3
//

import SwiftUI

struct ApplicationsListView: View {
    @StateObject private var viewModel = ApplicationsListViewModel()
    @State private var showingAddApplication = false
    @State private var searchText = ""
    @State private var selectedStatus: ApplicationStatus?
    
    var body: some View {
        NavigationView {
            ZStack {
                if viewModel.applications.isEmpty {
                    EmptyStateView(
                        icon: "doc.text",
                        title: "No Applications Yet",
                        description: "Start tracking your job applications by adding your first one"
                    )
                } else {
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(filteredApplications) { application in
                                NavigationLink(destination: ApplicationDetailView(application: application)) {
                                    ApplicationRowView(application: application)
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle("Applications")
            .searchable(text: $searchText, prompt: "Search applications")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showingAddApplication = true }) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                            .foregroundColor(.blue)
                    }
                }
            }
            .sheet(isPresented: $showingAddApplication) {
                AddApplicationView()
            }
            .onAppear {
                Task {
                    await viewModel.loadApplications()
                }
            }
        }
    }
    
    private var filteredApplications: [JobApplication] {
        viewModel.applications.filter { application in
            let matchesSearch = searchText.isEmpty ||
                application.companyName.localizedCaseInsensitiveContains(searchText) ||
                application.roleTitle.localizedCaseInsensitiveContains(searchText)
            
            let matchesStatus = selectedStatus == nil || application.status == selectedStatus
            
            return matchesSearch && matchesStatus
        }
    }
}

@MainActor
class ApplicationsListViewModel: ObservableObject {
    @Published var applications: [JobApplication] = []
    @Published var isLoading = false
    
    func loadApplications() async {
        isLoading = true
        
        // TODO: Replace with actual API call
        try? await Task.sleep(nanoseconds: 500_000_000)
        applications = JobApplication.sampleData
        
        isLoading = false
    }
}

#Preview {
    ApplicationsListView()
}
