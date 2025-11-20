//
//  JobDetailView.swift
//  JobTracker
//
//  Detailed job view with realistic LinkedIn-style UI
//

import SwiftUI

struct JobDetailView: View {
    let job: JobRecommendation
    @ObservedObject var viewModel: JobsViewModel
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: Spacing.l) {
                    // Company Header
                    CompanyHeader(job: job)
                    
                    Divider()
                    
                    // Job Title and Match Score
                    VStack(alignment: .leading, spacing: Spacing.s) {
                        Text(job.title)
                            .font(Typography.title2)
                            .foregroundColor(AppColors.textPrimary)
                        
                        if job.matchScore > 0 {
                            MatchScoreBadge(score: job.matchScore)
                        }
                    }
                    
                    // Job Meta Info
                    JobMetaInfo(job: job)
                    
                    Divider()
                    
                    // Match Reasons (if available)
                    if !job.matchReasons.isEmpty {
                        VStack(alignment: .leading, spacing: Spacing.s) {
                            Text("Why you're a great fit")
                                .font(Typography.headline)
                                .foregroundColor(AppColors.textPrimary)
                            
                            ForEach(job.matchReasons, id: \.self) { reason in
                                HStack(alignment: .top, spacing: Spacing.s) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .font(.system(size: IconSize.m))
                                        .foregroundColor(AppColors.success)
                                    
                                    Text(reason)
                                        .font(Typography.subheadline)
                                        .foregroundColor(AppColors.textSecondary)
                                }
                            }
                        }
                        
                        Divider()
                    }
                    
                    // Job Description
                    VStack(alignment: .leading, spacing: Spacing.s) {
                        Text("About the role")
                            .font(Typography.headline)
                            .foregroundColor(AppColors.textPrimary)
                        
                        Text(job.description)
                            .font(Typography.body)
                            .foregroundColor(AppColors.textSecondary)
                            .lineSpacing(4)
                    }
                    
                    // Requirements
                    if !job.requirements.isEmpty {
                        Divider()
                        
                        VStack(alignment: .leading, spacing: Spacing.s) {
                            Text("Requirements")
                                .font(Typography.headline)
                                .foregroundColor(AppColors.textPrimary)
                            
                            ForEach(job.requirements, id: \.self) { requirement in
                                HStack(alignment: .top, spacing: Spacing.s) {
                                    Text("•")
                                        .font(Typography.body)
                                        .foregroundColor(AppColors.textSecondary)
                                    
                                    Text(requirement)
                                        .font(Typography.body)
                                        .foregroundColor(AppColors.textSecondary)
                                }
                            }
                        }
                    }
                    
                    // Skills
                    if !job.skills.isEmpty {
                        Divider()
                        
                        VStack(alignment: .leading, spacing: Spacing.s) {
                            Text("Skills")
                                .font(Typography.headline)
                                .foregroundColor(AppColors.textPrimary)
                            
                            FlowLayout(spacing: Spacing.xs) {
                                ForEach(job.skills, id: \.self) { skill in
                                    Text(skill)
                                        .chipStyle(color: AppColors.primary)
                                }
                            }
                        }
                    }
                    
                    // Benefits
                    if !job.benefits.isEmpty {
                        Divider()
                        
                        VStack(alignment: .leading, spacing: Spacing.s) {
                            Text("Benefits")
                                .font(Typography.headline)
                                .foregroundColor(AppColors.textPrimary)
                            
                            ForEach(job.benefits, id: \.self) { benefit in
                                HStack(alignment: .top, spacing: Spacing.s) {
                                    Image(systemName: "star.fill")
                                        .font(.system(size: IconSize.s))
                                        .foregroundColor(AppColors.warning)
                                    
                                    Text(benefit)
                                        .font(Typography.body)
                                        .foregroundColor(AppColors.textSecondary)
                                }
                            }
                        }
                    }
                }
                .padding(Spacing.m)
            }
            .navigationTitle("Job Details")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: { dismiss() }) {
                        Image(systemName: "xmark.circle.fill")
                            .font(.system(size: IconSize.l))
                            .foregroundColor(AppColors.textSecondary)
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        Task {
                            await viewModel.toggleSaveJob(job)
                        }
                    }) {
                        Image(systemName: job.isSaved ? "bookmark.fill" : "bookmark")
                            .font(.system(size: IconSize.l))
                            .foregroundColor(job.isSaved ? AppColors.primary : AppColors.textSecondary)
                    }
                }
            }
            .safeAreaInset(edge: .bottom) {
                // Apply Button
                Button(action: {
                    if let url = URL(string: job.applicationUrl) {
                        UIApplication.shared.open(url)
                    }
                }) {
                    HStack(spacing: Spacing.xs) {
                        Text("Apply on \(job.company)")
                            .font(Typography.headline)
                        
                        Image(systemName: "arrow.up.right")
                            .font(.system(size: IconSize.s))
                    }
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .frame(height: 52)
                    .background(AppColors.primary)
                    .cornerRadius(CornerRadius.m)
                }
                .padding(Spacing.m)
                .background(AppColors.background.ignoresSafeArea())
            }
        }
    }
}

