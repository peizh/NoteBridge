## 1. 当前任务目标

当前主线任务是完成并推进 GitHub 上的 i18n feature request，并把这项工作通过 PR 流程推进到可合并状态。

当前对应 GitHub artefacts：
- issue: `#3 [Feature] Add i18n support for Chinese and French`
- PR: `#4 Add app UI localization support`

预期产出：
- NotesBridge app 内支持 `System / English / 简体中文 / Français`
- 设置页、菜单栏弹窗、slash menu、核心状态/同步进度文案能随语言切换
- slash command token 仍保持英文稳定，例如 `/title`
- PR review comment 已处理，CI 通过，PR 可继续 review / merge

完成标准：
- PR #4 无未处理的合理 review finding
- `swift test` 和 `xcodebuild ... test` 通过
- 用户确认 UI 语言切换覆盖范围满足预期，或继续扩展剩余未本地化文案

## 2. 当前进展

已经完成：
- 为 app 新增轻量本地化层，而不是引入 Apple `.strings` / bundle 级完整 i18n 系统
- 新增语言枚举：
  - `/Users/petepei/Projects/Notes/Sources/NotesBridge/Domain/AppLanguage.swift`
- 新增本地化字典和 helper：
  - `/Users/petepei/Projects/Notes/Sources/NotesBridge/Support/AppLocalization.swift`
- 在 `AppSettings` 中持久化语言选择：
  - `/Users/petepei/Projects/Notes/Sources/NotesBridge/Domain/AppSettings.swift`
- 在 `AppModel` 中加入：
  - `localization`
  - `t(_:)`
  - `tf(_:_:)`
  - `languageDisplayName(for:)`
- 已接入本地化的主要 UI：
  - 设置页 `SettingsView`
  - 菜单栏弹窗 `MenuBarContentView`
  - 同步进度 `SyncProgress`
  - slash 命令摘要 / inline 状态摘要 / 核心状态文案
- 已补 slash menu 漏掉的标题本地化：
  - `SlashCommandCatalog` 改为 `titleKey`
  - `SlashCommandMenuView` 改为根据 `AppLocalization` 渲染显示标题
  - `SlashCommandEngine` / `SlashCommandMenuController` 支持传递 localization
  - slash token 仍保持英文不变
- 新增测试：
  - `/Users/petepei/Projects/Notes/Tests/NotesBridgeTests/AppLocalizationTests.swift`

