## 1. 当前任务目标
- 当前会话已经收尾，最近一轮重点是稳定 `0.2.2` 发布后的 Apple Notes 正文同步渲染。
- 最近两个已修复的高优先级格式同步问题：
  - code block 首字符落在 Markdown fence 外。
  - `mailto:p@peizh.live` 被碎成多个 Markdown link，同时影响下一行删除线。
- 当前没有未落地的代码修改；如果下一位 Agent 接手，优先处理新的用户反馈或继续 release/update 基础设施收尾。

## 2. 当前进展
- `Issue #8` 的 Sparkle 直装更新能力已完成并合并；PR #9 已 merged。
- `Issue #10` 已创建，主题是统一 slash menu / inline menu 交互与视觉风格。
- `0.2.2` GitHub Release 已发布；相关提交包括：
  - `3b9eb4d` `Fix release Sparkle framework lookup`
  - `a88184a` `Prepare 0.2.2 release notes`
- Apple Notes 渲染相关最近提交：
  - `6efb71c` `fix bug of sync decoder`
    - 修复 CRLF 归一化过早导致的 `attributeRuns.length` offset 漂移，解决 code block 首字符掉到 fence 外。
  - `555ded9` `Fix fragmented mailto and strikethrough rendering`
    - 在段落归一化阶段合并相邻同格式 runs，修复 `mailto` 和删除线碎裂。
- 当前分支是 `main`，当前 `HEAD`/`origin/main` 是 `95759ed` `update README.*`。
  - 说明用户在 `555ded9` 之后又更新了 README.*；不要回退这部分。

## 3. 关键上下文
- 关键代码路径：
  - `/Users/petepei/Projects/Notes/Sources/NotesBridge/Services/AppleNotesNoteProtoDecoder.swift`
  - `AppleNotesMarkdownRenderer.normalizedRenderRuns(...)`
  - `AppleNotesMarkdownRenderer.RenderState.formattedText(...)`
- 关键测试文件：
  - `/Users/petepei/Projects/Notes/Tests/NotesBridgeTests/AppleNotesMarkdownRendererTests.swift`
- 用户明确要求的工作流规则：
  - 每次任何测试命令通过后，都要立刻启动 bundled app。
  - 这个规则被写进了未跟踪文件 `/Users/petepei/Projects/Notes/AGENTS.md`，但没有提交进 git。
- 已知 bundled app 命令与路径：
  - 命令：`./scripts/run-bundled-app.sh`
  - app：`/Users/petepei/Library/Application Support/NotesBridge/NotesBridge.app`
- 用于真实 Apple Notes payload 离线排查的本地数据库路径：
  - `/Users/petepei/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`
- 之前提取真实 note payload（note PK `7418`）的命令，后续如果还有同步格式 bug 可复用：
  - `sqlite3 "/Users/petepei/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite" "SELECT hex(d.ZDATA) FROM ZICCLOUDSYNCINGOBJECT n JOIN ZICNOTEDATA d ON d.ZNOTE = n.Z_PK WHERE n.Z_PK = 7418;" > /tmp/note7418.hex`

## 4. 关键发现
- 不要在按 `attributeRuns.length` 切片之前对整段 `noteText` 做 `\r\n -> \n` 归一化。
  - Apple Notes 的 run 长度是按原始文本计数；提前归一化会让 offset 漂移。
- Apple Notes 会把同一个逻辑格式 span 拆成多个相邻 run。
  - 真实出现过的类型：code block 段落、`mailto` link、删除线。
  - 直接按 run 单独渲染 Markdown 会生成碎链接、残缺 `~~`、或 fence 边界错位。
- 当前正确修复点在 `normalizedRenderRuns(...)`：
  - 先按原始文本切 run。
  - 按段落回填缺失的段落样式。
  - 再把“格式完全相同”的相邻 runs 合并后交给 `formattedText(...)`。
- 当前 run 合并的等价条件在 `canMerge(...)`，包含：
  - `paragraphStyle`
  - `fontWeight`
  - `underlined`
  - `strikethrough`
  - `superscript`
  - `link`
  - `attachmentInfo`
