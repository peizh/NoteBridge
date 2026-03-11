#!/usr/bin/env python3
"""Create a repeatable Apple Notes fixture tree for NotesBridge testing.

The script creates a dedicated top-level folder in Apple Notes, then recreates
folders and notes with richer HTML bodies than the old JXA probes.

Apple Notes does not reliably preserve scripted internal-note hrefs when body
HTML is assigned directly. For cross-note coverage, this script writes both:
1. an attempted applenotes:note anchor
2. the visible target note identifier alongside the reference text

That gives NotesBridge stable fixture content for naming, folder hierarchy,
rich text, date-titled notes, and traceable note-to-note references.
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class NoteFixture:
    key: str
    folder_key: str
    title: str
    template: str
    link_targets: Dict[str, str] = field(default_factory=dict)


FOLDERS = {
    "root": "",
    "inbox": "Inbox",
    "projects": "Projects",
    "specs": "Projects/Specs",
    "design": "Projects/Design",
    "journal": "Journal",
    "journal-2026": "Journal/2026",
    "journal-march": "Journal/2026/March",
    "research": "Research",
    "notebooklm": "Research/NotebookLM",
    "zh": "中文",
    "zh-product": "中文/产品",
}


NOTES: List[NoteFixture] = [
    NoteFixture(
        key="welcome",
        folder_key="inbox",
        title="Welcome to NotesBridge",
        template="""
<div>
  <h1>Welcome to NotesBridge</h1>
  <h2>Fixture goals</h2>
  <p>This note covers <b>bold</b>, <i>italic</i>, <code>inline code</code>, and a
  <a href="https://example.com/notesbridge">regular web link</a>.</p>
  <blockquote>Use this folder tree to validate native Apple Notes sync.</blockquote>
  <ul>
    <li>Nested folders</li>
    <li>Mixed English and 中文 content</li>
    <li>Date-titled journal notes</li>
    <li>Cross-note references</li>
  </ul>
  <p>See also: {link:roadmap}</p>
  <table>
    <tr><th>Area</th><th>Status</th></tr>
    <tr><td>Sync</td><td>Ready</td></tr>
    <tr><td>Slash</td><td>Regression-tested</td></tr>
  </table>
</div>
""",
        link_targets={"roadmap": "roadmap"},
    ),
    NoteFixture(
        key="roadmap",
        folder_key="specs",
        title="Roadmap Q3",
        template="""
<div>
  <h1>Roadmap Q3</h1>
  <p>Roadmap note with references into design and journal history.</p>
  <ol>
    <li>Ship native NoteStore sync</li>
    <li>Stabilize slash commands</li>
    <li>Improve debug logging and fixtures</li>
  </ol>
  <p>Design reference: {link:design-system}</p>
  <p>Journal reference: {link:journal-today}</p>
  <pre><code>swift test
xcodebuild -scheme NotesBridge -workspace .swiftpm/xcode/package.xcworkspace -destination 'platform=macOS' test</code></pre>
</div>
""",
        link_targets={
            "design-system": "design-system",
            "journal-today": "journal-today",
        },
    ),
    NoteFixture(
        key="design-system",
        folder_key="design",
        title="Design System v2",
        template="""
<div>
  <h1>Design System v2</h1>
  <h3>Component coverage</h3>
  <p>This note is intentionally dense to exercise HTML to Markdown conversion.</p>
  <table>
    <tr><th>Component</th><th>Owner</th><th>State</th></tr>
    <tr><td>Command Menu</td><td>Editor</td><td>Experimental</td></tr>
    <tr><td>Sync Status</td><td>Bridge</td><td>Stable</td></tr>
    <tr><td>Attachments</td><td>Importer</td><td>Stable</td></tr>
  </table>
  <blockquote>Design debt is acceptable only when it is visible and testable.</blockquote>
  <p>Back to roadmap: {link:roadmap}</p>
</div>
""",
        link_targets={"roadmap": "roadmap"},
    ),
    NoteFixture(
        key="journal-today",
        folder_key="journal-march",
        title="3/11/2026",
        template="""
