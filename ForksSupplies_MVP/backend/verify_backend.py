import asyncio
from services.erp import ERPService
from services.tms import TMSService
from services.wms import WMSService
from agents.orchestrator import ControlTowerAgent
from auth import verify_password, get_password_hash, create_access_token, authenticate_user, fake_users_db

async def verify_backend():
    print("--- Verifying Backend Logic ---")
    
    # 1. Auth Verification
    print("\n[1] Testing Authentication...")
    hashed = get_password_hash("secret")
    assert verify_password("secret", hashed) == True, "Password verification failed"
    print("   - Password hashing: OK")
    
    user = authenticate_user(fake_users_db, "johndoe", "secret")
    assert user is not False, "User authentication failed"
    print("   - User authentication: OK")
    
    token = create_access_token(data={"sub": "johndoe"})
    assert len(token) > 0, "Token generation failed"
    print("   - Token generation: OK")

    # 2. Services Verification
    print("\n[2] Testing Mock Services...")
    erp = ERPService()
    tms = TMSService()
    wms = WMSService()
    
    orders = erp.orders
    assert "PO-999" in orders, "ERP missing PO-999"
    print("   - ERP Service: OK")
    
    shipments = tms.get_all_shipments()
    assert len(shipments) >= 2, "TMS missing shipments"
    print("   - TMS Service: OK")
    
    inventory = wms.get_inventory("MED-GLOVES-L")
    assert inventory["sku"] == "MED-GLOVES-L", "WMS missing inventory"
    print("   - WMS Service: OK")

    # 3. Agent Verification
    print("\n[3] Testing Control Tower Agent...")
    agent = ControlTowerAgent(erp, tms, wms)
    alerts = agent.analyze_network()
    
    assert len(alerts) > 0, "Agent failed to generate alerts"
    alert = alerts[0]
    assert alert["shipment_id"] == "SH-101", "Agent missed delayed shipment"
    assert "Expedite" in alert["resolution_proposal"], "Agent resolution logic failed"
    print("   - Agent Logic: OK")
    
    print("\n--- All Backend Checks Passed ---")

if __name__ == "__main__":
    asyncio.run(verify_backend())
