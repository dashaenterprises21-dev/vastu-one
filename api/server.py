from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from api.config import API_TITLE, API_DESCRIPTION, API_VERSION
from api.routes import vastu_routes, devata_routes, pdf_routes, report_routes, upload_routes, auth_routes, user_routes, payment_routes, chakra_routes, plan_analyze_routes
from api.dependencies import get_all_devatas, get_elements_data
from api.models.schemas import HealthOut

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(vastu_routes.router)
app.include_router(devata_routes.router)
app.include_router(pdf_routes.router)
app.include_router(report_routes.router)
app.include_router(upload_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(payment_routes.router)
app.include_router(chakra_routes.router)
app.include_router(plan_analyze_routes.router)

# Frontend static files
BASE = Path(__file__).resolve().parent.parent
FRONTEND = BASE / "frontend"

if FRONTEND.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND / "static"), name="static")

    @app.get("/", include_in_schema=False)
    def frontend_home():
        return FileResponse(FRONTEND / "index.html")
else:
    @app.get("/", tags=["Root"])
    def root():
        return {"message": "Vastu AI Engine is running", "docs": "/docs"}


@app.get("/health", response_model=HealthOut, tags=["Health"])
def health():
    return {
        "status": "ok",
        "version": API_VERSION,
        "total_devatas": len(get_all_devatas()),
        "total_elements": len(get_elements_data()["elements"])
    }

@app.get("/report/{report_id}", include_in_schema=False)
def serve_report(report_id: str):
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "report.html")

@app.get("/upload", include_in_schema=False)
def serve_upload_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "upload.html")



@app.get("/chakra-form", include_in_schema=False)
def chakra_form_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "chakra-form.html")

# ═══ DATABASE INIT ═══
@app.on_event("startup")
def startup_event():
    from database.db import init_db
    init_db()
    print("[INFO] Vastu One API started")

@app.get("/login", include_in_schema=False)
def login_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "login.html")


@app.get("/signup", include_in_schema=False)
def signup_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "signup.html")

@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "dashboard.html")

@app.get("/pricing", include_in_schema=False)
def pricing_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "pricing.html")

@app.get("/reports", include_in_schema=False)
def reports_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "reports.html")

@app.get("/rooms-form", include_in_schema=False)
def rooms_form_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "rooms-form.html")



@app.get("/chakra-overlay", include_in_schema=False)
def chakra_overlay_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "chakra-overlay.html")



@app.get("/plan-report/{report_id}", include_in_schema=False)
def plan_report_page(report_id: str):
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "plan-report.html")



@app.get("/plan-upload", include_in_schema=False)
def plan_upload_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "plan-upload.html")



@app.get("/profile", include_in_schema=False)
def profile_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "profile.html")


@app.get("/settings", include_in_schema=False)
def settings_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "settings.html")


@app.get("/help", include_in_schema=False)
def help_page():
    from fastapi.responses import FileResponse
    return FileResponse(FRONTEND / "help.html")