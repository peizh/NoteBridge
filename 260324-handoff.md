## 1. 当前任务目标

把 NotesBridge 的 direct-download 更新链路恢复到可用状态，并为下一位 Agent 保留足够上下文以继续做端到端验证和后续收尾。当前阶段的完成标准是：

- `0.2.5` GitHub release 已发布并带 changelog
- Sparkle appcast 已成功发布到 GitHub Pages
- 仓库已配置 `SPARKLE_PRIVATE_ED_KEY`
- 已明确说明 `0.2.2` 到 `0.2.4` 用户需要手动升级一次
- 下一步只剩真实 app 内的更新检查验证和后续流程优化

## 2. 当前进展

- 已定位 update feature broken 的根因：不是客户端 UI 逻辑，而是 Sparkle feed `https://peizh.github.io/NotesBridge/updates/appcast.xml` 之前返回 `404`。
- 已确认此前没有 `gh-pages` 分支，release workflow 也因缺少 changelog section 和缺少 `SPARKLE_PRIVATE_ED_KEY` 失败。
- 已修复 clean runner 构建失败问题：
  - `/Users/petepei/Projects/Notes/scripts/build-app-bundle.sh`
  - 现在会先执行 `swift build -c release`，再解析 bin path，避免 `Sparkle.framework not found`。
- 已补 `CHANGELOG.md` 中 `0.2.4` 与 `0.2.5` section：
  - `/Users/petepei/Projects/Notes/CHANGELOG.md`
- 已确认旧 Sparkle 私钥找不到，按“已丢失”处理。
- 用户已本地生成新 Sparkle key：
  - public key: `bN0AdWyNntmdvuNQNXa2pDP8peMGNfsbBcrXIBf60ys=`
- 用户已本地导出私钥到 `/tmp/NotesBridge.sparkle.key`，我已执行：
  - `gh secret set SPARKLE_PRIVATE_ED_KEY < /tmp/NotesBridge.sparkle.key`
- 已更新内嵌公钥：
  - `/Users/petepei/Projects/Notes/scripts/build-app-bundle.sh`
- 已补文档：
  - `/Users/petepei/Projects/Notes/docs/sparkle-key-setup.md`
- 已提交并推送修复：
  - `a42f1c8` `Fix Sparkle release publishing for 0.2.4`
  - `47c589c` `Rotate Sparkle key and restore update publishing`
- 已触发并完成 Release workflow：
  - run id `23469831931`
