import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    print("Attempting to import main...")
    from main import app
    print("Successfully imported main.")
    
    print("Attempting to import services...")
    from services.erp import ERPService
    from services.tms import TMSService
    from services.wms import WMSService
    print("Successfully imported services.")
    
    print("Attempting to import agents...")
    from agents.orchestrator import ControlTowerAgent
    print("Successfully imported agents.")
    
    print("All imports successful!")

except Exception as e:
    print(f"Caught exception: {e}")
    import traceback
    traceback.print_exc()
