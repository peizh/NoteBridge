# NotesBridge

[English](./README.md) | [简体中文](./README.zh-CN.md) | [Français](./README.fr.md)

[![CI](https://img.shields.io/github/actions/workflow/status/peizh/NoteBridge/ci.yml?branch=main&label=CI)](https://github.com/peizh/NoteBridge/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/peizh/NoteBridge?style=social)](https://github.com/peizh/NoteBridge/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/peizh/NoteBridge?style=social)](https://github.com/peizh/NoteBridge/network/members)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

![NotesBridge social banner](./images/notesbridge-social.svg)

> 该文档可能会略晚于英文版更新。

把共享的 Apple Notes 转成本地 Markdown 文件和文件夹，方便长期保存、搜索、版本管理，并交给 AI agents 使用。

## 项目状态

NotesBridge 仍在持续开发中。它是一个面向 macOS 的伴侣应用，适合那些在 Apple Notes 中接收、整理笔记，但希望长期知识资产以本地 Markdown 文件和文件夹形式保存的人。

当前直装版主要聚焦两件事：

- 在 Apple Notes 里提供 slash commands 和 markdown-style 行内编辑增强
- 把 Apple Notes 同步成具备文件夹、附件、front matter 和内部链接的本地优先 Markdown 仓库

Apple Notes 很适合承接家人和朋友共享过来的内容。NotesBridge 的作用，是把这些共享输入沉淀为更适合组织、自动化、版本管理、并与 AI agents 协作的 Markdown 工作区。

如果你已经在用 Apple Notes 做捕获、用 Obsidian 做长期整理，NotesBridge 就是为这种工作流准备的。

## 为什么值得试

- 把 Apple Notes 结构保留下来，变成真实的 Markdown 文件和文件夹。
- 保留原生附件、扫描件导出、表格和内部笔记链接。
- 让同步后的内容更适合搜索、版本管理和 AI agents 处理。
- 直接在 Apple Notes 上叠加 slash commands 和行内格式化工具。
- 以轻量菜单栏应用方式工作，而不是强行替换你的笔记流程。

## 快速开始

1. 从 [Releases](https://github.com/peizh/NoteBridge/releases) 下载最新直装版。
2. 将 `NotesBridge.app` 拖到 `/Applications`。
3. 启动应用并授予需要的 macOS 权限。
4. 第一次全量同步时选择 Apple Notes 数据目录。
5. 开始把 Apple Notes 同步到你的 Obsidian 仓库。

## 当前原型支持

- 以菜单栏伴侣应用方式运行，并提供轻量级设置窗口。
- 在 Apple Notes 位于前台且编辑器获得焦点时进行监听。
- 在支持的构建中，在选中文本上方显示浮动格式工具条。
- 将行首的 Markdown / 列表触发符转换为 Apple Notes 原生格式命令。
- 支持 slash commands，包括精确命令直接执行和浮动建议菜单。
- 将 Apple Notes 同步到 Obsidian 仓库，并导出 front matter 元数据与原生附件。

## 产品约束

Apple Notes 没有公开的插件或扩展 API，因此 NotesBridge 是一个伴侣应用，而不是真正嵌入 Notes 内部的扩展。

当前实现刻意保持保守：

- 行内增强依赖辅助功能权限和事件合成，因此直装版是完整体验的主要载体。
- 可通过 `NOTESBRIDGE_APPSTORE=1` 模拟 App Store 版本；该模式会禁用 Apple Notes 行内增强，但保留设置和同步能力。
- 当前主要同步方向仍然是 Apple Notes -> Obsidian。
- slash command 菜单键盘导航可能需要 Input Monitoring；如果拦截不可用，精确命令加空格和鼠标点选仍然可用。
- 全量同步会提示你选择 macOS 的 `group.com.apple.notes` 数据目录，以便 NotesBridge 直接读取 Apple Notes 数据库和附件文件。

## 构建与运行

```bash
./scripts/run-bundled-app.sh
```

这是推荐的开发入口。它会构建 SwiftPM 可执行文件，将其包装为已签名的 `NotesBridge.app`，并从 `~/Library/Application Support/NotesBridge/NotesBridge.app` 启动该 bundle。

当前 bundled app 使用稳定的 designated requirement，因此辅助功能和 Input Monitoring 权限在重建之后仍可持续绑定。如果你此前授予的是旧版 NotesBridge，而应用仍显示 `Required`，请在系统设置中删除旧条目后重新添加当前 bundled app。

如果只是快速进行非 bundle 运行，也可以使用：

```bash
swift run
```

但 `swift run` 启动的是裸可执行文件，因此依赖真实 app bundle 的 macOS 权限流程，尤其是 slash 菜单键盘导航所需的 Input Monitoring，在这种模式下不会正常工作。

如果你只想重建 `.app` 而不立刻启动：

```bash
./scripts/run-bundled-app.sh --build-only
```

首次以 bundled 方式启动时，macOS 可能会请求辅助功能和自动化权限，以便 NotesBridge 观察 Apple Notes 并同步内容。第一次全量同步还会要求你选择 `~/Library/Group Containers/group.com.apple.notes`，以便应用读取 `NoteStore.sqlite` 和二进制附件。

## 建议的下一步

1. 强化多显示器与全屏空间下的选区锚点、slash 菜单定位以及格式工具条定位。
2. 增加更丰富的同步索引和增量笔记变更跟踪能力，减少全量导出中的重复工作。
3. 完成正式的签名与 notarization 直装版发布链路，再决定是否值得单独长期维护真正的 App Store 交付物。

## License

MIT。见 [LICENSE](./LICENSE)。
