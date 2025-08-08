import sys
import types


class QueryColumn:
    def __init__(self, name: str, col_type: str = "string") -> None:
        self.name = name
        self.type = col_type


class DummyResultColsAsStrings:
    columns = ["Date", "totalCost"]
    rows = [
        ["2024-10-01", 1.0],
        ["2024-10-02", 2.5],
    ]


class DummyResultColsAsObjects:
    columns = [QueryColumn("UsageDate", "datetime"), QueryColumn("ResourceGroupName", "string"), QueryColumn("Cost", "number")]
    rows = [
        ["2024-10-01", "rg1", 3.14],
        ["2024-10-02", "rg2", 6.28],
    ]


class DummyQueryStrings:
    def usage(self, scope: str, parameters: dict) -> DummyResultColsAsStrings:
        # Validate expected keys are present in the query
        assert "timePeriod" in parameters
        assert "from" in parameters["timePeriod"]
        assert "to" in parameters["timePeriod"]
        return DummyResultColsAsStrings()


class DummyQueryObjects:
    def usage(self, scope: str, parameters: dict) -> DummyResultColsAsObjects:
        return DummyResultColsAsObjects()


class DummyClientStrings:
    def __init__(self, credential: object) -> None:
        self.query = DummyQueryStrings()


class DummyClientObjects:
    def __init__(self, credential: object) -> None:
        self.query = DummyQueryObjects()


class DummyCredential:
    pass


def _install_dummy_core(monkeypatch):
    dummy_core = types.ModuleType("azure.core")
    dummy_creds = types.ModuleType("azure.core.credentials")
    dummy_creds.AccessToken = object
    dummy_creds.TokenCredential = object
    dummy_core.credentials = dummy_creds
    monkeypatch.setitem(sys.modules, "azure.core", dummy_core)
    monkeypatch.setitem(sys.modules, "azure.core.credentials", dummy_creds)


def test_actual_cost_last_month_with_string_columns(monkeypatch):
    _install_dummy_core(monkeypatch)

    dummy_mod = types.SimpleNamespace(CostManagementClient=DummyClientStrings)
    monkeypatch.setitem(sys.modules, "azure.mgmt.costmanagement", dummy_mod)

    from backend.azure import cost as cost_module

    monkeypatch.setattr(cost_module, "get_flask_credential", lambda: DummyCredential())

    analyzer = cost_module.CostAnalyzer("sub1")
    result = analyzer.actual_cost_last_month()

    assert result == [
        {"UsageDate": "2024-10-01", "Cost": 1.0},
        {"UsageDate": "2024-10-02", "Cost": 2.5},
    ]


def test_cost_per_resource_group_with_querycolumn_objects(monkeypatch):
    _install_dummy_core(monkeypatch)

    dummy_mod = types.SimpleNamespace(CostManagementClient=DummyClientObjects)
    monkeypatch.setitem(sys.modules, "azure.mgmt.costmanagement", dummy_mod)

    from backend.azure import cost as cost_module

    monkeypatch.setattr(cost_module, "get_flask_credential", lambda: DummyCredential())

    analyzer = cost_module.CostAnalyzer("sub1")
    result = analyzer.cost_per_resource_group()

    assert result == [
        {"date": "2024-10-01", "resource_group": "rg1", "cost": 3.14},
        {"date": "2024-10-02", "resource_group": "rg2", "cost": 6.28},
    ]


