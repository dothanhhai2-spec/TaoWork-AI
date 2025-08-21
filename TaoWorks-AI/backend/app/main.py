from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, presentations, generate

app = FastAPI(title="TaoWorks AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(presentations.router, prefix="/presentations", tags=["presentations"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])

@app.get("/health")
def health():
    return {"ok": True}
