"""Classifies activity logs into high-level categories based on process names and window titles/URLs."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

from src.historical.domain.model import ActivityCategory
from src.historical.domain.model import ActivityLogs
from src.historical.domain.model import ClassifiedActivity


@dataclass
class ProcessRule:
    """Matches a process name (exact or prefix) to a category."""

    process: str
    category: ActivityCategory
    match_prefix: bool = False


@dataclass
class WindowRule:
    """Matches window title / URL substring to a category."""

    substring: str
    category: ActivityCategory


class ActivityClassifier:
    """Classifies activity logs into high-level categories.

    Rules are data-driven and can be extended via configuration.
    """

    def __init__(
        self,
        process_rules: list[ProcessRule] | None = None,
        window_rules: list[WindowRule] | None = None,
    ) -> None:
        """Initialize the classifier with optional custom rules."""
        self.process_rules = process_rules or self._default_process_rules()
        self.window_rules = window_rules or self._default_window_rules()

    def classify(self, log: ActivityLogs) -> ActivityCategory:
        """Classify a single activity log into a category."""
        process = (log.process or "").lower()
        window = (log.window_title or "").lower()

        category = (
            self._classify_system(process, window)
            or self._classify_by_process(process)
            or self._classify_by_window(window)
            or self._classify_browser_heuristic(process, window)
        )
        return category or ActivityCategory.MISC

    @staticmethod
    def _classify_system(process: str, window: str) -> ActivityCategory | None:
        if process in ("[pause]", "[resume]") or window in ("[pause]", "[resume]"):
            return ActivityCategory.BREAK_IDLE
        return None

    def _classify_by_process(self, process: str) -> ActivityCategory | None:
        for process_rule in self.process_rules:
            rp = process_rule.process.lower()
            if process_rule.match_prefix and process.startswith(rp):
                return process_rule.category
            if not process_rule.match_prefix and process == rp:
                return process_rule.category
        return None

    def _classify_by_window(self, window: str) -> ActivityCategory | None:
        for window_rule in self.window_rules:
            if window_rule.substring.lower() in window:
                return window_rule.category
        return None

    def _classify_browser_heuristic(self, process: str, window: str) -> ActivityCategory | None:
        if process not in ("chrome", "chromium", "brave", "edge", "safari", "firefox"):
            return None
        domain = self._extract_domain(window)
        if not domain:
            return None
        if self._is_social_domain(domain):
            return ActivityCategory.SOCIAL_ENTERTAINMENT
        if self._is_dev_docs_domain(domain):
            return ActivityCategory.DOC_RESEARCH_WORK_WEB
        return ActivityCategory.OTHER_WEB

    def classify_logs(
        self,
        device_id: str,
        logs: Iterable[ActivityLogs],
        start_time: datetime,
        stop_time: datetime,
    ) -> list[ClassifiedActivity]:
        """Classify a list of activity logs into classified activities."""
        classified: list[ClassifiedActivity] = []

        for log in logs:
            start = max(log.start_time, start_time)
            stop = log.stop_time or stop_time
            stop = min(stop, stop_time)
            if stop <= start:
                continue

            duration = round((stop - start).total_seconds())
            category = self.classify(log)

            classified.append(
                ClassifiedActivity(
                    device_id=device_id,
                    start_time=start,
                    stop_time=stop,
                    process=log.process,
                    window_title=log.window_title,
                    category=category,
                    duration_seconds=duration,
                ),
            )

        return classified

    @staticmethod
    def _default_process_rules() -> list[ProcessRule]:
        return [
            # Coding IDEs / editors
            ProcessRule(process="vscode", category=ActivityCategory.CODING),
            ProcessRule(process="code", category=ActivityCategory.CODING),
            ProcessRule(process="pycharm", category=ActivityCategory.CODING, match_prefix=True),
            ProcessRule(process="idea", category=ActivityCategory.CODING, match_prefix=True),
            # DB tools
            ProcessRule(process="sequel-ace", category=ActivityCategory.DB_TECH),
            ProcessRule(process="sequel-pro", category=ActivityCategory.DB_TECH),
            ProcessRule(process="pgadmin", category=ActivityCategory.DB_TECH),
            ProcessRule(process="dbeaver", category=ActivityCategory.DB_TECH),
            # DevOps / Git / terminals
            ProcessRule(process="iterm2", category=ActivityCategory.DEVOPS_GIT),
            ProcessRule(process="terminal", category=ActivityCategory.DEVOPS_GIT),
            ProcessRule(process="wezterm", category=ActivityCategory.DEVOPS_GIT),
            ProcessRule(process="sourcetree", category=ActivityCategory.DEVOPS_GIT),
            ProcessRule(process="gitkraken", category=ActivityCategory.DEVOPS_GIT),
            # Meetings / calls
            ProcessRule(process="teams", category=ActivityCategory.MEETINGS_CALLS, match_prefix=True),
            ProcessRule(process="teams2", category=ActivityCategory.MEETINGS_CALLS, match_prefix=True),
            ProcessRule(process="zoom", category=ActivityCategory.MEETINGS_CALLS, match_prefix=True),
            ProcessRule(process="slack", category=ActivityCategory.MEETINGS_CALLS, match_prefix=True),
            ProcessRule(process="google meet", category=ActivityCategory.MEETINGS_CALLS, match_prefix=True),
            ProcessRule(process="discord", category=ActivityCategory.SOCIAL_ENTERTAINMENT, match_prefix=True),
            # Internal / other tools can be added here...
        ]

    @staticmethod
    def _default_window_rules() -> list[WindowRule]:
        return [
            # Work / docs / research web
            WindowRule(substring="trello.com", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="jira", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="github.com", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="gitlab.com", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="notion.so", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="confluence", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="metodostandup.it", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="onrender.com", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="chatgpt.com", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            WindowRule(substring="tc2services.app", category=ActivityCategory.DOC_RESEARCH_WORK_WEB),
            # DB related web
            WindowRule(substring="mongodb.com", category=ActivityCategory.DB_TECH),
            WindowRule(substring="supabase.com", category=ActivityCategory.DB_TECH),
            WindowRule(substring="neon.tech", category=ActivityCategory.DB_TECH),
            # Social / entertainment web
            WindowRule(substring="youtube.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="tiktok.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="instagram.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="facebook.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="twitter.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="x.com", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
            WindowRule(substring="whatsapp", category=ActivityCategory.SOCIAL_ENTERTAINMENT),
        ]

    @staticmethod
    def _extract_domain(window_title: str) -> str | None:
        """Best-effort domain extractor from a window title that contains a URL."""
        if not window_title:
            return None
        # crude heuristic: if it contains '/', treat as URL
        if "http://" in window_title or "https://" in window_title:
            try:
                url = window_title.split()[0]
                parsed = urlparse(url)
                return parsed.netloc.lower()
            except Exception:  # noqa: BLE001
                return None
        # simple domain-like detection (very naive)
        parts = window_title.split()
        for p in parts:
            if "." in p and not p.startswith("["):
                return p.lower()
        return None

    @staticmethod
    def _is_social_domain(domain: str) -> bool:
        social = ("youtube.com", "tiktok.com", "instagram.com", "facebook.com", "twitter.com", "x.com")
        return any(domain.endswith(d) for d in social)

    @staticmethod
    def _is_dev_docs_domain(domain: str) -> bool:
        dev = ("github.com", "gitlab.com", "bitbucket.org", "vercel.com", "render.com", "onrender.com")
        return any(domain.endswith(d) for d in dev)
