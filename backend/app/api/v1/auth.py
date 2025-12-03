"""
Authentication API routes
Login and token management
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.auth import verify_admin_credentials, create_access_token, verify_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse, summary="Admin login")
async def login(credentials: LoginRequest):
    """
    Admin login endpoint

    Returns JWT access token if credentials are valid
    """
    # Verify credentials
    if not verify_admin_credentials(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": credentials.username, "type": "admin"},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency to get current authenticated admin

    Validates JWT token and returns payload
    """
    token = credentials.credentials
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin resources"
        )

    return payload


@router.get("/verify", summary="Verify token")
async def verify_token(current_admin: dict = Depends(get_current_admin)):
    """
    Verify if current token is valid

    Returns user info if token is valid
    """
    return {
        "success": True,
        "data": {
            "username": current_admin.get("sub"),
            "type": current_admin.get("type")
        }
    }