- 之前 CI 有过 `xcodebuild test` 跑完不退出的问题，根因是测试进程里启动了真实 Sparkle updater。
  - 已通过给非更新相关测试注入 `NoOpAppUpdater` 修好，不要回退。
- release/update 基础设施的最后已知外部状态：
  - `0.2.2` release 已发.
  - GitHub Actions 曾因账号 billing / spending limit 问题导致 release workflow 没有跑起来.
  - 本会话里 `https://peizh.github.io/NotesBridge/updates/appcast.xml` 曾是 404；若下次继续处理更新分发，需要重新确认当前 Pages/billing 状态.

## 5. 未完成事项
- 没有未提交代码。
- 如果用户继续报正文同步格式问题：
  - 先新增最小回归测试，再改 renderer。
  - 改完后用 bundled app 重新执行一次 sync，确认真实导出结果。
- 如果用户继续推进更新分发：
  - 检查 GitHub Pages 是否已启用。
  - 检查 `SPARKLE_PRIVATE_ED_KEY` secret。
  - 检查 Actions billing/spending limit 是否已恢复。
- 如果用户继续推进菜单体验优化：
  - 从 Issue #10 开始，不要重新做问题定义；已有一版清晰的 acceptance criteria 和 phased plan。

## 6. 建议接手路径
- 如果继续处理 Apple Notes 同步渲染问题：
  - `git status --short`
  - 保持未跟踪文件不动：`.worktree-attachments/`、`260315-handoff.md`、`260320-handoff.md`、`260323-handoff.md`、`AGENTS.md`、`docs/`
  - 从 `/Users/petepei/Projects/Notes/Sources/NotesBridge/Services/AppleNotesNoteProtoDecoder.swift` 的 `normalizedRenderRuns(...)` 开始看。
  - 在 `/Users/petepei/Projects/Notes/Tests/NotesBridgeTests/AppleNotesMarkdownRendererTests.swift` 先写回归测试。
  - 运行：
    - `swift test`
    - `./scripts/run-bundled-app.sh`
    - `xcodebuild -scheme NotesBridge -workspace .swiftpm/xcode/package.xcworkspace -destination 'platform=macOS' test`
    - `./scripts/run-bundled-app.sh`
  - 再用 bundled app 执行一次 sync，确认真实 Markdown 输出。
- 如果继续处理 release / Sparkle / Pages：
  - 先看 `/Users/petepei/Projects/Notes/.github/workflows/release.yml`
  - 再看 `/Users/petepei/Projects/Notes/scripts/publish-sparkle-appcast.sh`
  - 然后确认远端 Pages 和 billing 状态，不要只看本地脚本。

## 7. 风险与注意事项
- 当前 git 工作区只有未跟踪文件，没有 tracked dirty changes；这些未跟踪文件大多是用户本地文档或 handoff，不要随便删除或提交。
- `run-bundled-app.sh` / bundled build 过程中会出现 `install_name_tool` 让签名失效的 warning，但脚本后续会重新签名；这条 warning 目前是已知正常噪音。
- `swift test` 和 `xcodebuild test` 输出里，Swift Testing 的真实结果在后半段 `◇ / ✔` 区块，不要被前面的 XCTest “Executed 0 tests” 误导。
- 如果未来还有 run merge 相关 bug，优先扩展 `canMerge(...)` 的判定条件，不要把零散的 Markdown 拼接补丁塞进 `formattedText(...)`。
- 用户对执行习惯要求比较明确：
  - 不要提交或回退无关文件。
  - 测试通过后要启动 bundled app。

下一位 Agent 的第一步建议：
先运行 `git status --short` 确认工作区只有这些未跟踪文件；如果用户继续报正文同步格式问题，直接从 `AppleNotesMarkdownRenderer.normalizedRenderRuns(...)` 和 `AppleNotesMarkdownRendererTests.swift` 入手，先写最小回归测试再改实现。
