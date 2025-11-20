//
//  DesignSystem.swift
//  JobTracker
//
//  Comprehensive design system for consistent, professional UI
//

import SwiftUI

// MARK: - Typography

struct Typography {
    // Display
    static let largeTitle = Font.system(size: 34, weight: .bold, design: .rounded)
    static let title1 = Font.system(size: 28, weight: .bold, design: .rounded)
    static let title2 = Font.system(size: 22, weight: .bold, design: .rounded)
    static let title3 = Font.system(size: 20, weight: .semibold, design: .rounded)
    
    // Body
    static let headline = Font.system(size: 17, weight: .semibold, design: .rounded)
    static let body = Font.system(size: 17, weight: .regular, design: .default)
    static let bodyBold = Font.system(size: 17, weight: .semibold, design: .default)
    static let callout = Font.system(size: 16, weight: .regular, design: .default)
    static let subheadline = Font.system(size: 15, weight: .regular, design: .default)
    static let subheadlineBold = Font.system(size: 15, weight: .semibold, design: .default)
    
    // Small
    static let footnote = Font.system(size: 13, weight: .regular, design: .default)
    static let footnoteBold = Font.system(size: 13, weight: .semibold, design: .default)
    static let caption1 = Font.system(size: 12, weight: .regular, design: .default)
    static let caption1Bold = Font.system(size: 12, weight: .semibold, design: .default)
    static let caption2 = Font.system(size: 11, weight: .regular, design: .default)
    static let caption2Bold = Font.system(size: 11, weight: .semibold, design: .default)
}

// MARK: - Colors

struct AppColors {
    // Primary
    static let primary = Color.blue
    static let primaryLight = Color.blue.opacity(0.1)
    static let primaryDark = Color(red: 0, green: 0.4, blue: 0.8)
    
    // Secondary
    static let secondary = Color.purple
    static let secondaryLight = Color.purple.opacity(0.1)
    
    // Semantic
    static let success = Color.green
    static let successLight = Color.green.opacity(0.1)
    static let warning = Color.orange
    static let warningLight = Color.orange.opacity(0.1)
    static let error = Color.red
    static let errorLight = Color.red.opacity(0.1)
    static let info = Color.blue
    static let infoLight = Color.blue.opacity(0.1)
    
    // Neutrals
    static let textPrimary = Color.primary
    static let textSecondary = Color.secondary
    static let textTertiary = Color(.systemGray)
    static let textDisabled = Color(.systemGray3)
    
    // Backgrounds
    static let background = Color(.systemBackground)
    static let backgroundSecondary = Color(.secondarySystemBackground)
    static let backgroundTertiary = Color(.tertiarySystemBackground)
    static let surface = Color(.systemBackground)
    static let surfaceElevated = Color(.systemBackground)
    
    // Borders
    static let border = Color(.systemGray5)
    static let borderLight = Color(.systemGray6)
    
    // Shadows
    static let shadowLight = Color.black.opacity(0.05)
    static let shadowMedium = Color.black.opacity(0.1)
    static let shadowHeavy = Color.black.opacity(0.15)
}

// MARK: - Spacing

struct Spacing {
    static let xxs: CGFloat = 4
    static let xs: CGFloat = 8
    static let s: CGFloat = 12
    static let m: CGFloat = 16
    static let l: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
    static let xxxl: CGFloat = 64
}

// MARK: - Corner Radius

struct CornerRadius {
    static let xs: CGFloat = 6
    static let s: CGFloat = 8
    static let m: CGFloat = 12
    static let l: CGFloat = 16
    static let xl: CGFloat = 20
    static let xxl: CGFloat = 24
    static let pill: CGFloat = 999
}

// MARK: - Shadows

struct Shadows {
    static let small = Shadow(
        color: AppColors.shadowLight,
        radius: 4,
        x: 0,
        y: 2
    )
    
    static let medium = Shadow(
        color: AppColors.shadowMedium,
        radius: 8,
        x: 0,
        y: 4
    )
    
    static let large = Shadow(
        color: AppColors.shadowMedium,
        radius: 12,
        x: 0,
        y: 6
    )
    
    static let card = Shadow(
        color: AppColors.shadowLight,
        radius: 10,
        x: 0,
        y: 4
    )
}

struct Shadow {
    let color: Color
    let radius: CGFloat
    let x: CGFloat
    let y: CGFloat
}

// MARK: - View Modifiers

struct CardModifier: ViewModifier {
    var padding: CGFloat = Spacing.m
    var cornerRadius: CGFloat = CornerRadius.l
    var shadow: Shadow = Shadows.card
    
    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .fill(AppColors.surface)
                    .shadow(
                        color: shadow.color,
                        radius: shadow.radius,
                        x: shadow.x,
                        y: shadow.y
                    )
            )
    }
}

struct PrimaryButtonStyle: ButtonStyle {
    var isEnabled: Bool = true
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Typography.headline)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .frame(height: 52)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.m)
                    .fill(isEnabled ? AppColors.primary : AppColors.textDisabled)
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .opacity(isEnabled ? 1.0 : 0.6)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

struct SecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Typography.headline)
            .foregroundColor(AppColors.primary)
            .frame(maxWidth: .infinity)
            .frame(height: 52)
            .background(
                RoundedRectangle(cornerRadius: CornerRadius.m)
                    .fill(AppColors.primaryLight)
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

struct ChipStyle: ViewModifier {
    var color: Color = AppColors.primary
    var isSelected: Bool = false
    
    func body(content: Content) -> some View {
        content
            .font(Typography.caption1Bold)
            .foregroundColor(isSelected ? .white : color)
            .padding(.horizontal, Spacing.s)
            .padding(.vertical: Spacing.xs)
            .background(
                Capsule()
                    .fill(isSelected ? color : color.opacity(0.1))
            )
    }
}

// MARK: - View Extensions

extension View {
    func cardStyle(
        padding: CGFloat = Spacing.m,
        cornerRadius: CGFloat = CornerRadius.l,
        shadow: Shadow = Shadows.card
    ) -> some View {
        modifier(CardModifier(padding: padding, cornerRadius: cornerRadius, shadow: shadow))
    }
    
    func chipStyle(color: Color = AppColors.primary, isSelected: Bool = false) -> some View {
        modifier(ChipStyle(color: color, isSelected: isSelected))
    }
}

// MARK: - Icon Sizes

struct IconSize {
    static let xs: CGFloat = 12
    static let s: CGFloat = 16
    static let m: CGFloat = 20
    static let l: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 40
}

// MARK: - Animation Presets

struct Animations {
    static let quick = Animation.easeInOut(duration: 0.2)
    static let standard = Animation.easeInOut(duration: 0.3)
    static let slow = Animation.easeInOut(duration: 0.5)
    static let spring = Animation.spring(response: 0.3, dampingFraction: 0.7)
    static let bouncy = Animation.spring(response: 0.4, dampingFraction: 0.6)
}
