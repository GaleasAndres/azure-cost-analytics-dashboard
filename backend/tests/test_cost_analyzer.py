import sys
import types

class DummyResult:
    columns = ["UsageDate", "ResourceGroupName", "totalCost"]
    rows = [["2024-10-01", "rg1", 1.23], ["2024-10-02", "rg1", 4.56]]

class DummyQuery:
    def usage(self, scope: str, parameters: dict) -> DummyResult:
        return DummyResult()

class DummyClient:
    def __init__(self, credential: object) -> None:
        self.query = DummyQuery()

class DummyCredential:
    pass


def test_cost_per_resource_group(monkeypatch):
    dummy_core = types.ModuleType("azure.core")
    dummy_creds = types.ModuleType("azure.core.credentials")
    dummy_creds.AccessToken = object
    dummy_creds.TokenCredential = object
    dummy_core.credentials = dummy_creds

    monkeypatch.setitem(sys.modules, "azure.core", dummy_core)
    monkeypatch.setitem(sys.modules, "azure.core.credentials", dummy_creds)

    dummy_mod = types.SimpleNamespace(CostManagementClient=DummyClient)
    monkeypatch.setitem(sys.modules, "azure.mgmt.costmanagement", dummy_mod)

    from backend.azure import cost as cost_module

    monkeypatch.setattr(cost_module, "get_flask_credential", lambda: DummyCredential())

    analyzer = cost_module.CostAnalyzer("sub1")
    result = analyzer.cost_per_resource_group()

    assert result == [
        {"date": "2024-10-01", "resource_group": "rg1", "cost": 1.23},
        {"date": "2024-10-02", "resource_group": "rg1", "cost": 4.56},
    ]
