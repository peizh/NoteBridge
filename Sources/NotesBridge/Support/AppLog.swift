import OSLog

enum AppLog {
    private static let subsystem = "dev.notesbridge.app"

    static let sync = Logger(subsystem: subsystem, category: "sync")
    static let appleNotes = Logger(subsystem: subsystem, category: "apple-notes")
    static let export = Logger(subsystem: subsystem, category: "export")
    static let access = Logger(subsystem: subsystem, category: "access")
}
