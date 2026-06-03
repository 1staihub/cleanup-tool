# cleanup-tool

一个用 `uv` 管理的 Python 清理审计项目。

当前能力：

- 扫描系统盘垃圾、缓存、临时文件和大目录
- 生成中文报告
- 在确认后执行安全清理

## 项目结构

```text
cleanup-tool/
  pyproject.toml
  README.md
  src/
    cleanup_tool/
      app.py
      cli.py
      config.py
      exceptions.py
      interfaces.py
      logging_utils.py
      orchestrator.py
      templates/
      domain/
      rules/
      scanning/
      reporting/
      cleaning/
      system/
```

## 当前可用命令

```bash
uv sync
uv run cleanup-tool scan --root "C:\"
uv run cleanup-tool report --root "C:\"
uv run cleanup-tool html --root "C:\"
uv run cleanup-tool apply --root "C:\" --yes
uv run cleanup-tool drilldown --path "C:\Users\Administrator\AppData\Local"
uv run cleanup-tool drilldown --path "C:\Users\Administrator\AppData\Roaming"
```

默认报告文件写到当前目录的 `cleanup-report.md`。

推荐先验证：

```bash
uv run cleanup-tool scan --root "C:\"
uv run cleanup-tool report --root "C:\"
uv run cleanup-tool html --root "C:\"
```

`drilldown` 适合继续细分 `AppData\Local`、`AppData\Roaming`、缓存目录等大项，
用来判断哪些目录应该升级成更细粒度的绿灯、黄灯或红灯规则。

## 规范

请先看 [CONTRIBUTING.md](CONTRIBUTING.md)。
