from __future__ import annotations

import os
from pathlib import Path

from cleanup_tool.config import AppConfig
from cleanup_tool.domain.models import CleanupItem


class WindowsCleanupRules:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    @classmethod
    def from_root(cls, root_dir: Path) -> "WindowsCleanupRules":
        return cls(AppConfig(root_dir=root_dir, report_path=root_dir / "cleanup-report.md", system_drive=root_dir))

    def rules(self) -> list[CleanupItem]:
        system_drive = self.config.system_drive or self._default_system_drive()
        local = Path(os.environ.get("LOCALAPPDATA", ""))
        roaming = Path(os.environ.get("APPDATA", ""))
        temp = Path(os.environ.get("TEMP", ""))
        user = Path(os.environ.get("USERPROFILE", ""))
        codex = roaming / "Codex"
        tencent = roaming / "Tencent" / "xwechat"
        local_openai_codex = local / "OpenAI" / "Codex"
        local_google_chrome = local / "Google" / "Chrome"
        local_google_chrome_user_data = local_google_chrome / "User Data"
        local_google_chrome_default = local_google_chrome_user_data / "Default"
        local_google_chrome_safe_browsing = local_google_chrome_user_data / "Safe Browsing"
        local_google_chrome_optimization_guide = local_google_chrome_user_data / "optimization_guide_model_store"
        local_google_chrome_component_cache = local_google_chrome_user_data / "component_crx_cache"
        local_google_chrome_wasm_tts = local_google_chrome_user_data / "WasmTtsEngine"
        local_google_chrome_grshader = local_google_chrome_user_data / "GrShaderCache"
        local_google_chrome_shader = local_google_chrome_user_data / "ShaderCache"
        local_google_chrome_graphite = local_google_chrome_user_data / "GraphiteDawnCache"
        local_edge = local / "Microsoft" / "Edge"
        local_edge_user_data = local_edge / "User Data"
        local_edge_default = local_edge_user_data / "Default"
        local_edge_component_cache = local_edge_user_data / "component_crx_cache"
        local_edge_provenance = local_edge_user_data / "ProvenanceData"
        local_edge_wallet = local_edge_user_data / "Edge Wallet"
        local_edge_subresource = local_edge_user_data / "Subresource Filter"
        local_edge_grshader = local_edge_user_data / "GrShaderCache"
        local_edge_entity = local_edge_user_data / "Edge Entity Extraction"
        local_edge_shopping = local_edge_user_data / "Edge Shopping"
        local_edge_safe_browsing = local_edge_user_data / "Safe Browsing"
        local_edge_metrics = local_edge_user_data / "BrowserMetrics"
        local_edge_metrics_spare = local_edge_user_data / "BrowserMetrics-spare.pma"
        local_edge_language_model = local_edge_user_data / "EdgeLanguageDetectionModel"
        local_edge_speech = local_edge_user_data / "Speech Recognition"
        local_edge_shader = local_edge_user_data / "ShaderCache"
        local_edge_provenance_tensors = local_edge_user_data / "ProvenanceDataTensors"
        local_edge_sidebar = local_edge_user_data / "Edge Sidebar"
        local_edge_signal = local_edge_user_data / "Edge Signal Triggers"
        local_edge_smartscreen = local_edge_user_data / "SmartScreen"
        local_rider = local / "JetBrains" / "Rider2025.2"
        local_rider_full_line = local_rider / "full-line"
        local_rider_caches = local_rider / "caches"
        local_rider_resharper = local_rider / "resharper-host"
        local_rider_index = local_rider / "index"
        local_rider_jcef = local_rider / "jcef_cache"
        local_rider_log = local_rider / "log"
        local_rider_plugins = local_rider / "plugins"
        local_rider_projects = local_rider / "projects"
        local_rider_local_history = local_rider / "LocalHistory"
        local_rider_vcs_log = local_rider / "vcs-log"
        local_rider_vcs_users = local_rider / "vcs-users"
        local_rider_tmp = local_rider / "tmp"
        local_rider_icon_cache = local_rider / "icon-cache-v1.db"
        local_comet = local / "Perplexity" / "Comet"
        local_comet_application = local_comet / "Application"
        local_comet_user_data = local_comet / "User Data"
        local_comet_default = local_comet_user_data / "Default"
        local_comet_grshader = local_comet_user_data / "GrShaderCache"
        local_comet_metrics = local_comet_user_data / "BrowserMetrics"
        local_comet_crash_metrics = local_comet_user_data / "CrashpadMetrics-active.pma"
        local_comet_graphite = local_comet_user_data / "GraphiteDawnCache"
        local_comet_shader = local_comet_user_data / "ShaderCache"
        local_comet_extensions_cache = local_comet_user_data / "extensions_crx_cache"
        local_comet_updater = local / "Perplexity" / "CometUpdater"
        local_comet_updater_crx = local_comet_updater / "crx_cache"
        local_comet_updater_version = local_comet_updater / "145.2.7632.4583"
        local_comet_updater_log = local_comet_updater / "updater.log"
        local_comet_updater_log_old = local_comet_updater / "updater.log.old"
        local_comet_updater_hist = local_comet_updater / "updater_history.jsonl"
        local_comet_updater_hist_old = local_comet_updater / "updater_history.jsonl.old"
        local_tsc = local / "Microsoft" / "Terminal Server Client"
        local_tsc_cache = local_tsc / "Cache"
        local_fontcache = local / "Microsoft" / "FontCache"
        programs_antigravity = local / "Programs" / "antigravity"
        programs_antigravity_ide = local / "Programs" / "Antigravity IDE"

        green = [
            CleanupItem("Green", "Temp", temp, "系统临时文件", "Safe to clean", category="temp"),
            CleanupItem("Green", "LocalAppData Temp", local / "Temp", "应用临时文件", "Safe to clean", category="temp"),
            CleanupItem("Green", "Windows Temp", Path("C:/Windows/Temp"), "系统临时文件", "Safe to clean", category="temp"),
            CleanupItem("Green", "Windows Update Download", Path("C:/Windows/SoftwareDistribution/Download"), "Windows Update 缓存", "Safe to clean", category="system-cache"),
            CleanupItem("Green", "pip Cache", local / "pip" / "Cache", "Python 包缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "uv Cache", local / "uv", "uv 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "Yarn Cache", local / "Yarn", "Yarn 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "Playwright Cache", local / "ms-playwright", "Playwright 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "Go Build Cache", local / "go-build", "Go 编译缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".cache", user / ".cache", "常见开发缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".npm", user / ".npm", "npm 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".gradle", user / ".gradle", "Gradle 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".m2", user / ".m2", "Maven 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".cargo", user / ".cargo", "Rust 缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", ".nuget packages", user / ".nuget" / "packages", ".NET 包缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "NuGet v3 cache", local / "NuGet" / "v3-cache", "NuGet 包缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "Azure Functions Releases", local / "AzureFunctionsTools" / "Releases", "Azure Functions 发布包缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "pnpm metadata", local / "pnpm-cache" / "metadata-v1.3", "pnpm 元数据缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "pnpm full metadata", local / "pnpm-cache" / "metadata-full-v1.3", "pnpm 全量元数据缓存", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "zig temp", local / "zig" / "tmp", "zig 临时文件", "Safe to clean", category="dev-cache"),
            CleanupItem("Green", "Microsoft FontCache", local_fontcache, "字体缓存", "Safe to clean", category="system-cache"),
            CleanupItem("Green", "Terminal Server Client Cache", local_tsc_cache, "远程桌面缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Chrome Safe Browsing", local_google_chrome_safe_browsing, "Chrome 安全浏览缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome optimization guide", local_google_chrome_optimization_guide, "Chrome 模型缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome component cache", local_google_chrome_component_cache, "Chrome 组件缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome WasmTtsEngine", local_google_chrome_wasm_tts, "Chrome 语音模型缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome GrShaderCache", local_google_chrome_grshader, "Chrome 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome ShaderCache", local_google_chrome_shader, "Chrome 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Chrome GraphiteDawnCache", local_google_chrome_graphite, "Chrome 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge component cache", local_edge_component_cache, "Edge 组件缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Subresource Filter", local_edge_subresource, "Edge 过滤缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge GrShaderCache", local_edge_grshader, "Edge 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Entity Extraction", local_edge_entity, "Edge 提取模型缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Shopping", local_edge_shopping, "Edge 购物缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Safe Browsing", local_edge_safe_browsing, "Edge 安全浏览缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge BrowserMetrics", local_edge_metrics, "Edge 指标缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge BrowserMetrics spare", local_edge_metrics_spare, "Edge 指标缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge language model", local_edge_language_model, "Edge 语言模型缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Speech Recognition", local_edge_speech, "Edge 语音缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge ShaderCache", local_edge_shader, "Edge 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Sidebar", local_edge_sidebar, "Edge 侧边栏缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge Signal Triggers", local_edge_signal, "Edge 信号缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Edge SmartScreen", local_edge_smartscreen, "Edge SmartScreen 缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Codex Cache", codex / "Cache", "Codex 缓存目录", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex GPUCache", codex / "GPUCache", "Codex 图形缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex DawnGraphiteCache", codex / "DawnGraphiteCache", "Codex 图形缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex DawnWebGPUCache", codex / "DawnWebGPUCache", "Codex 图形缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex Code Cache", codex / "Code Cache", "Codex 代码缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex Crashpad", codex / "Crashpad", "Codex 崩溃报告", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Codex blob_storage", codex / "blob_storage", "Codex 临时存储", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider caches", local_rider_caches, "Rider 索引缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider index", local_rider_index, "Rider 索引目录", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider jcef_cache", local_rider_jcef, "Rider 嵌入式浏览器缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider log", local_rider_log, "Rider 日志目录", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider tmp", local_rider_tmp, "Rider 临时目录", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider icon cache", local_rider_icon_cache, "Rider 图标缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider vcs-log", local_rider_vcs_log, "Rider VCS 日志缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Rider vcs-users", local_rider_vcs_users, "Rider VCS 用户缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "CometUpdater crx_cache", local_comet_updater_crx, "Comet 更新器扩展缓存", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "CometUpdater log", local_comet_updater_log, "Comet 更新器日志", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "CometUpdater log old", local_comet_updater_log_old, "Comet 更新器旧日志", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "CometUpdater history", local_comet_updater_hist, "Comet 更新器历史日志", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "CometUpdater history old", local_comet_updater_hist_old, "Comet 更新器旧历史日志", "Safe to clean", category="app-cache"),
            CleanupItem("Green", "Comet GrShaderCache", local_comet_grshader, "Comet 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Comet BrowserMetrics", local_comet_metrics, "Comet 指标缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Comet CrashpadMetrics", local_comet_crash_metrics, "Comet 崩溃指标缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Comet GraphiteDawnCache", local_comet_graphite, "Comet 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Comet ShaderCache", local_comet_shader, "Comet 图形缓存", "Safe to clean", category="browser-cache"),
            CleanupItem("Green", "Comet extensions cache", local_comet_extensions_cache, "Comet 扩展缓存", "Safe to clean", category="browser-cache"),
        ]

        yellow = [
            CleanupItem("Yellow", "Downloads", user / "Downloads", "下载目录可能含用户文件", "Review before cleaning", category="downloads"),
            CleanupItem("Yellow", "Desktop", user / "Desktop", "桌面通常含用户文件", "Review before cleaning", category="user-data"),
            CleanupItem("Yellow", "Documents", user / "Documents", "文档目录通常含用户文件", "Review before cleaning", category="user-data"),
            CleanupItem("Yellow", "Roaming AppData", roaming, "应用配置和用户数据", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Local AppData", local, "应用数据和缓存混合", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "pnpm dlx", local / "pnpm-cache" / "dlx", "pnpm dlx 目录可能混合缓存和临时安装内容", "Review before cleaning", category="dev-cache"),
            CleanupItem("Yellow", "pnpm v11", local / "pnpm-cache" / "v11", "pnpm 内容寻址缓存，通常可重建但建议先确认", "Review before cleaning", category="dev-cache"),
            CleanupItem("Yellow", "zig p", local / "zig" / "p", "zig 包缓存，通常可重建但可能影响下次构建速度", "Review before cleaning", category="dev-cache"),
            CleanupItem("Yellow", "zig o", local / "zig" / "o", "zig 输出缓存，通常可重建但建议先确认", "Review before cleaning", category="dev-cache"),
            CleanupItem("Yellow", "zig z", local / "zig" / "z", "zig 缓存目录，通常可重建但建议先确认", "Review before cleaning", category="dev-cache"),
            CleanupItem("Yellow", "Roaming uv python", roaming / "uv" / "python", "uv 管理的 Python 运行时", "Review before cleaning", category="tooling"),
            CleanupItem("Yellow", "Roaming uv tools", roaming / "uv" / "tools", "uv 管理的工具环境", "Review before cleaning", category="tooling"),
            CleanupItem("Yellow", "Codex web", codex / "web", "Codex 本地 Web 资源和状态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Codex Local Storage", codex / "Local Storage", "Codex 本地存储", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Codex Session Storage", codex / "Session Storage", "Codex 会话存储", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Codex Network", codex / "Network", "Codex 网络状态与 Cookie 类数据", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Codex Preferences", codex / "Preferences", "Codex 配置文件", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Codex Local State", codex / "Local State", "Codex 全局状态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Local OpenAI Codex", local_openai_codex, "OpenAI Codex 本地目录，混合缓存与状态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Chrome User Data", local_google_chrome_user_data, "Chrome 用户数据目录，混合缓存、配置与登录态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Chrome Default profile", local_google_chrome_default, "Chrome 主配置目录，混合登录态、数据库与缓存", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Edge User Data", local_edge_user_data, "Edge 用户数据目录，混合缓存、配置与登录态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Edge Default profile", local_edge_default, "Edge 主配置目录，混合登录态、数据库与缓存", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Edge ProvenanceData", local_edge_provenance, "Edge 大型本地数据目录，建议先确认", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Edge Wallet", local_edge_wallet, "Edge 钱包数据", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Edge ProvenanceDataTensors", local_edge_provenance_tensors, "Edge 模型张量数据", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Rider full-line", local_rider_full_line, "Rider AI/模型相关数据，建议先确认", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Rider resharper-host", local_rider_resharper, "Rider ReSharper 主机数据，建议先确认", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Rider plugins", local_rider_plugins, "Rider 插件数据", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Rider projects", local_rider_projects, "Rider 项目缓存与状态", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Rider LocalHistory", local_rider_local_history, "Rider 本地历史", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Comet User Data", local_comet_user_data, "Comet 用户数据目录", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Comet Default profile", local_comet_default, "Comet 主配置目录，混合状态与缓存", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "CometUpdater version files", local_comet_updater_version, "Comet 更新器版本目录，建议先确认", "Review before cleaning", category="appdata"),
            CleanupItem("Yellow", "Terminal Server Client", local_tsc, "远程桌面客户端目录，混合缓存与历史", "Review before cleaning", category="appdata"),
        ]

        red = [
            CleanupItem("Red", "Program Files", system_drive / "Program Files", "应用本体，不建议手删", "Use uninstaller", category="apps"),
            CleanupItem("Red", "Program Files (x86)", system_drive / "Program Files (x86)", "应用本体，不建议手删", "Use uninstaller", category="apps"),
            CleanupItem("Red", "Windows", system_drive / "Windows", "系统目录，不要手删", "Use Disk Cleanup or DISM", category="system"),
            CleanupItem("Red", "Programs antigravity", programs_antigravity, "应用安装目录，不建议手删", "Use uninstaller", category="apps"),
            CleanupItem("Red", "Programs Antigravity IDE", programs_antigravity_ide, "应用安装目录，不建议手删", "Use uninstaller", category="apps"),
            CleanupItem("Red", "OpenAI Codex bin", local_openai_codex / "bin", "Codex 本地二进制目录，更像应用本体，不建议手删", "Use uninstaller or reinstall", category="apps"),
            CleanupItem("Red", "Comet Application", local_comet_application, "Comet 应用本体目录，不建议手删", "Use uninstaller", category="apps"),
            CleanupItem("Red", "Tencent xwechat", tencent, "微信数据主目录，可能包含聊天记录、文件和索引，不建议自动清理", "Clean inside the app", category="appdata"),
        ]

        return green + yellow + red

    def _default_system_drive(self) -> Path:
        drive = os.environ.get("SystemDrive", "C:")
        return Path(drive + "\\")
