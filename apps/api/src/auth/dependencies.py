"""
apps/api/src/auth/dependencies.py

Authentication dependencies for FastAPI.
"""

from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.jwt import (
    extract_bearer_token,
    verify_access_token,
)

# Replace with your actual User model + DB session
# from database.session import get_db
# from models.user import User

security = HTTPBearer(auto_error=False)


# ============================================================
# JWT Payload
# ============================================================

def get_current_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Returns decoded JWT payload.
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token = extract_bearer_token(
        f"Bearer {credentials.credentials}"
    )

    return verify_access_token(token)


# ============================================================
# User ID
# ============================================================

def get_current_user_id(
    payload=Depends(get_current_payload),
):
    return payload["sub"]


# ============================================================
# Username
# ============================================================

def get_current_username(
    payload=Depends(get_current_payload),
):
    return payload.get("username")


# ============================================================
# Email
# ============================================================

def get_current_email(
    payload=Depends(get_current_payload),
):
    return payload.get("email")


# ============================================================
# Roles
# ============================================================

def get_current_roles(
    payload=Depends(get_current_payload),
):
    return payload.get("roles", [])


# ============================================================
# Permissions
# ============================================================

def get_current_permissions(
    payload=Depends(get_current_payload),
):
    return payload.get("permissions", [])


# ============================================================
# Admin Only
# ============================================================

def require_admin(
    roles=Depends(get_current_roles),
):
    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )


# ============================================================
# Moderator
# ============================================================

def require_moderator(
    roles=Depends(get_current_roles),
):
    if (
        "admin" not in roles
        and "moderator" not in roles
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator access required",
        )


# ============================================================
# Permission Checker
# ============================================================

def require_permission(permission: str):
    """
    Usage:

    @router.get(...)
    async def route(
        user=Depends(require_permission("trade"))
    ):
        ...
    """

    def dependency(
        permissions=Depends(get_current_permissions),
    ):
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission}",
            )

    return dependency


# ============================================================
# Optional Authentication
# ============================================================

def get_optional_payload(
    credentials: Optional[
        HTTPAuthorizationCredentials
    ] = Depends(security),
):
    """
    Returns None if user is not authenticated.
    """

    if credentials is None:
        return None

    try:
        token = extract_bearer_token(
            f"Bearer {credentials.credentials}"
        )

        return verify_access_token(token)

    except Exception:
        return None


# ============================================================
# Current User (Stub)
# ============================================================

def get_current_user(
    payload=Depends(get_current_payload),
):
    """
    Replace this with your database lookup.

    Example:

    user = db.query(User).filter(
        User.id == payload["sub"]
    ).first()

    if not user:
        raise HTTPException(...)

    return user
    """

    return payload


# ============================================================
# Active User
# ============================================================

def require_active_user(
    user=Depends(get_current_user),
):
    """
    Replace with actual user.active check.
    """

    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="User disabled",
    #     )

    return user


# ============================================================
# Verified User
# ============================================================

def require_verified_user(
    user=Depends(get_current_user),
):
    """
    Replace with actual email verification.
    """

    # if not user.email_verified:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Email not verified",
    #     )

    return user


# ============================================================
# Request Context
# ============================================================

def get_request_ip(
    request: Request,
):
    return request.client.host


def get_user_agent(
    request: Request,
):
    return request.headers.get(
        "user-agent",
        "Unknown",
    )