Git 进展：
- 已创建并推送分支：`codex/i18n-support`
- 已创建 PR：
  - [#4 Add app UI localization support](https://github.com/peizh/NotesBridge/pull/4)
- 已关联 feature request：
  - `Closes #3`

Review 处理：
- cubic 在 PR #4 提了两条 review finding，均已确认合理并修复
- 修复提交：
  - `7beae8e` `Add app UI localization support`
  - `54e8600` `Address i18n review feedback`
- 已在 PR 中回复并明确说明是 `cubic found` 的问题：
  - https://github.com/peizh/NotesBridge/pull/4#issuecomment-4062494324

## 3. 关键上下文

重要背景：
- 仓库是 `NotesBridge`
- 当前默认分支已经是 `main`
- 用户明确要求以后不要直接 push 到 `main`，要走 PR 流程
- 当前 i18n 工作就是按这个要求走的

用户的明确要求：
- 实现 GitHub 上关于 i18n 的 feature request
- 先支持 app UI 层面的中/法文
- slash menu 也要包含在 i18n 范围内
- 最终要整理成 PR，并关联 GitHub 上的需求 issue
- 需要处理 PR 上的 review comments，如合理则修复再提交

已知约束：
- 当前环境里没有可直接使用的 `gh` CLI，之前尝试 `gh issue list` 失败：`command not found`
- GitHub 交互当前通过：
  - `git credential-manager get`
  - GitHub REST API
- 必须用 `apply_patch` 编辑文件
- 当前运行环境对我创建分支有前缀约束：`codex/`
- 仓库中存在未跟踪本地目录，不应提交：
  - `.worktree-attachments/`
  - `obsidian-importer/`

已做出的关键决定：
- 采用“轻量 app-level localization”方案，不上完整 `.strings` / `Bundle.main.localizedString` 体系
- 原因：当前 feature request 范围主要在 app UI，且现有项目很多文案由 `AppModel` 拼装/返回，直接集中到一个 `AppLocalization` 更快、更稳、更容易补齐
- slash command token 保持英文，不做本地化，例如 `/title`
- 只本地化可见标题，如“Title / Heading / Table”

重要假设：
- 当前 issue #3 的范围以 app UI 为主，不要求一次性把所有错误、日志、导出文本、诊断文本都彻底国际化
- 如果后续 reviewer / 用户继续追补，可以在当前方案上继续加 key，而不需要推翻设计

## 4. 关键发现

1. slash menu 确实一开始漏掉了
- 原因不是 `SettingsView` 或 `AppModel`，而是：
  - `/Users/petepei/Projects/Notes/Sources/NotesBridge/Interaction/SlashCommandCatalog.swift`
  - 其中 `SlashCommandEntry.title` 是硬编码英文
- 已修复为 `titleKey + localizedTitle(using:)`

2. cubic 的两个 review finding 都是有效问题
- P1:
  - `AppModel.tf(_:_:)` 最初把 variadic 参数直接转发给另一个 variadic，会多包一层数组
  - 已改为 `AppLocalization.text(_:arguments:)`
- P2:
  - `AppLocalizationTests` 里直接对可选 `entry?` 做 `#expect`
  - 已改为 `try #require(...)`

3. 当前这版 i18n 设计是“局部覆盖成功，但不是全量覆盖”
- 已覆盖：设置页、菜单栏、slash menu 标题、同步进度、部分状态摘要
- 未完全覆盖：所有 `AppModel.present(...)` fallback、部分 error message、部分 Apple Notes 数据访问 message、部分 attachment warning / sync diagnostics

4. 当前工作区有用户之前留下的 README 改动
- `README.md`
- `README.zh-CN.md`
- `README.fr.md`
- 这三份改动没有被纳入 i18n PR，必须继续保持隔离，避免误把无关文案改动混到 PR #4 里

5. 分支状态
- 当前分支应为：`codex/i18n-support`
- 最新已推远端提交：`54e8600`

## 5. 未完成事项

按优先级排序：

1. 跟进 PR #4 的后续 review / CI / merge
- 检查 PR 是否还有新的 review comment
- 检查 GitHub Actions 是否通过
- 如有新 comment，继续按同样方式处理

2. 评估是否需要继续扩大 i18n 覆盖范围
- 当前 PR 已满足 issue 的核心范围，但还存在英文残留
- 需要看 reviewer / 用户是否要求：
  - Apple Notes data access status message 本地化
  - `present(error, fallback:)` 的所有 fallback 文案本地化
  - attachment / sync diagnostics 文案本地化

3. 如果 PR 合并，后续可能要继续补 README 或发行说明的多语言叙事
- 这不属于当前 PR 范围
- 但用户之前对 README / banner / 多语言 README 做过很多工作，后续可能继续追

## 6. 建议接手路径

优先查看这些文件：

1. i18n 主要实现
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Support/AppLocalization.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Domain/AppLanguage.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Domain/AppSettings.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/App/AppModel.swift`

2. UI 接线层
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Views/SettingsView.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Views/MenuBarContentView.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Domain/SyncProgress.swift`

3. slash menu i18n
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Interaction/SlashCommandCatalog.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Interaction/SlashCommandMenuView.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Interaction/SlashCommandMenuController.swift`
- `/Users/petepei/Projects/Notes/Sources/NotesBridge/Interaction/SlashCommandEngine.swift`

4. 测试
- `/Users/petepei/Projects/Notes/Tests/NotesBridgeTests/AppLocalizationTests.swift`

优先验证：
- `git branch --show-current` 确认还在 `codex/i18n-support`
- `git status --short` 确认 README 改动仍未被 staged/committed 到 i18n PR
- 重新看 PR #4 当前状态和 comment

建议命令：
- 检查分支/工作区：
  - `git branch --show-current`
  - `git status --short`
- 跑测试：
  - `swift test --filter AppLocalizationTests`
  - `swift test`
  - `xcodebuild -scheme NotesBridge -workspace .swiftpm/xcode/package.xcworkspace -destination 'platform=macOS' test`

如果要继续读 GitHub：
- 当前没有 `gh`
- 用下面方式继续：
  - 通过 `git credential-manager get` 取当前 GitHub 凭据
  - 用 Python + `urllib.request` 调 GitHub REST API
- 已验证可用的 endpoints：
  - `GET /repos/{owner}/{repo}/pulls/4/reviews`
  - `GET /repos/{owner}/{repo}/pulls/4/comments`
  - `POST /repos/{owner}/{repo}/issues/4/comments`

推荐下一步动作：
1. 先检查 PR #4 是否出现新的 review / CI 失败
2. 如果没有，等待或推动合并
3. 如果用户要求“继续补齐所有英文残留”，就在当前 `AppLocalization` 上继续加 key，不要切换到另一套 i18n 机制

## 7. 风险与注意事项

1. 不要把 README 改动误带进 i18n PR
- 当前工作区中有 3 个 README 文件改动，是用户之前其他工作留下的
- 它们不属于 issue #3，不应混入 PR #4

2. 不要改 slash token
- 用户当前要的是 UI 可本地化，不是命令语法本地化
- `/title`、`/heading`、`/table` 这些 token 需要保持英文稳定

3. 不要重复追“为什么不用 .strings”
- 这轮已经做了明确设计决策：轻量本地化层优先
- 除非用户明确要求迁移到系统本地化资源，否则继续在 `AppLocalization` 上增量迭代最合适

4. 注意 attribution
- PR #4 上的 review finding 来自 cubic
- 如果继续在 PR comment / summary 中提到这两条问题，要明确写是 `cubic found`

5. GitHub 鉴权别再绕回 `gh`
- 当前环境里 `gh` 不可用
- 直接沿用已验证的 `git credential-manager get + Python urllib` 路线最稳

6. 不要提交未跟踪目录
- `.worktree-attachments/`
- `obsidian-importer/`

下一位 Agent 的第一步建议：

先运行：
- `git branch --show-current`
- `git status --short`

确认还在 `codex/i18n-support`，且 README 改动没有被 staged。然后用 GitHub API 再检查一次 PR #4 的最新 review / checks。如果没有新问题，就把精力放在推动合并；如果有新 comment，就只在当前 `AppLocalization` 方案上继续增量修复，不要重构 i18n 体系。
