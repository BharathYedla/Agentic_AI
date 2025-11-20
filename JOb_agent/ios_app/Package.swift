// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "JobTracker",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "JobTracker",
            targets: ["JobTracker"])
    ],
    targets: [
        .target(
            name: "JobTracker",
            path: "JobTracker")
    ]
)
