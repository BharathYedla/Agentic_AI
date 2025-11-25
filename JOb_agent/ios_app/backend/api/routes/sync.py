from fastapi import APIRouter, BackgroundTasks, HTTPException
import sys
import os
from pathlib import Path
import logging

# Add project root to sys.path to allow importing agents
# Current file: ios_app/backend/api/routes/sync.py
# Root: JOb_agent/
current_file = Path(__file__).resolve()
backend_dir = current_file.parent.parent.parent
project_root = backend_dir.parent.parent
print(f"DEBUG: project_root={project_root}")
print(f"DEBUG: agents path exists? {(project_root / 'agents').exists()}")
sys.path.append(str(project_root))

try:
    from agents.orchestrator_agent import create_orchestrator_agent, run_job_tracking_workflow
except ImportError as e:
    print(f"Error importing agents: {e}")
    # Fallback for when running in a different context
    create_orchestrator_agent = None
    run_job_tracking_workflow = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Global state to track sync status
sync_state = {
    "is_running": False,
    "last_run": None,
    "last_status": None,
    "last_result": None
}

def run_sync_task():
    """Background task to run the sync workflow"""
    global sync_state
    
    if not create_orchestrator_agent:
        logger.error("Agents module not found")
        sync_state["is_running"] = False
        sync_state["last_status"] = "failed"
        sync_state["last_result"] = {"error": "Agents module not found"}
        return

    try:
        logger.info("Starting background sync task...")
        orchestrator = create_orchestrator_agent()
        
        # Run workflow (fetch recent emails from last 7 days)
        results = run_job_tracking_workflow(orchestrator, mode='recent', days=7)
        
        sync_state["last_result"] = results
        sync_state["last_status"] = "success"
        logger.info(f"Sync task completed: {results}")
        
    except Exception as e:
        logger.error(f"Sync task failed: {e}", exc_info=True)
        sync_state["last_status"] = "failed"
        sync_state["last_result"] = {"error": str(e)}
        
    finally:
        sync_state["is_running"] = False
        from datetime import datetime
        sync_state["last_run"] = datetime.utcnow().isoformat()

@router.get("/")
async def get_sync_status():
    """Get current sync status"""
    return sync_state

@router.post("/run")
async def trigger_sync(background_tasks: BackgroundTasks):
    """Trigger a manual sync of emails"""
    global sync_state
    
    if sync_state["is_running"]:
        raise HTTPException(status_code=409, detail="Sync already in progress")
    
    sync_state["is_running"] = True
    sync_state["last_status"] = "running"
    
    background_tasks.add_task(run_sync_task)
    
    return {"message": "Sync started", "status": "running"}