// MARK: - Company Header

struct CompanyHeader: View {
    let job: JobRecommendation
    
    var body: some View {
        HStack(spacing: Spacing.m) {
            // Company Logo
            if let logoUrl = job.companyLogo, let url = URL(string: logoUrl) {
                AsyncImage(url: url) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                } placeholder: {
                    CompanyLogoPlaceholder(company: job.company)
                }
                .frame(width: 60, height: 60)
                .clipShape(RoundedRectangle(cornerRadius: CornerRadius.m))
            } else {
                CompanyLogoPlaceholder(company: job.company)
                    .frame(width: 60, height: 60)
            }
            
            VStack(alignment: .leading, spacing: Spacing.xxs) {
                Text(job.company)
                    .font(Typography.title3)
                    .foregroundColor(AppColors.textPrimary)
                
                Text(job.location)
                    .font(Typography.subheadline)
                    .foregroundColor(AppColors.textSecondary)
                
                HStack(spacing: Spacing.xxs) {
                    Image(systemName: job.locationType.icon)
                        .font(.system(size: IconSize.s))
                    Text(job.locationType.displayName)
                        .font(Typography.caption1)
                }
                .foregroundColor(AppColors.textTertiary)
            }
            
            Spacer()
        }
    }
}

// MARK: - Job Meta Info

struct JobMetaInfo: View {
    let job: JobRecommendation
    
    var body: some View {
        VStack(spacing: Spacing.s) {
            // Salary
            if let salary = job.salary {
                MetaRow(
                    icon: "dollarsign.circle.fill",
                    iconColor: AppColors.success,
                    title: "Salary",
                    value: salary.displayString
                )
            }
            
            // Experience Level
            MetaRow(
                icon: "chart.bar.fill",
                iconColor: AppColors.info,
                title: "Experience",
                value: job.experienceLevel.displayName
            )
            
            // Employment Type
            MetaRow(
                icon: "briefcase.fill",
                iconColor: AppColors.primary,
                title: "Type",
                value: job.employmentType.displayName
            )
            
            // Posted Date
            MetaRow(
                icon: "clock.fill",
                iconColor: AppColors.textTertiary,
                title: "Posted",
                value: job.postedDate.timeAgoDisplay()
            )
        }
    }
}

struct MetaRow: View {
    let icon: String
    let iconColor: Color
    let title: String
    let value: String
    
    var body: some View {
        HStack(spacing: Spacing.m) {
            ZStack {
                Circle()
                    .fill(iconColor.opacity(0.1))
                    .frame(width: 36, height: 36)
                
                Image(systemName: icon)
                    .font(.system(size: IconSize.m))
                    .foregroundColor(iconColor)
            }
            
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(Typography.caption1)
                    .foregroundColor(AppColors.textTertiary)
                
                Text(value)
                    .font(Typography.subheadlineBold)
                    .foregroundColor(AppColors.textPrimary)
            }
            
            Spacer()
        }
    }
}

// MARK: - Flow Layout for Skills

struct FlowLayout: Layout {
    var spacing: CGFloat = 8
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = FlowResult(
            in: proposal.replacingUnspecifiedDimensions().width,
            subviews: subviews,
            spacing: spacing
        )
        return result.size
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = FlowResult(
            in: bounds.width,
            subviews: subviews,
            spacing: spacing
        )
        for (index, subview) in subviews.enumerated() {
            subview.place(at: CGPoint(x: bounds.minX + result.positions[index].x,
                                     y: bounds.minY + result.positions[index].y),
                         proposal: .unspecified)
        }
    }
    
    struct FlowResult {
        var size: CGSize = .zero
        var positions: [CGPoint] = []
        
        init(in maxWidth: CGFloat, subviews: Subviews, spacing: CGFloat) {
            var x: CGFloat = 0
            var y: CGFloat = 0
            var lineHeight: CGFloat = 0
            
            for subview in subviews {
                let size = subview.sizeThatFits(.unspecified)
                
                if x + size.width > maxWidth && x > 0 {
                    x = 0
                    y += lineHeight + spacing
                    lineHeight = 0
                }
                
                positions.append(CGPoint(x: x, y: y))
                lineHeight = max(lineHeight, size.height)
                x += size.width + spacing
            }
            
            self.size = CGSize(width: maxWidth, height: y + lineHeight)
        }
    }
}

#Preview {
    JobDetailView(
        job: JobRecommendation.sampleData[0],
        viewModel: JobsViewModel()
    )
}
