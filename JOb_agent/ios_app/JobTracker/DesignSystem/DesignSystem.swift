import SwiftUI

struct DesignSystem {
    struct Colors {
        static let primary = Color.blue
        static let secondary = Color.gray
        
        // Neutrals
        static let textPrimary = Color.primary
        static let textSecondary = Color.secondary
        static let textTertiary = Color(UIColor.systemGray)
        static let textDisabled = Color(UIColor.systemGray3)
        
        // Backgrounds
        static let background = Color(UIColor.systemBackground)
        static let backgroundSecondary = Color(UIColor.secondarySystemBackground)
        static let backgroundTertiary = Color(UIColor.tertiarySystemBackground)
        static let surface = Color(UIColor.systemBackground)
        static let surfaceElevated = Color(UIColor.systemBackground)
        
        // Borders
        static let border = Color(UIColor.systemGray5)
        static let borderLight = Color(UIColor.systemGray6)
        
        // Semantic
        static let error = Color.red
        static let success = Color.green
        static let warning = Color.orange
        static let info = Color.blue
        
        // Shadows
        static let shadowLight = Color.black.opacity(0.05)
        static let shadowMedium = Color.black.opacity(0.1)
        static let shadowHeavy = Color.black.opacity(0.15)
        
        // Legacy aliases (for compatibility)
        static let text = textPrimary
    }
    
    struct Typography {
        static let largeTitle = Font.largeTitle.bold()
        static let title = Font.title.bold()
        static let headline = Font.headline.weight(.semibold)
        static let body = Font.body
        static let caption = Font.caption
    }
    
    struct Spacing {
        static let small: CGFloat = 8
        static let medium: CGFloat = 16
        static let large: CGFloat = 24
        static let xLarge: CGFloat = 32
    }
    
    struct CornerRadius {
        static let small: CGFloat = 8
        static let medium: CGFloat = 12
        static let large: CGFloat = 16
    }
}

// Common View Modifiers
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding()
            .background(DesignSystem.Colors.primary)
            .foregroundColor(.white)
            .cornerRadius(DesignSystem.CornerRadius.medium)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}

extension View {
    func primaryButton() -> some View {
        self.buttonStyle(PrimaryButtonStyle())
    }
}
