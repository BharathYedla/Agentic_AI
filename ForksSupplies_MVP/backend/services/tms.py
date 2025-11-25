from typing import List, Dict
from datetime import datetime, timedelta

class TMSService:
    """
    Mock Transportation Management System (TMS).
    Source of Truth for: Shipments, Locations, Carriers, ETAs.
    """
    
    def __init__(self):
        self.shipments = {
            "SH-101": {
                "shipment_id": "SH-101",
                "order_id": "PO-999",
                "carrier": "FastTrack Logistics",
                "status": "DELAYED",
                "current_location": "Chicago, IL",
                "eta_original": (datetime.now() + timedelta(hours=2)).isoformat(),
                "eta_revised": (datetime.now() + timedelta(hours=6)).isoformat(),
                "delay_reason": "Weather - Heavy Snow",
                "delay_hours": 4
            },
            "SH-102": {
                "shipment_id": "SH-102",
                "order_id": "PO-888",
                "carrier": "SlowMo Trucking",
                "status": "ON_TIME",
                "current_location": "St. Louis, MO",
                "eta_original": (datetime.now() + timedelta(hours=5)).isoformat(),
                "eta_revised": (datetime.now() + timedelta(hours=5)).isoformat(),
                "delay_reason": None,
                "delay_hours": 0
            }
        }

    def get_shipment_status(self, shipment_id: str) -> Dict:
        return self.shipments.get(shipment_id, {"error": "Shipment not found"})

    def get_all_shipments(self) -> List[Dict]:
        return list(self.shipments.values())
