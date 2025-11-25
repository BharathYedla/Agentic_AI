from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
import os
from auth import Token, authenticate_user, create_access_token, fake_users_db, get_current_user, User
from services.erp import ERPService
from services.tms import TMSService
from services.wms import WMSService
from agents.orchestrator import ControlTowerAgent

app = FastAPI(title="ForksSupplies Agentic AI")

# Initialize Services
erp_service = ERPService()
tms_service = TMSService()
wms_service = WMSService()

# Initialize Agent
agent = ControlTowerAgent(erp_service, tms_service, wms_service)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- API Endpoints ---

@app.get("/api/agent/analyze")
async def run_agent_analysis(current_user: User = Depends(get_current_user)):
    return agent.analyze_network()

@app.get("/api/shipments")
async def get_shipments(current_user: User = Depends(get_current_user)):
    return tms_service.get_all_shipments()

@app.get("/api/orders/{order_id}")
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    return erp_service.get_order_details(order_id)

@app.get("/api/inventory/{sku}")
async def get_inventory(sku: str, current_user: User = Depends(get_current_user)):
    return wms_service.get_inventory(sku)

# --- Pages ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # In a real app, we'd check the cookie or header here, but for MVP we'll handle auth in JS or via a dependency if we want strict server-side rendering checks.
    # For this MVP, we'll serve the page and let JS redirect if no token.
    return templates.TemplateResponse("index.html", {"request": request, "title": "ForksSupplies Control Tower"})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/login")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
