// swift-tools-version: 6.2
import PackageDescription
import Foundation

private func resolvedTestingFrameworksPath() -> String {
    let fileManager = FileManager.default
    let candidates = [
        ProcessInfo.processInfo.environment["DEVELOPER_DIR"]
            .map { "\($0)/Platforms/MacOSX.platform/Developer/Library/Frameworks" },
        "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/Library/Frameworks",
        "/Library/Developer/CommandLineTools/Library/Developer/Frameworks",
    ].compactMap { $0 }

    return candidates.first(where: { fileManager.fileExists(atPath: "\($0)/Testing.framework") })
        ?? "/Library/Developer/CommandLineTools/Library/Developer/Frameworks"
}

let testingFrameworksDirectory = resolvedTestingFrameworksPath()

let package = Package(
    name: "NotesBridge",
    platforms: [
        .macOS(.v14),
    ],
    products: [
        .executable(
            name: "NotesBridge",
            targets: ["NotesBridge"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/scinfu/SwiftSoup.git", exact: "2.9.6"),
        .package(url: "https://github.com/sparkle-project/Sparkle.git", exact: "2.9.0"),
    ],
    targets: [
        .executableTarget(
            name: "NotesBridge",
            dependencies: [
                .product(name: "SwiftSoup", package: "SwiftSoup"),
                .product(name: "Sparkle", package: "Sparkle"),
            ]
        ),
        .testTarget(
            name: "NotesBridgeTests",
            dependencies: ["NotesBridge"],
            swiftSettings: [
                .unsafeFlags([
                    "-F\(testingFrameworksDirectory)",
                    "-I\(testingFrameworksDirectory)",
                ]),
            ],
            linkerSettings: [
                .unsafeFlags([
                    "-F\(testingFrameworksDirectory)",
                    "-Xlinker",
                    "-rpath",
                    "-Xlinker",
                    testingFrameworksDirectory,
                ]),
            ]
        ),
    ]
)
