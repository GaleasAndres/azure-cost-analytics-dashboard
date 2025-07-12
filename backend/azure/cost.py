"""Cost analytics helpers using Azure Cost Management."""

import datetime as _dt

from azure.mgmt.costmanagement import CostManagementClient

from .credentials import get_flask_credential


class CostAnalyzer:
    """Retrieve cost details for a subscription."""

    def __init__(self, subscription_id: str) -> None:
        credential = get_flask_credential()
        self._client = CostManagementClient(credential)
        self._scope = f"subscriptions/{subscription_id}"

    def actual_cost_last_month(self) -> list[dict]:
        """Return daily cost data for the previous month."""

        today: _dt.date = _dt.date.today().replace(day=1)
        start: _dt.date = (today - _dt.timedelta(days=1)).replace(day=1)
        end: _dt.date = today - _dt.timedelta(days=1)

        query: dict[str, object] = {
            "type": "Usage",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start.isoformat(),
                "to": end.isoformat(),
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
            },
        }

        result = self._client.query.usage(scope=self._scope, parameters=query)
        return [dict(zip(result.columns, row)) for row in result.rows]

    def cost_per_resource_group(self) -> list[dict]:
        """Return cost by resource group aggregated daily for the previous month."""

        today: _dt.date = _dt.date.today().replace(day=1)
        start: _dt.date = (today - _dt.timedelta(days=1)).replace(day=1)
        end: _dt.date = today - _dt.timedelta(days=1)

        query: dict[str, object] = {
            "type": "Usage",
            "timeframe": "Custom",
            "timePeriod": {"from": start.isoformat(), "to": end.isoformat()},
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
                "grouping": [{"type": "Dimension", "name": "ResourceGroupName"}],
            },
        }

        result = self._client.query.usage(scope=self._scope, parameters=query)

        columns: list[str] = list(result.columns)
        idx_date: int = columns.index("UsageDate")
        idx_rg: int = columns.index("ResourceGroupName")
        idx_cost: int = columns.index("totalCost")

        return [
            {
                "date": row[idx_date],
                "resource_group": row[idx_rg],
                "cost": row[idx_cost],
            }
            for row in result.rows
        ]

