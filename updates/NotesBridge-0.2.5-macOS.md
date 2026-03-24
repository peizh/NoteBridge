<!-- sparkle-sign-warning:
IMPORTANT: This file was signed by Sparkle. Any modifications to this file requires updating signatures in appcasts that reference this file! This will involve re-running generate_appcast or sign_update.
-->
## [0.2.5] - 2026-03-24

### Fixed

- Fixed the direct-download update pipeline by rotating the Sparkle signing key and restoring GitHub Pages appcast publishing.
- Fixed release automation so Sparkle framework lookup and release-note extraction succeed on clean CI runners.

### Important

- NotesBridge `0.2.2` to `0.2.4` were built with the previous Sparkle public key and cannot automatically upgrade to this release.
- Users on those versions need to manually install `0.2.5` once. After that, in-app updates can work again.

### Distribution

- Direct-download build.
- Ad-hoc signed.
- Not notarized yet.
