"""Cost analytics helpers using Azure Cost Management."""

import datetime as _dt
from datetime import timezone
from typing import Any, Iterable

from azure.mgmt.costmanagement import CostManagementClient

from .credentials import get_flask_credential


class CostAnalyzer:
    """Retrieve cost details for a subscription."""

    def __init__(self, subscription_id: str) -> None:
        credential = get_flask_credential()
        self._client = CostManagementClient(credential)
        self._scope = f"subscriptions/{subscription_id}"

    @staticmethod
    def _column_names(result: Any) -> list[str]:
        # result.columns is a list of QueryColumn objects; extract .name
        try:
            return [getattr(col, "name", str(col)) for col in result.columns]
        except Exception:
            return list(result.columns)

    @staticmethod
    def _find_date_key(result: Any, names: list[str]) -> str:
        # Prefer explicit known names
        for key in ("UsageDate", "Date", "UsageDateTime", "BillingDate"):
            if key in names:
                return key
        # Try to find by column type if available
        try:
            for col in result.columns:
                if getattr(col, "type", "").lower() in ("datetime", "date"):
                    return getattr(col, "name")
        except Exception:
            pass
        # Fallback to first column
        return names[0] if names else "Date"

    @staticmethod
    def _find_cost_key(names: list[str]) -> str:
        for key in ("Cost", "totalCost", "PreTaxCost", "Amount"):
            if key in names:
                return key
        # Fallback to last column
        return names[-1] if names else "Cost"

    def actual_cost_last_month(self) -> list[dict]:
        """Return daily cost data for the previous month, normalized to keys UsageDate and Cost."""

        today: _dt.date = _dt.date.today().replace(day=1)
        start: _dt.date = (today - _dt.timedelta(days=1)).replace(day=1)
        end: _dt.date = today - _dt.timedelta(days=1)

        # Convert to datetime with timezone for proper ISO format
        start_dt = _dt.datetime.combine(start, _dt.time.min, tzinfo=timezone.utc)
        end_dt = _dt.datetime.combine(end, _dt.time.max, tzinfo=timezone.utc)

        query: dict[str, object] = {
            "type": "Usage",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start_dt.isoformat(),
                "to": end_dt.isoformat(),
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
            },
        }

        result = self._client.query.usage(scope=self._scope, parameters=query)
        names = self._column_names(result)
        date_key = self._find_date_key(result, names)
        cost_key = self._find_cost_key(names)
        idx_date = names.index(date_key)
        idx_cost = names.index(cost_key)

        normalized: list[dict] = []
        for row in result.rows:
            try:
                normalized.append({
                    "UsageDate": row[idx_date],
                    "Cost": float(row[idx_cost] or 0),
                })
            except Exception:
                # Best-effort fallback using pairwise mapping
                row_map = {names[i]: row[i] for i in range(min(len(names), len(row)))}
                normalized.append({
                    "UsageDate": row_map.get(date_key),
                    "Cost": float(row_map.get(cost_key) or 0),
                })
        return normalized

    def cost_per_resource_group(self) -> list[dict]:
        """Return cost by resource group aggregated daily for the previous month.
        Normalized to keys: date, resource_group, cost.
        """

        today: _dt.date = _dt.date.today().replace(day=1)
        start: _dt.date = (today - _dt.timedelta(days=1)).replace(day=1)
        end: _dt.date = today - _dt.timedelta(days=1)

        # Convert to datetime with timezone for proper ISO format
        start_dt = _dt.datetime.combine(start, _dt.time.min, tzinfo=timezone.utc)
        end_dt = _dt.datetime.combine(end, _dt.time.max, tzinfo=timezone.utc)

        query: dict[str, object] = {
            "type": "Usage",
            "timeframe": "Custom",
            "timePeriod": {"from": start_dt.isoformat(), "to": end_dt.isoformat()},
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
                "grouping": [{"type": "Dimension", "name": "ResourceGroupName"}],
            },
        }

        result = self._client.query.usage(scope=self._scope, parameters=query)
        names = self._column_names(result)
        date_key = self._find_date_key(result, names)
        cost_key = self._find_cost_key(names)
        rg_key = "ResourceGroupName" if "ResourceGroupName" in names else ("ResourceGroup" if "ResourceGroup" in names else None)

        # Build indices where possible
        idx_date = names.index(date_key)
        idx_cost = names.index(cost_key)
        idx_rg = names.index(rg_key) if rg_key else None

        output: list[dict] = []
        for row in result.rows:
            try:
                resource_group_value = row[idx_rg] if idx_rg is not None else None
                output.append({
                    "date": row[idx_date],
                    "resource_group": resource_group_value or "Unknown",
                    "cost": float(row[idx_cost] or 0),
                })
            except Exception:
                row_map = {names[i]: row[i] for i in range(min(len(names), len(row)))}
                output.append({
                    "date": row_map.get(date_key),
                    "resource_group": row_map.get(rg_key) or "Unknown",
                    "cost": float(row_map.get(cost_key) or 0),
                })
        return output

