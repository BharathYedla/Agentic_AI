import SwiftUI

struct SignInView: View {
    @StateObject private var authService = AuthService.shared
    @State private var email = ""
    @State private var password = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Welcome Back")
                .font(DesignSystem.Typography.largeTitle)
            
            TextField("Email", text: $email)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .autocapitalization(.none)
            
            SecureField("Password", text: $password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
            
            if let error = errorMessage {
                Text(error)
                    .foregroundColor(.red)
            }
            
            Button(action: signIn) {
                if isLoading {
                    ProgressView()
                } else {
                    Text("Sign In")
                        .frame(maxWidth: .infinity)
                }
            }
            .primaryButton()
            .disabled(isLoading)
        }
        .padding()
    }
    
    private func signIn() {
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                try await authService.signIn(email: email, password: password)
            } catch {
                errorMessage = error.localizedDescription
            }
            isLoading = false
        }
    }
}
