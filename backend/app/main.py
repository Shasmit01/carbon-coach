"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import close_db, init_db
from app.routers import activities, admin, analytics, auth, chatbot, health

# Event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    # Startup
    print("🚀 Starting application...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("🛑 Shutting down...")
    await close_db()
    print("✅ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware
# app.add_middleware(GZIPMiddleware, minimum_size=1000)  # Temporarily disabled

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rate limiting middleware
class RateLimitMiddleware:
    def __init__(self, app):
        self.app = app
        self.requests = {}

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Get client IP
        client_ip = scope.get("client", ("", 0))[0]

        # Track requests
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Simple rate limiting (10 requests per minute)
        from datetime import datetime, timedelta

        now = datetime.now()
        self.requests[client_ip] = [
            req_time
            for req_time in self.requests[client_ip]
            if now - req_time < timedelta(minutes=1)
        ]

        if len(self.requests[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            # Rate limit exceeded
            async def send_rate_limit_response(message):
                if message["type"] == "http.response.start":
                    message["status"] = 429
                    message["headers"] = [
                        [b"content-type", b"application/json"],
                    ]
                await send(message)

            await send_rate_limit_response(
                {
                    "type": "http.response.start",
                    "status": 429,
                    "headers": [[b"content-type", b"application/json"]],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": b'{"detail": "Rate limit exceeded"}',
                }
            )
            return

        self.requests[client_ip].append(now)

        await self.app(scope, receive, send)


# Register routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(chatbot.router)
app.include_router(analytics.router)
app.include_router(admin.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.API_TITLE,
        "version": "1.0.0",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "detail": exc.detail,
        "status_code": exc.status_code,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
