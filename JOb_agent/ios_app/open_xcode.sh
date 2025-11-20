#!/bin/bash

# JobTracker - Quick Xcode Setup Script

echo "🚀 JobTracker - Xcode Setup"
echo "=========================="
echo ""

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode is not installed"
    echo "   Please install Xcode from the App Store"
    exit 1
fi

echo "✅ Xcode is installed"
echo ""

# Navigate to ios_app directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo ""

# Check if project exists
if [ -f "JobTracker.xcodeproj/project.pbxproj" ]; then
    echo "✅ Xcode project found!"
    echo "   Opening Xcode..."
    open JobTracker.xcodeproj
    exit 0
fi

echo "⚠️  Xcode project not found"
echo ""
echo "📝 To create the Xcode project:"
echo ""
echo "1. Open Xcode"
echo "2. File → New → Project"
echo "3. Choose: iOS → App"
echo "4. Product Name: JobTracker"
echo "5. Interface: SwiftUI"
echo "6. Language: Swift"
echo "7. Save in: $(pwd)"
echo ""
echo "8. Delete default files (ContentView.swift, JobTrackerApp.swift)"
echo "9. Right-click JobTracker folder → Add Files..."
echo "10. Select all folders in JobTracker/ directory"
echo "11. Uncheck 'Copy items if needed'"
echo "12. Click Add"
echo ""
echo "13. Select simulator: iPhone 15 Pro"
echo "14. Press ⌘R to run!"
echo ""
echo "📖 Full guide: HOW_TO_RUN_XCODE.md"
echo ""
echo "🎯 Quick start:"
echo "   1. Open Xcode from Applications"
echo "   2. Create new iOS App project named 'JobTracker'"
echo "   3. Save it in: $(pwd)"
echo "   4. Add existing files from JobTracker/ folder"
echo "   5. Run with ⌘R"
echo ""
echo "💡 Need help? Check HOW_TO_RUN_XCODE.md for detailed instructions"