- 已成功发布 release：
  - `0.2.5`
  - [Release](https://github.com/peizh/NotesBridge/releases/tag/0.2.5)
- 已成功发布 Sparkle appcast：
  - [appcast.xml](https://peizh.github.io/NotesBridge/updates/appcast.xml)

## 3. 关键上下文

- 当前分支：`main`
- 最近相关提交：
  - `47c589c Rotate Sparkle key and restore update publishing`
  - `0a68e2c Create GitHub Pages site`
  - `a42f1c8 Fix Sparkle release publishing for 0.2.4`
- 当前仓库工作区仍有未跟踪本地文件，不要误提交：
  - `/Users/petepei/Projects/Notes/.worktree-attachments/`
  - `/Users/petepei/Projects/Notes/260315-handoff.md`
  - `/Users/petepei/Projects/Notes/260320-handoff.md`
  - `/Users/petepei/Projects/Notes/260323-handoff.md`
  - `/Users/petepei/Projects/Notes/AGENTS.md`
  - `/Users/petepei/Projects/Notes/docs/repo-architecture-review.md`
- GitHub release 规则已明确：
  - 每次 release 必须带 changelog
  - 不允许只写占位文案
- 当前 release 分发状态：
  - direct-download
  - ad-hoc signed
  - not notarized
- 用户明确要求：
  - 以后 release 要带 changelog
  - 更新功能要能实际工作

## 4. 关键发现

- update feature 失败的直接原因是 Sparkle feed 不存在，不是客户端“检查更新”代码本身坏掉。
- 旧公钥 `0Gcbr/JsQLrUXt36na4JMUNt7S9/+GIVr3fNSE8q1F4=` 对应的私钥没有找到：
  - `gh secret list` 最初为空
  - `generate_keys -p` 找不到已有 signing key
  - Keychain 里也没有 Sparkle 旧私钥记录
- 因此必须做 Sparkle key rotation。
- 这意味着：
  - `0.2.2` 到 `0.2.4` 无法自动升级到 `0.2.5`
  - 用户必须手动安装一次 `0.2.5`
  - 从 `0.2.5` 开始，后续自动更新才可能恢复正常
- 目前基础链路已经通了：
  - `gh-pages` 分支存在
  - `appcast.xml` 返回 `200`
  - `0.2.5` release note 正常
  - 发布包里嵌入的新公钥与刚生成的 key 一致
- 仍有一个 CI/workflow 层面的后续点：
  - Release workflow annotation 提示 `actions/upload-artifact@v4` 仍基于 Node 20，后续最好升到支持 Node 24 的版本

## 5. 未完成事项

1. 做一次真实端到端更新验证：
   - 手动安装 `0.2.5`
   - 在 app 内点击 `Check for Updates`
   - 确认 Sparkle 可以正常读取 appcast，不再报 “retrieving update information” 错误
2. 如果用户需要更稳的发布体验，补正式说明：
   - 在 README 或 release note 里强调 `0.2.2–0.2.4` 需要手动升级一次
3. 可选收尾：
   - 升级 `.github/workflows/release.yml` 中 Node 20 相关 action
4. 可选长期项：
   - 推进 Developer ID 签名与 notarization，避免长期停留在 ad-hoc signed

## 6. 建议接手路径

- 先看这些文件：
  - `/Users/petepei/Projects/Notes/scripts/build-app-bundle.sh`
  - `/Users/petepei/Projects/Notes/.github/workflows/release.yml`
  - `/Users/petepei/Projects/Notes/CHANGELOG.md`
  - `/Users/petepei/Projects/Notes/docs/sparkle-key-setup.md`
- 先验证以下命令的结果仍然正确：
  - `gh release view 0.2.5`
  - `curl -I -L https://peizh.github.io/NotesBridge/updates/appcast.xml`
  - `git ls-remote --heads origin gh-pages`
  - `gh secret list`
- 如需确认发布包公钥一致性，使用：
  - `gh release download 0.2.5 -p 'NotesBridge-0.2.5-macOS.zip' -D /tmp/notesbridge-release-check`
  - `unzip -p /tmp/notesbridge-release-check/NotesBridge-0.2.5-macOS.zip NotesBridge.app/Contents/Info.plist | plutil -extract SUPublicEDKey raw -`
- 如果要继续改 release workflow，先用：
  - `gh run view 23469831931`
  - 作为已成功的基线 run

## 7. 风险与注意事项

- 不要再尝试找旧 Sparkle 私钥的恢复路径，已经做过 repo、环境、keychain、Sparkle 工具层面的检查；继续投入大概率重复劳动。
- 不要误以为 `0.2.5` 发布成功就等于旧版本能自动升级；由于公钥已轮换，`0.2.2–0.2.4` 只能手动升级一次。
- 不要提交当前工作区的未跟踪本地文件，尤其是 handoff、AGENTS 和本地文档。
- 如果用户后续反馈“仍然无法更新”，先确认他是否仍停留在 `0.2.2–0.2.4`。
- 当前分发仍是 ad-hoc signed / not notarized，不要把“更新恢复”误解成“正式分发体验已完善”。

下一位 Agent 的第一步建议：
先手动安装 `0.2.5`，然后在 app 内执行一次 `Check for Updates` 端到端验证；如果这一步通过，再决定是否继续优化 release workflow 的 Node 24 兼容和 notarization。
