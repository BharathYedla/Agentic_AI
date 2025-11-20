//
//  SignUpView.swift
//  JobTracker
//
//  Beautiful sign-up screen with premium UI and password strength indicator
//

import SwiftUI

struct SignUpView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var appState: AppState
    
    @State private var fullName = ""
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var isPasswordVisible = false
    @State private var isConfirmPasswordVisible = false
    @State private var isLoading = false
    @State private var showError = false
    @State private var errorMessage = ""
    @State private var agreedToTerms = false
    
    @FocusState private var focusedField: Field?
    
    enum Field {
        case fullName, email, password, confirmPassword
    }
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [
                        Color.purple.opacity(0.1),
                        Color.blue.opacity(0.05)
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 32) {
                        // Header
                        VStack(spacing: 16) {
                            // Logo/Icon
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(
                                            colors: [.purple, .blue],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 80, height: 80)
                                
                                Image(systemName: "person.badge.plus.fill")
                                    .font(.system(size: 36))
                                    .foregroundColor(.white)
                            }
                            .padding(.top, 40)
                            
                            VStack(spacing: 8) {
                                Text("Create Account")
                                    .font(.system(size: 32, weight: .bold))
                                    .foregroundColor(.primary)
                                
                                Text("Start tracking your job applications today")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                                    .multilineTextAlignment(.center)
                                    .padding(.horizontal)
                            }
                        }
                        
                        // Form
                        VStack(spacing: 20) {
                            // Full Name Field
                            CustomTextField(
                                icon: "person.fill",
                                placeholder: "Full Name",
                                text: $fullName,
                                textContentType: .name
                            )
                            .focused($focusedField, equals: .fullName)
                            .submitLabel(.next)
                            .onSubmit {
                                focusedField = .email
                            }
                            
                            // Email Field
                            VStack(alignment: .leading, spacing: 8) {
                                CustomTextField(
                                    icon: "envelope.fill",
                                    placeholder: "Email",
                                    text: $email,
                                    keyboardType: .emailAddress,
                                    textContentType: .emailAddress
                                )
                                .focused($focusedField, equals: .email)
                                .submitLabel(.next)
                                .onSubmit {
                                    focusedField = .password
                                }
                                
                                // Email validation indicator
                                if !email.isEmpty {
                                    HStack(spacing: 6) {
                                        Image(systemName: User.isValidEmail(email) ? "checkmark.circle.fill" : "xmark.circle.fill")
                                            .font(.caption)
                                            .foregroundColor(User.isValidEmail(email) ? .green : .red)
                                        
                                        Text(User.isValidEmail(email) ? "Valid email" : "Invalid email format")
                                            .font(.caption)
                                            .foregroundColor(User.isValidEmail(email) ? .green : .red)
                                    }
                                    .padding(.leading, 4)
                                }
                            }
                            
                            // Password Field
                            VStack(alignment: .leading, spacing: 8) {
                                CustomSecureField(
                                    icon: "lock.fill",
                                    placeholder: "Password",
                                    text: $password,
                                    isVisible: $isPasswordVisible
                                )
                                .focused($focusedField, equals: .password)
                                .submitLabel(.next)
                                .onSubmit {
                                    focusedField = .confirmPassword
                                }
                                
                                // Password strength indicator
                                if !password.isEmpty {
                                    PasswordStrengthIndicator(password: password)
                                }
                            }
                            
                            // Confirm Password Field
                            VStack(alignment: .leading, spacing: 8) {
                                CustomSecureField(
                                    icon: "lock.fill",
                                    placeholder: "Confirm Password",
                                    text: $confirmPassword,
                                    isVisible: $isConfirmPasswordVisible
                                )
                                .focused($focusedField, equals: .confirmPassword)
                                .submitLabel(.go)
                                .onSubmit {
                                    Task {
                                        await signUp()
                                    }
                                }
                                
                                // Password match indicator
                                if !confirmPassword.isEmpty {
                                    HStack(spacing: 6) {
                                        Image(systemName: passwordsMatch ? "checkmark.circle.fill" : "xmark.circle.fill")
                                            .font(.caption)
                                            .foregroundColor(passwordsMatch ? .green : .red)
                                        
                                        Text(passwordsMatch ? "Passwords match" : "Passwords don't match")
                                            .font(.caption)
                                            .foregroundColor(passwordsMatch ? .green : .red)
                                    }
                                    .padding(.leading, 4)
                                }
                            }
                            
                            // Terms and Conditions
                            HStack(alignment: .top, spacing: 12) {
                                Button(action: { agreedToTerms.toggle() }) {
                                    Image(systemName: agreedToTerms ? "checkmark.square.fill" : "square")
                                        .font(.title3)
                                        .foregroundColor(agreedToTerms ? .blue : .secondary)
                                }
                                
                                VStack(alignment: .leading, spacing: 4) {
                                    Text("I agree to the ")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    + Text("Terms of Service")
                                        .font(.caption)
                                        .foregroundColor(.blue)
                                        .underline()
                                    + Text(" and ")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    + Text("Privacy Policy")
                                        .font(.caption)
                                        .foregroundColor(.blue)
                                        .underline()
                                }
                            }
                            .padding(.top, 8)
                        }
                        .padding(.horizontal, 24)
                        
                        // Sign Up Button
                        Button(action: {
                            Task {
                                await signUp()
                            }
                        }) {
                            HStack(spacing: 12) {
                                if isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                } else {
                                    Text("Create Account")
                                        .font(.headline)
                                }
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(
                                LinearGradient(
                                    colors: [.purple, .blue],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(16)
                            .shadow(color: .purple.opacity(0.3), radius: 8, x: 0, y: 4)
                        }
                        .disabled(isLoading || !isFormValid)
                        .opacity(isFormValid ? 1.0 : 0.6)
                        .padding(.horizontal, 24)
                        
                        // Divider
                        HStack(spacing: 16) {
                            Rectangle()
                                .fill(Color.gray.opacity(0.3))
                                .frame(height: 1)
                            
                            Text("OR")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            Rectangle()
                                .fill(Color.gray.opacity(0.3))
                                .frame(height: 1)
                        }
                        .padding(.horizontal, 24)
                        
                        // Social Sign Up (Future)
                        VStack(spacing: 12) {
                            SocialSignInButton(
                                icon: "apple.logo",
                                title: "Continue with Apple",
                                color: .black
                            ) {
                                // TODO: Implement Apple Sign In
                            }
                            
                            SocialSignInButton(
                                icon: "g.circle.fill",
                                title: "Continue with Google",
                                color: .red
                            ) {
                                // TODO: Implement Google Sign In
                            }
                        }
                        .padding(.horizontal, 24)
                        
                        // Sign In Link
                        HStack(spacing: 4) {
                            Text("Already have an account?")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                            
                            Button(action: {
                                dismiss()
                                // Parent view will show sign in
                            }) {
                                Text("Sign In")
                                    .font(.subheadline)
                                    .fontWeight(.semibold)
                                    .foregroundColor(.blue)
                            }
                        }
                        .padding(.bottom, 32)
                    }
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: { dismiss() }) {
                        Image(systemName: "xmark.circle.fill")
                            .font(.title3)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .alert("Error", isPresented: $showError) {
                Button("OK", role: .cancel) {}
            } message: {
                Text(errorMessage)
            }
        }
    }
    
    // MARK: - Computed Properties
    
    private var isFormValid: Bool {
        !fullName.isEmpty &&
        User.isValidEmail(email) &&
        User.isValidPassword(password) &&
        passwordsMatch &&
        agreedToTerms
    }
    
    private var passwordsMatch: Bool {
        password == confirmPassword
    }
    
    // MARK: - Methods
    
    private func signUp() async {
        // Dismiss keyboard
        focusedField = nil
        
        // Haptic feedback
        let impact = UIImpactFeedbackGenerator(style: .medium)
        impact.impactOccurred()
        
        isLoading = true
        
        do {
            try await appState.signUp(
                email: email,
                password: password,
                fullName: fullName
            )
            
            // Success haptic
            let success = UINotificationFeedbackGenerator()
            success.notificationOccurred(.success)
            
            // Dismiss view
            dismiss()
            
        } catch {
            // Error haptic
            let errorHaptic = UINotificationFeedbackGenerator()
            errorHaptic.notificationOccurred(.error)
            
            errorMessage = error.localizedDescription
            showError = true
        }
        
        isLoading = false
    }
}

