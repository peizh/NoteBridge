# Repository Guidelines

## Project Structure & Module Organization
`Sources/NotesBridge/` contains the macOS app code, grouped by responsibility: `App/`, `Domain/`, `Interaction/`, `Services/`, `Support/`, and `Views/`. Swift tests live in `Tests/NotesBridgeTests/` and generally mirror the production type they cover, for example `MarkdownTransformerTests.swift`. Build, packaging, and release helpers live in `scripts/`, with `notesbridge.sh` as the main entry point. Static brand assets live in `images/`, the marketing site lives in `site/`, and longer-form internal docs live in `docs/`.

## Build, Test, and Development Commands
Use the bundled app flow for normal macOS development:

```bash
./scripts/notesbridge.sh dev
./scripts/notesbridge.sh dev --build-only
swift run
swift test
xcodebuild -scheme NotesBridge -workspace .swiftpm/xcode/package.xcworkspace -destination 'platform=macOS' test
```

`./scripts/notesbridge.sh dev` builds, signs, and launches a real `.app`, which is required for permission-sensitive behavior like Accessibility. `swift run` is only for fast executable-only checks. Use `./scripts/notesbridge.sh bundle`, `./scripts/notesbridge.sh release`, and `./scripts/notesbridge.sh release-notes <version>` for packaging and release work.

## Coding Style & Naming Conventions
Follow existing Swift naming: `UpperCamelCase` for types, `lowerCamelCase` for methods and properties, and one primary type per file named after that type. Keep modules explicit and low-complexity; prefer small services over shared utility buckets. Keep shell scripts simple and explicit as well; `scripts/notesbridge.sh` is the canonical workflow entry point and should stay readable and subcommand-driven.

## Testing Guidelines
Add or update Swift tests for every behavior change. Prefer focused unit tests beside the affected subsystem, and keep UI-style coverage in files such as `NotesBridgeUITests.swift`. Run both `swift test` and the `xcodebuild ... test` command before opening a PR.
After agent-run test command passes successfully, launch the bundled app with `./scripts/notesbridge.sh dev` before handing control back to the user.
Exception: if the change does not affect the app itself, for example it only touches `site/`, GitHub workflow files, or other non-app assets/docs, skip rebuilding and relaunching the bundled app. Apply the same exception to GitHub workflow-only changes.

## Commit & Pull Request Guidelines
Recent commits use short imperative subjects that describe shipped behavior, for example `Add app UI localization support` and `Stabilize slash menu interactions`. Keep commits focused and behavior-oriented. PRs should link the source issue, summarize the behavior change, list validation steps, and call out risks or regressions checked. Include screenshots or exported-note samples when UI, sync output, or attachment handling changes.

## Release Guidelines
Every GitHub release must include a changelog in the release notes. Do not publish a release with only a generic placeholder such as "Direct download build for macOS." Summarize the user-visible changes since the previous release, group them into a few high-signal bullets, and mention important distribution details such as whether the build is ad-hoc signed or notarized.

## Security & Configuration Tips
Do not commit Apple Notes data, exported vault content, signing secrets, notarization credentials, or local permission artifacts. Use the documented environment variables in the release scripts for signing and notarization, and keep repository security settings aligned with `SECURITY.md`.
