"""Aggregates classified activity logs into summaries."""

from collections import defaultdict
from collections.abc import Iterable
from datetime import date
from datetime import datetime
from urllib.parse import urlparse

from src.historical.classifier import ActivityClassifier
from src.historical.domain.model import ActivityCategory
from src.historical.domain.model import ActivityCategoryComponentSummary
from src.historical.domain.model import ActivityCategorySummary
from src.historical.domain.model import ActivityLogs
from src.historical.domain.model import ActivitySummaryResult
from src.historical.domain.model import ClassifiedActivity
from src.historical.domain.model import DailyActivitySummary
from src.settings import get_logger

logger = get_logger()


class ActivityAggregator:
    """Aggregates activity logs into durations per category and per day."""

    def __init__(self, classifier: ActivityClassifier | None = None) -> None:
        """Initialize the aggregator with an optional classifier."""
        self.classifier = classifier or ActivityClassifier()

    @staticmethod
    def _make_window_bucket(activity: ClassifiedActivity) -> str:
        """Return a normalized window bucket for composition analysis.

        Args:
            activity: ClassifiedActivity instance.

        Returns:
            A string representing the window bucket. For browsers, this is a
            best-effort domain extraction (e.g., `youtube.com`). For native
            apps, this is a normalized window title.
        """
        process = (activity.process or "").lower()
        title = (activity.window_title or "").strip()

        if process in {"chrome", "chromium", "edge", "brave", "firefox", "safari"}:
            # Try to extract a domain name
            if "http://" in title or "https://" in title:
                try:
                    url = title.split()[0]
                    parsed = urlparse(url)
                    if parsed.netloc:
                        return parsed.netloc.lower()
                except Exception:
                    logger.exception(f"Failed to parse URL from title: {title}")
            # Fallback: pick something that looks like a domain
            for token in title.split():
                if "." in token and not token.startswith("["):
                    return token.lower()
            return "(browser:unknown)"

        # For native applications, just normalize the window title
        if not title:
            return "(no-title)"

        return title.lower()

    def _aggregate_activities(
        self,
        activities: Iterable[ClassifiedActivity],
    ) -> tuple[float, list[ActivityCategorySummary]]:
        total_seconds = sum(a.duration_seconds for a in activities) or 0.0

        cat_totals: dict[ActivityCategory, float] = defaultdict(float)
        cat_counts: dict[ActivityCategory, int] = defaultdict(int)
        cat_components_seconds: dict[ActivityCategory, dict[tuple[str, str], float]] = defaultdict(
            lambda: defaultdict(float),
        )
        cat_components_count: dict[ActivityCategory, dict[tuple[str, str], int]] = defaultdict(
            lambda: defaultdict(int),
        )

        for activity in activities:
            cat_totals[activity.category] += activity.duration_seconds
            cat_counts[activity.category] += 1

            bucket = self._make_window_bucket(activity)
            key = ((activity.process or "").lower(), bucket)
            cat_components_seconds[activity.category][key] += activity.duration_seconds
            cat_components_count[activity.category][key] += 1

        categories_summary: list[ActivityCategorySummary] = []
        for category, seconds in cat_totals.items():
            pct_global = (seconds / total_seconds * 100.0) if total_seconds > 0 else 0.0

            comp_summaries: list[ActivityCategoryComponentSummary] = []
            components = cat_components_seconds[category]
            for (proc, bucket), comp_seconds in components.items():
                pct_of_cat = (comp_seconds / seconds * 100.0) if seconds > 0 else 0.0
                comp_summaries.append(
                    ActivityCategoryComponentSummary(
                        process=proc,
                        window_bucket=bucket,
                        total_seconds=comp_seconds,
                        percentage_of_category=round(pct_of_cat, 2),
                        entries_count=cat_components_count[category][(proc, bucket)],
                    ),
                )

            categories_summary.append(
                ActivityCategorySummary(
                    category=category,
                    total_seconds=seconds,
                    percentage=round(pct_global, 2),
                    entries_count=cat_counts[category],
                    components=comp_summaries,
                ),
            )

        return total_seconds, categories_summary

    def _aggregate_by_day(
        self,
        activities: Iterable[ClassifiedActivity],
    ) -> list[DailyActivitySummary]:
        by_day: dict[date, list[ClassifiedActivity]] = defaultdict(list)
        for a in activities:
            by_day[a.start_time.date()].append(a)

        days_summary: list[DailyActivitySummary] = []
        for day, day_activities in sorted(by_day.items(), key=lambda x: x[0]):
            total_day, cat_summaries = self._aggregate_activities(day_activities)
            days_summary.append(
                DailyActivitySummary(
                    day=day,
                    total_seconds=total_day,
                    categories=cat_summaries,
                ),
            )

        return days_summary

    def classify_and_aggregate(
        self,
        device_id: str,
        logs: Iterable[ActivityLogs],
        start_time: datetime,
        stop_time: datetime,
        group_by_day: bool = False,
    ) -> ActivitySummaryResult:
        """Classify and aggregate activity logs."""
        classified_activities = self.classifier.classify_logs(
            device_id=device_id,
            logs=logs,
            start_time=start_time,
            stop_time=stop_time,
        )

        total_seconds, categories_summary = self._aggregate_activities(classified_activities)

        days_summary: list[DailyActivitySummary] = []
        if group_by_day:
            days_summary = self._aggregate_by_day(classified_activities)

        return ActivitySummaryResult(
            start_time=start_time,
            stop_time=stop_time,
            group_by="day" if group_by_day else None,
            total_seconds=total_seconds,
            categories=categories_summary,
            days=days_summary,
        )