// MARK: - Password Strength Indicator

struct PasswordStrengthIndicator: View {
    let password: String
    
    private var strength: PasswordStrength {
        User.passwordStrength(password)
    }
    
    private var strengthColor: Color {
        switch strength {
        case .weak: return .red
        case .medium: return .orange
        case .strong: return .green
        }
    }
    
    private var strengthProgress: CGFloat {
        switch strength {
        case .weak: return 0.33
        case .medium: return 0.66
        case .strong: return 1.0
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Progress bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 2)
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 4)
                    
                    RoundedRectangle(cornerRadius: 2)
                        .fill(strengthColor)
                        .frame(width: geometry.size.width * strengthProgress, height: 4)
                        .animation(.easeInOut, value: strengthProgress)
                }
            }
            .frame(height: 4)
            
            // Strength label
            HStack(spacing: 6) {
                Image(systemName: "lock.shield.fill")
                    .font(.caption)
                    .foregroundColor(strengthColor)
                
                Text("Password strength: \(strength.text)")
                    .font(.caption)
                    .foregroundColor(strengthColor)
            }
            
            // Requirements
            if strength != .strong {
                VStack(alignment: .leading, spacing: 4) {
                    PasswordRequirement(
                        text: "At least 8 characters",
                        isMet: password.count >= 8
                    )
                    
                    PasswordRequirement(
                        text: "Contains uppercase letter",
                        isMet: password.rangeOfCharacter(from: .uppercaseLetters) != nil
                    )
                    
                    PasswordRequirement(
                        text: "Contains lowercase letter",
                        isMet: password.rangeOfCharacter(from: .lowercaseLetters) != nil
                    )
                    
                    PasswordRequirement(
                        text: "Contains number",
                        isMet: password.rangeOfCharacter(from: .decimalDigits) != nil
                    )
                }
                .padding(.top, 4)
            }
        }
        .padding(.leading, 4)
    }
}

// MARK: - Password Requirement

struct PasswordRequirement: View {
    let text: String
    let isMet: Bool
    
    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: isMet ? "checkmark.circle.fill" : "circle")
                .font(.caption2)
                .foregroundColor(isMet ? .green : .secondary)
            
            Text(text)
                .font(.caption2)
                .foregroundColor(isMet ? .green : .secondary)
        }
    }
}

// MARK: - Preview

#Preview {
    SignUpView()
        .environmentObject(AppState())
}
