from typing import List, Dict

class ERPService:
    """
    Mock Enterprise Resource Planning (ERP) system.
    Source of Truth for: Orders, Customer Priority, Product Details.
    """
    
    def __init__(self):
        self.orders = {
            "PO-999": {
                "order_id": "PO-999",
                "customer": "General Hospital",
                "priority": "CRITICAL",
                "items": [
                    {"sku": "MED-GLOVES-L", "qty": 5000},
                    {"sku": "MED-MASKS-N95", "qty": 2000}
                ],
                "value": 15000.00
            },
            "PO-888": {
                "order_id": "PO-888",
                "customer": "Retail Mart",
                "priority": "STANDARD",
                "items": [
                    {"sku": "GROC-CEREAL", "qty": 1000}
                ],
                "value": 2500.00
            }
        }

    def get_order_details(self, order_id: str) -> Dict:
        return self.orders.get(order_id, {"error": "Order not found"})

    def get_sku_priority(self, sku: str) -> str:
        if "MED" in sku:
            return "CRITICAL"
        return "STANDARD"