<div>
  <h1>3/11/2026</h1>
  <p>Journal note with a slash in the title to validate file-name sanitization.</p>
  <p>Yesterday: {link:journal-yesterday}</p>
  <p>Project roadmap: {link:roadmap}</p>
  <ul>
    <li>Checked Apple Notes account visibility</li>
    <li>Captured unified logs</li>
    <li>Rebuilt test fixtures</li>
  </ul>
</div>
""",
        link_targets={
            "journal-yesterday": "journal-yesterday",
            "roadmap": "roadmap",
        },
    ),
    NoteFixture(
        key="journal-yesterday",
        folder_key="journal-march",
        title="3/10/2026",
        template="""
<div>
  <h1>3/10/2026</h1>
  <p>Prior journal entry that links forward.</p>
  <p>Next day: {link:journal-today}</p>
  <p>Research follow-up: {link:notebooklm}</p>
</div>
""",
        link_targets={
            "journal-today": "journal-today",
            "notebooklm": "notebooklm",
        },
    ),
    NoteFixture(
        key="notebooklm",
        folder_key="notebooklm",
        title="NotebookLM Research Pack",
        template="""
<div>
  <h1>NotebookLM Research Pack</h1>
  <p>Used to test long-form mixed formatting.</p>
  <h2>Inputs</h2>
  <ul>
    <li>Annual report PDF</li>
    <li>Quarterly filing screenshots</li>
    <li>Executive summary draft</li>
  </ul>
  <h2>Questions</h2>
  <ol>
    <li>What changed in gross margin?</li>
    <li>Which risk factors repeated from last year?</li>
    <li>Which items should be added to the Obsidian vault?</li>
  </ol>
  <p>Reference note: {link:welcome}</p>
</div>
""",
        link_targets={"welcome": "welcome"},
    ),
    NoteFixture(
        key="zh-product",
        folder_key="zh-product",
        title="赛博朋克粒子交互系统开发指令角色设定",
        template="""
<div>
  <h1>赛博朋克粒子交互系统开发指令角色设定</h1>
  <p>这是一条用于验证中英文混排、标题、列表、引用与代码块的测试数据。</p>
  <blockquote>目标：验证 Apple Notes 到 Obsidian 的中文目录与正文导出。</blockquote>
  <ul>
    <li>角色：系统架构师</li>
    <li>风格：冷静、直接、可执行</li>
    <li>输出：Markdown 文档与引用链接</li>
  </ul>
  <pre><code>{
  "persona": "systems-architect",
  "language": "zh-CN",
  "theme": "cyberpunk-particles"
}</code></pre>
  <p>关联英文说明：{link:welcome}</p>
</div>
""",
        link_targets={"welcome": "welcome"},
    ),
    NoteFixture(
        key="edge-cases",
        folder_key="inbox",
        title="Sync Edge Cases",
        template="""
<div>
  <h1>Sync Edge Cases</h1>
  <p>This note exists to stress export naming and unresolved-link handling.</p>
  <p>Existing link: {link:journal-today}</p>
  <p>Missing link: {link:missing-note}</p>
  <p>Literal Apple Notes URL for parser inspection:</p>
  <pre><code>applenotes:note/{missing-note-id}</code></pre>
</div>
""",
        link_targets={"journal-today": "journal-today"},
    ),
]


def run_osascript(script: str, *args: str) -> str:
    command = ["osascript", "-"]
    command.extend(args)
    result = subprocess.run(
        command,
        input=script,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown osascript failure"
        raise RuntimeError(message)
    return result.stdout.strip()


def delete_root_folder(root_name: str) -> None:
    script = """
on run argv
    set rootName to item 1 of argv
    tell application "Notes"
        if exists folder rootName then
            delete folder rootName
        end if
    end tell
end run
"""
    run_osascript(script, root_name)


def ensure_top_level_folder(root_name: str) -> str:
    script = """
on run argv
    set rootName to item 1 of argv
    tell application "Notes"
        if exists folder rootName then
            return id of folder rootName
        end if

        set createdFolder to make new folder with properties {name:rootName}
        return id of createdFolder
    end tell
end run
"""
    return run_osascript(script, root_name)


def ensure_child_folder(parent_id: str, folder_name: str) -> str:
    script = """
