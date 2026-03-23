import Foundation

enum AutomaticSyncInterval: Int, Codable, CaseIterable, Identifiable, Sendable {
    case thirtyMinutes = 30
    case oneHour = 60
    case sixHours = 360
    case oneDay = 1440

    var id: Int { rawValue }

    var minutes: Int { rawValue }

    var displayKey: String {
        switch self {
        case .thirtyMinutes:
            return "Every 30 minutes"
        case .oneHour:
            return "Every hour"
        case .sixHours:
            return "Every 6 hours"
        case .oneDay:
            return "Every day"
        }
    }
}
