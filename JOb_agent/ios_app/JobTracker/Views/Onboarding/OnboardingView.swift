//
//  OnboardingView.swift
//  JobTracker
//
//  Beautiful onboarding experience
//

import SwiftUI

struct OnboardingView: View {
    @State private var currentPage = 0
    @State private var showingSignIn = false
    @State private var showingSignUp = false
    
    private let pages: [OnboardingPage] = [
        OnboardingPage(
            title: "Track Every Application",
            description: "Never lose track of your job applications again. AI-powered email analysis keeps everything organized.",
            imageName: "doc.text.magnifyingglass",
            color: .blue
        ),
        OnboardingPage(
            title: "Smart Email Analysis",
            description: "Our AI automatically reads your emails and extracts company names, roles, and application status.",
            imageName: "envelope.badge.shield.half.filled",
            color: .purple
        ),
        OnboardingPage(
            title: "Beautiful Insights",
            description: "Get powerful analytics about your job search. Track interview rates, response times, and more.",
            imageName: "chart.line.uptrend.xyaxis",
            color: .green
        ),
        OnboardingPage(
            title: "Stay Organized",
            description: "Manage interviews, deadlines, and follow-ups all in one place. Never miss an opportunity.",
            imageName: "calendar.badge.checkmark",
            color: .orange
        )
    ]
    
    var body: some View {
        ZStack {
            // Background gradient
            LinearGradient(
                colors: [
                    pages[currentPage].color.opacity(0.1),
                    pages[currentPage].color.opacity(0.05)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Page content
                TabView(selection: $currentPage) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        OnboardingPageView(page: pages[index])
                            .tag(index)
                    }
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
                .animation(.easeInOut, value: currentPage)
                
                // Custom page indicator
                HStack(spacing: 8) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        Circle()
                            .fill(currentPage == index ? pages[currentPage].color : Color.gray.opacity(0.3))
                            .frame(width: currentPage == index ? 10 : 8, height: currentPage == index ? 10 : 8)
                            .animation(.spring(), value: currentPage)
                    }
                }
                .padding(.bottom, 30)
                
                // Action buttons
                VStack(spacing: 16) {
                    if currentPage == pages.count - 1 {
                        // Last page - show sign up/sign in
                        Button(action: { showingSignUp = true }) {
                            Text("Get Started")
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 56)
                                .background(pages[currentPage].color)
                                .cornerRadius(16)
                        }
                        .buttonStyle(ScaleButtonStyle())
                        
                        Button(action: { showingSignIn = true }) {
                            Text("I already have an account")
                                .font(.subheadline)
                                .foregroundColor(pages[currentPage].color)
                        }
                    } else {
                        // Next button
                        Button(action: { withAnimation { currentPage += 1 } }) {
                            Text("Continue")
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 56)
                                .background(pages[currentPage].color)
                                .cornerRadius(16)
                        }
                        .buttonStyle(ScaleButtonStyle())
                        
                        Button(action: { withAnimation { currentPage = pages.count - 1 } }) {
                            Text("Skip")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 40)
            }
        }
        .sheet(isPresented: $showingSignUp) {
            SignUpView()
        }
        .sheet(isPresented: $showingSignIn) {
            SignInView()
        }
    }
}

// MARK: - Onboarding Page View

struct OnboardingPageView: View {
    let page: OnboardingPage
    
    var body: some View {
        VStack(spacing: 32) {
            Spacer()
            
            // Icon
            ZStack {
                Circle()
                    .fill(page.color.opacity(0.1))
                    .frame(width: 140, height: 140)
                
                Image(systemName: page.imageName)
                    .font(.system(size: 60, weight: .medium))
                    .foregroundColor(page.color)
            }
            .padding(.top, 60)
            
            // Text content
            VStack(spacing: 16) {
                Text(page.title)
                    .font(.system(size: 32, weight: .bold))
                    .multilineTextAlignment(.center)
                    .foregroundColor(.primary)
                
                Text(page.description)
                    .font(.system(size: 17))
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                    .padding(.horizontal, 32)
                    .fixedSize(horizontal: false, vertical: true)
            }
            
            Spacer()
        }
    }
}

// MARK: - Models

struct OnboardingPage {
    let title: String
    let description: String
    let imageName: String
    let color: Color
}

// MARK: - Button Styles

struct ScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .animation(.easeInOut(duration: 0.2), value: configuration.isPressed)
    }
}

// MARK: - Preview

#Preview {
    OnboardingView()
}
