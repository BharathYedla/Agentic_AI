from typing import List, Dict

class WMSService:
    """
    Mock Warehouse Management System (WMS).
    Source of Truth for: Inventory Levels, Warehouse Locations.
    """
    
    def __init__(self):
        self.inventory = {
            "MED-GLOVES-L": {
                "sku": "MED-GLOVES-L",
                "warehouses": {
                    "WH-CHI": {"qty": 0, "status": "OUT_OF_STOCK"},
                    "WH-NYC": {"qty": 10000, "status": "IN_STOCK"},
                    "WH-LAX": {"qty": 5000, "status": "IN_STOCK"}
                }
            },
            "MED-MASKS-N95": {
                "sku": "MED-MASKS-N95",
                "warehouses": {
                    "WH-CHI": {"qty": 500, "status": "LOW_STOCK"},
                    "WH-NYC": {"qty": 2000, "status": "IN_STOCK"}
                }
            }
        }

    def get_inventory(self, sku: str) -> Dict:
        return self.inventory.get(sku, {"error": "SKU not found"})

    def check_stock_coverage(self, sku: str, location: str) -> str:
        item = self.inventory.get(sku)
        if not item:
            return "UNKNOWN"
        wh = item["warehouses"].get(location)
        if not wh:
            return "NO_WAREHOUSE_NEARBY"
        return wh["status"]
