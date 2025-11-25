from typing import List, Dict
from services.erp import ERPService
from services.tms import TMSService
from services.wms import WMSService

class ControlTowerAgent:
    """
    The 'Digital Worker' that orchestrates data across systems.
    """
    
    def __init__(self, erp: ERPService, tms: TMSService, wms: WMSService):
        self.erp = erp
        self.tms = tms
        self.wms = wms

    def analyze_network(self) -> List[Dict]:
        """
        Scans all shipments, identifies issues, and proposes resolutions.
        """
        shipments = self.tms.get_all_shipments()
        alerts = []

        for shipment in shipments:
            if shipment["status"] == "DELAYED":
                # 1. Get Order Context from ERP
                order_id = shipment["order_id"]
                order = self.erp.get_order_details(order_id)
                
                # 2. Determine Priority
                priority = order.get("priority", "STANDARD")
                
                # 3. Check Inventory Impact (WMS)
                impact_analysis = []
                for item in order.get("items", []):
                    sku = item["sku"]
                    inventory = self.wms.get_inventory(sku)
                    # Simple logic: check if we have stock in a backup warehouse (e.g., NYC)
                    # In a real app, we'd check distance to destination.
                    backup_stock = inventory.get("warehouses", {}).get("WH-NYC", {}).get("qty", 0)
                    impact_analysis.append({
                        "sku": sku,
                        "backup_stock_nyc": backup_stock
                    })

                # 4. Formulate Resolution
                resolution = "Monitor situation."
                if priority == "CRITICAL":
                    resolution = "RECOMMENDATION: Expedite replacement from WH-NYC via Air Freight. Estimated Cost: $500."
                
                alerts.append({
                    "type": "DELAY_ALERT",
                    "severity": "HIGH" if priority == "CRITICAL" else "MEDIUM",
                    "shipment_id": shipment["shipment_id"],
                    "customer": order.get("customer"),
                    "delay_reason": shipment["delay_reason"],
                    "impact": f"Delayed {shipment['delay_hours']} hours. Critical items: {len(impact_analysis)}",
                    "resolution_proposal": resolution
                })
        
        return alerts
