from __future__ import annotations

from datetime import datetime
from pathlib import Path

from cleanup_tool.domain.models import CleanupItem, CleanupSummary
from cleanup_tool.system import SystemInfo


class MarkdownReporter:
    def __init__(self, report_path: Path) -> None:
        self.report_path = report_path

    def write_markdown(self, system: SystemInfo, summary: CleanupSummary, items: list[CleanupItem]) -> Path:
        top5 = sorted(items, key=lambda item: item.size_bytes, reverse=True)[:5]
        lines: list[str] = [
            "# 清理扫描报告",
            "",
            f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 系统概览",
            "",
            f"- 系统：{system.os_name}",
            f"- 用户：{system.user}",
            f"- 主盘：{system.drive_name}",
            f"- 容量：{system.disk_total} / {system.disk_used} / {system.disk_free}",
            "",
            "## 执行建议",
            "",
            self._overview(summary, top5),
            "",
            "## Top 5 占用项",
            "",
        ]
        for index, item in enumerate(top5, start=1):
            lines.append(f"{index}. {item.name} - {self._human_size(item.size_bytes)} - {item.reason}")
        lines.extend(
            [
                "",
                "## 结论",
                "",
                f"可直接清理项合计约 {self._human_size(summary.green_bytes)}，需要确认项合计约 {self._human_size(summary.yellow_bytes)}，谨慎清理项合计约 {self._human_size(summary.red_bytes)}。",
                "",
            ]
        )
        lines.extend(self._render_section("绿灯：可直接清理", "Green", items))
        lines.extend(self._render_section("黄灯：建议先确认", "Yellow", items))
        lines.extend(self._render_section("红灯：谨慎清理", "Red", items))
        lines.extend(
            [
                "## 说明",
                "",
                "- 这份报告只扫描本机路径，不会做删除。",
                "- 绿色项目才会进入自动清理。",
                "- 黄色项目需要你先确认。",
                "- 红色项目建议使用系统工具或卸载器处理。",
                "",
                "## 长期建议",
                "",
                "- 定期清理临时目录和开发缓存。",
                "- 用系统自带磁盘清理或存储感知处理系统垃圾。",
                "- 大文件和下载内容建议分流到独立目录或外置盘。",
                "",
            ]
        )
        self.report_path.write_text("\n".join(lines), encoding="utf-8")
        return self.report_path

    def _overview(self, summary: CleanupSummary, top5: list[CleanupItem]) -> str:
        if not top5:
            return "未扫描到明显占用项。"
        lead = top5[0]
        return f"最大占用主要来自 {lead.name}。建议先清理绿色项约 {self._human_size(summary.green_bytes)}，再人工确认黄色项约 {self._human_size(summary.yellow_bytes)}。"

    def _render_section(self, title: str, tier: str, items: list[CleanupItem]) -> list[str]:
        section: list[str] = [f"## {title}", ""]
        scoped = sorted((item for item in items if item.tier == tier), key=lambda x: x.size_bytes, reverse=True)
        if not scoped:
            section.extend(["无", ""])
            return section
        for item in scoped:
            section.extend(
                [
                    f"- **{item.name}**",
                    f"  - 路径：`{item.path}`",
                    f"  - 大小：{self._human_size(item.size_bytes)}",
                    f"  - 说明：{item.reason}",
                    f"  - 处理：{item.action}",
                    "",
                ]
            )
        return section

    def _human_size(self, num: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(num)
        for unit in units:
            if value < 1024 or unit == "TB":
                return f"{value:.2f} {unit}" if unit != "B" else f"{int(value)} B"
            value /= 1024
        return f"{value:.2f} TB"
