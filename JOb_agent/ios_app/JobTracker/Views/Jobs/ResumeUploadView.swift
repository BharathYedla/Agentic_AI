//
//  ResumeUploadView.swift
//  JobTracker
//
//  Resume upload view with document picker
//

import SwiftUI
import UniformTypeIdentifiers

struct ResumeUploadView: View {
    @ObservedObject var viewModel: JobsViewModel
    @Environment(\.dismiss) var dismiss
    
    @State private var showingDocumentPicker = false
    @State private var isUploading = false
    @State private var uploadProgress: Double = 0
    @State private var showError = false
    @State private var errorMessage = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: Spacing.xl) {
                Spacer()
                
                // Icon
                ZStack {
                    Circle()
                        .fill(
                            LinearGradient(
                                colors: [AppColors.primary.opacity(0.2), AppColors.secondary.opacity(0.2)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 120, height: 120)
                    
                    Image(systemName: "doc.text.fill")
                        .font(.system(size: 50))
                        .foregroundColor(AppColors.primary)
                }
                
                // Text
                VStack(spacing: Spacing.s) {
                    Text("Upload Your Resume")
                        .font(Typography.title2)
                        .foregroundColor(AppColors.textPrimary)
                    
                    Text("Get personalized job recommendations based on your skills and experience")
                        .font(Typography.body)
                        .foregroundColor(AppColors.textSecondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, Spacing.xl)
                }
                
                // Upload Progress
                if isUploading {
                    VStack(spacing: Spacing.s) {
                        ProgressView(value: uploadProgress)
                            .progressViewStyle(LinearProgressViewStyle())
                            .padding(.horizontal, Spacing.xl)
                        
                        Text("Uploading and analyzing your resume...")
                            .font(Typography.caption1)
                            .foregroundColor(AppColors.textSecondary)
                    }
                }
                
                Spacer()
                
                // Upload Button
                VStack(spacing: Spacing.m) {
                    Button(action: { showingDocumentPicker = true }) {
                        HStack(spacing: Spacing.s) {
                            Image(systemName: "arrow.up.doc.fill")
                                .font(.system(size: IconSize.m))
                            
                            Text("Choose File")
                                .font(Typography.headline)
                        }
                    }
                    .buttonStyle(PrimaryButtonStyle(isEnabled: !isUploading))
                    .disabled(isUploading)
                    
                    Text("Supported formats: PDF, DOC, DOCX")
                        .font(Typography.caption1)
                        .foregroundColor(AppColors.textTertiary)
                }
                .padding(Spacing.m)
            }
            .navigationTitle("Upload Resume")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .disabled(isUploading)
                }
            }
            .sheet(isPresented: $showingDocumentPicker) {
                DocumentPicker { url in
                    Task {
                        await uploadResume(from: url)
                    }
                }
            }
            .alert("Upload Error", isPresented: $showError) {
                Button("OK", role: .cancel) {}
            } message: {
                Text(errorMessage)
            }
        }
    }
    
    private func uploadResume(from url: URL) async {
        isUploading = true
        uploadProgress = 0
        
        do {
            // Start accessing security-scoped resource
            guard url.startAccessingSecurityScopedResource() else {
                throw NSError(domain: "FileAccess", code: -1, userInfo: [NSLocalizedDescriptionKey: "Cannot access file"])
            }
            defer { url.stopAccessingSecurityScopedResource() }
            
            // Read file data
            let fileData = try Data(contentsOf: url)
            let fileName = url.lastPathComponent
            
            // Simulate progress
            for i in 1...3 {
                uploadProgress = Double(i) / 3.0
                try await Task.sleep(nanoseconds: 300_000_000) // 0.3 seconds
            }
            
            // Upload to backend
            try await viewModel.uploadResume(fileData: fileData, fileName: fileName)
            
            uploadProgress = 1.0
            
            // Success - dismiss
            dismiss()
            
        } catch {
            errorMessage = error.localizedDescription
            showError = true
        }
        
        isUploading = false
    }
}

// MARK: - Document Picker

struct DocumentPicker: UIViewControllerRepresentable {
    let onPick: (URL) -> Void
    
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(
            forOpeningContentTypes: [
                UTType.pdf,
                UTType(filenameExtension: "doc")!,
                UTType(filenameExtension: "docx")!
            ]
        )
        picker.delegate = context.coordinator
        picker.allowsMultipleSelection = false
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(onPick: onPick)
    }
    
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let onPick: (URL) -> Void
        
        init(onPick: @escaping (URL) -> Void) {
            self.onPick = onPick
        }
        
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            onPick(url)
        }
    }
}

#Preview {
    ResumeUploadView(viewModel: JobsViewModel())
}
