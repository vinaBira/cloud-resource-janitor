import json
from pathlib import Path

from app.models import CloudResource

class MockCollector:
    def __init__(self, inventory_path:Path | None = None) ->None:
        project_root = Path(__file__).resolve().parents[2]

        self.inventory_path = inventory_path or project_root / "data" / "mock_inventory.json"
    
    def collect(self) -> list[CloudResource]:
        """Return the validated mock resource inventory."""
        with self.inventory_path.open("r", encoding="utf-8",) as inventory_file:
            raw_resources = json.load(inventory_file)

        if not isinstance(raw_resources, list):
            raise ValueError("Mock inventory must be a list of resources.")

        return [
            CloudResource.model_validate(resource) for resource in raw_resources
        ]