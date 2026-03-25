# Feature Request: Change-Triggered Automatic Sync

## Summary

Add a change-triggered automatic sync mode for Apple Notes -> Obsidian so NotesBridge can run incremental sync shortly after note content changes, instead of relying only on manual sync or fixed polling intervals.

## Problem

NotesBridge already supports:

- manual `Sync Changed Notes`
- manual `Run Full Sync`
- timer-based automatic sync every 30 minutes, 1 hour, 6 hours, or 1 day

That leaves a gap for users who want synced markdown to stay fresh while they actively work in Apple Notes, without waiting for the next interval and without repeatedly pressing a button.

Periodic sync is useful, but it is not the same as modification-triggered sync.

## Current State

Current auto-sync behavior is interval-only:

- sync settings expose `Enable Automatic Sync` plus `Automatic Sync Interval`
- the interval options are defined in `Sources/NotesBridge/Domain/AutomaticSyncInterval.swift`
- automatic execution is timer-driven in `Sources/NotesBridge/App/AppModel.swift`
- sync settings persist `automaticSyncEnabled` and `automaticSyncInterval` in `Sources/NotesBridge/Domain/AppSettings.swift`

There is also a legacy `autoSyncOnPush` coding key in `AppSettings`, which suggests this idea existed previously but is not part of the current behavior.

## Proposal

Add a second automatic sync mode:

- `Periodic`
- `On Change`

Optional follow-up:

- `On Change + Fallback Interval`

For the first version, `On Change` should:

1. detect that Apple Notes content likely changed
2. debounce rapid edits
3. run the existing incremental sync pipeline
4. avoid overlapping sync runs
5. coalesce repeated changes into one follow-up sync when a sync is already in progress

## User Experience

In `Settings > Indexing & Sync`, replace the current interval-only model with an explicit trigger model.

Suggested controls:

- `Enable Automatic Sync`
- `Automatic Sync Trigger`
  - `Periodic`
  - `On Change`
- `Automatic Sync Interval`
  - shown only when trigger is `Periodic`

Suggested behavior:

- when `On Change` is enabled, NotesBridge waits for a detected source change and then runs `Sync Changed Notes`
- use a short debounce window such as 5 to 10 seconds
- if several edits happen close together, they should produce one sync run
- if a sync is already running, queue at most one extra run afterward

## Acceptance Criteria

1. When automatic sync is enabled in `On Change` mode, NotesBridge starts an incremental sync within a short debounce window after Apple Notes content changes.
2. Multiple rapid edits are coalesced into a single sync run.
3. NotesBridge never runs two sync jobs concurrently.
4. If edits happen during an active sync, NotesBridge schedules one follow-up incremental sync after the current run completes.
5. If nothing changed, NotesBridge should not create file churn or misleading status updates.
6. Manual `Sync Changed Notes` and `Run Full Sync` continue to work unchanged.
7. Existing `Periodic` automatic sync continues to work unchanged.
8. Settings migration preserves existing users on their current interval-based behavior unless they explicitly opt into `On Change`.

## Non-Goals

- reverse sync from Obsidian back to Apple Notes
- keystroke-by-keystroke live mirroring
- iOS push notifications
- replacing the existing incremental sync pipeline

## Implementation Notes

Use the current incremental sync path rather than building a second export path.

Recommended implementation shape:

- keep `runIncrementalSync(trigger:)` as the execution path
- add a new automatic sync trigger setting instead of overloading `AutomaticSyncInterval`
- add a small scheduler/coalescer in `AppModel` for debounced change-triggered runs
- prefer a reliable source-change signal such as Apple Notes data-folder file events, database file timestamp changes, or another repository-grounded signal
- if low-level change signals are noisy, gate them behind debounce and change coalescing before starting sync

## Open Questions

1. What is the best source-of-truth signal for "Apple Notes changed" on macOS in this app:
   - file-system events on the Apple Notes container
   - database file modification timestamps
   - foreground/app-state heuristics plus lightweight checks
2. What debounce window feels right for real usage: 5 seconds, 10 seconds, or configurable?
3. Should `On Change` remain a standalone mode for v1, with `On Change + Fallback Interval` as a later enhancement?

## Suggested Issue Title

`Add change-triggered automatic sync for Apple Notes -> Obsidian`