on run argv
    set parentID to item 1 of argv
    set childName to item 2 of argv
    tell application "Notes"
        set parentFolder to folder id parentID
        repeat with existingFolder in folders of parentFolder
            if (name of existingFolder as text) is childName then
                return id of existingFolder
            end if
        end repeat

        set createdFolder to make new folder at parentFolder with properties {name:childName}
        return id of createdFolder
    end tell
end run
"""
    return run_osascript(script, parent_id, folder_name)


def create_note(folder_id: str, title: str) -> str:
    script = """
on run argv
    set folderID to item 1 of argv
    set noteTitle to item 2 of argv
    tell application "Notes"
        set targetFolder to folder id folderID
        set createdNote to make new note at targetFolder with properties {name:noteTitle}
        return id of createdNote
    end tell
end run
"""
    return run_osascript(script, folder_id, title)


def update_note_body(note_id: str, body_html: str) -> None:
    script = """
on run argv
    set noteID to item 1 of argv
    set noteBody to item 2 of argv
    tell application "Notes"
        set body of note id noteID to noteBody
    end tell
end run
"""
    run_osascript(script, note_id, body_html)


def render_link(label: str, target_id: str | None, target_title: str | None) -> str:
    safe_label = html.escape(label)
    if not target_id or not target_title:
        return f"{safe_label} (unresolved fixture target)"

    safe_title = html.escape(target_title)
    safe_id = html.escape(target_id)
    return (
        f'<a href="applenotes:note/{safe_id}">{safe_label}</a>'
        f' <span style="color:#666;">(target: {safe_title} · applenotes:note/{safe_id})</span>'
    )


def render_body(note: NoteFixture, note_ids: Dict[str, str], note_titles: Dict[str, str]) -> str:
    body = note.template
    for token, target_key in note.link_targets.items():
        body = body.replace(
            "{link:" + token + "}",
            render_link(note_titles.get(target_key, target_key), note_ids.get(target_key), note_titles.get(target_key)),
        )

    body = body.replace(
        "{missing-note-id}",
        html.escape("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"),
    )
    return body.strip()


def build_folder_tree(root_name: str) -> Dict[str, str]:
    folder_ids: Dict[str, str] = {"root": ensure_top_level_folder(root_name)}
    path_to_key = {path: key for key, path in FOLDERS.items() if path}
    for folder_key, relative_path in FOLDERS.items():
        if folder_key == "root":
            continue
        current_parent_id = folder_ids["root"]
        current_path_parts: List[str] = []
        for segment in relative_path.split("/"):
            current_path_parts.append(segment)
            partial_path = "/".join(current_path_parts)
            next_key = path_to_key.get(partial_path)
            current_parent_id = ensure_child_folder(current_parent_id, segment)
            if next_key is not None and next_key not in folder_ids:
                folder_ids[next_key] = current_parent_id
        folder_ids[folder_key] = current_parent_id
    return folder_ids


def create_fixture_notes(folder_ids: Dict[str, str]) -> Dict[str, str]:
    note_ids: Dict[str, str] = {}
    for note in NOTES:
        note_ids[note.key] = create_note(folder_ids[note.folder_key], note.title)
    return note_ids


def populate_fixture_bodies(note_ids: Dict[str, str]) -> None:
    note_titles = {note.key: note.title for note in NOTES}
    for note in NOTES:
        update_note_body(note_ids[note.key], render_body(note, note_ids, note_titles))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recreate a rich Apple Notes fixture tree for NotesBridge testing."
    )
    parser.add_argument(
        "--root-folder",
        default="NotesBridge Fixtures",
        help="Top-level Apple Notes folder to create.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete the existing top-level fixture folder before recreating it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.replace:
            delete_root_folder(args.root_folder)
        folder_ids = build_folder_tree(args.root_folder)
        note_ids = create_fixture_notes(folder_ids)
        populate_fixture_bodies(note_ids)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Created Apple Notes fixture root: {args.root_folder}")
    for note in NOTES:
        print(f"- {FOLDERS[note.folder_key] or '.'}/{note.title} [{note_ids[note.key]}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
