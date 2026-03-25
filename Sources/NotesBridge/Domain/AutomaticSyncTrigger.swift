import Foundation

enum AutomaticSyncTrigger: String, Codable, CaseIterable, Identifiable, Sendable {
    case periodic
    case onChange

    var id: String { rawValue }

    var displayKey: String {
        switch self {
        case .periodic:
            "Periodic"
        case .onChange:
            "On Change"
        }
    }
}
