# 项目规范

## 日志

- `info` 只记录关键流程节点。
- `warning` 记录可恢复问题。
- `error` 记录失败和上下文。
- 用户输出和日志分离。

## 异常

- 业务异常统一继承 `CleanupToolError`。
- CLI 只处理项目异常，不处理散落的原生异常。
- 删除失败必须返回明确错误信息。

## CLI

- 子命令固定：`scan`、`report`、`html`、`apply`
- 默认只读，`apply` 必须显式 `--yes`
- 报告先生成，再执行清理

## 结构

- `rules` 只放规则。
- `scanner` 只负责扫描。
- `summary_service` 只负责汇总。
- `markdown_reporter` 只负责 Markdown 输出。
- `html_reporter` 只负责 HTML 输出。
- `cleaner` 只负责删除。
- `orchestrator` 只负责编排。
- `domain` 只放领域模型。
- `system` 只放系统信息和统计。
- `app.py` 只负责装配。
- `cli.py` 只负责命令入口。
