###############################################################################
# Imports
###############################################################################

from __future__ import annotations

###############################################################################
# API Version
###############################################################################

API_NAME: str = "Wallet DNA API"

API_VERSION: str = "1.0.0"

API_PREFIX: str = "/api/v1"

API_DESCRIPTION: str = (
    "Wallet DNA Intelligence API for funding analysis, "
    "wallet clustering, graph analytics, deployer reputation, "
    "bundle detection, Wallet DNA scoring, and real-time "
    "on-chain intelligence."
)

###############################################################################
# Build Information
###############################################################################

BUILD_NUMBER: str = "001"

BUILD_DATE: str = "2026-07-21"

BUILD_ENVIRONMENT: str = "development"

BUILD_AUTHOR: str = "Wallet DNA Team"


###############################################################################
# Git Information
###############################################################################

# These values are typically injected by CI/CD during deployment.

GIT_COMMIT: str = "unknown"

GIT_BRANCH: str = "main"

GIT_TAG: str = "v1.0.0"

GIT_DIRTY: bool = False

###############################################################################
# Release Information
###############################################################################

RELEASE_NAME: str = "Genesis"

RELEASE_STAGE: str = "development"
# development | staging | production

RELEASE_DATE: str = "2026-07-21"

CHANGELOG_VERSION: str = "v1.0.0"


###############################################################################
# Runtime
###############################################################################

import platform
import sys

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # Python <3.8 compatibility
    from importlib_metadata import version, PackageNotFoundError


def python_version() -> str:
    """
    Return current Python version.
    """

    return sys.version


###############################################################################


def platform_version() -> dict[str, str]:
    """
    Return platform information.
    """

    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


###############################################################################


def dependency_versions() -> dict[str, str]:
    """
    Return versions of important runtime dependencies.
    """

    packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "redis",
        "neo4j",
    ]

    versions: dict[str, str] = {}

    for package in packages:

        try:

            versions[package] = version(package)

        except PackageNotFoundError:

            versions[package] = "not installed"

    return versions


###############################################################################


def runtime_metadata() -> dict:
    """
    Runtime environment metadata.
    """

    return {
        "python": python_version(),
        "platform": platform_version(),
        "dependencies": dependency_versions(),
    }

###############################################################################
# API Metadata
###############################################################################

def openapi_metadata() -> dict:
    """
    Metadata used by FastAPI/OpenAPI.
    """

    return {
        "title": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
    }


###############################################################################


def server_metadata() -> dict:
    """
    Server metadata.
    """

    return {
        "name": API_NAME,
        "prefix": API_PREFIX,
        "environment": BUILD_ENVIRONMENT,
        "release": RELEASE_STAGE,
    }


###############################################################################


def version_metadata() -> dict:
    """
    Complete version metadata.
    """

    return {
        "api_version": API_VERSION,
        "build_number": BUILD_NUMBER,
        "build_date": BUILD_DATE,
        "release_name": RELEASE_NAME,
        "release_stage": RELEASE_STAGE,
        "git_commit": GIT_COMMIT,
        "git_branch": GIT_BRANCH,
        "git_tag": GIT_TAG,
    }


###############################################################################


def health_metadata() -> dict:
    """
    Health/version payload.
    """

    return {
        "status": "healthy",
        "version": API_VERSION,
        "build": BUILD_NUMBER,
        "environment": BUILD_ENVIRONMENT,
    }


###############################################################################
# Utilities
###############################################################################

def semantic_version() -> tuple[int, int, int]:
    """
    Parse semantic version.
    """

    major, minor, patch = API_VERSION.split(".")

    return (
        int(major),
        int(minor),
        int(patch),
    )


###############################################################################


def short_commit() -> str:
    """
    Short Git commit hash.
    """

    return GIT_COMMIT[:7]


###############################################################################


def full_version() -> str:
    """
    Human-readable version string.
    """

    return (
        f"{API_NAME} "
        f"{API_VERSION} "
        f"({RELEASE_STAGE}) "
        f"[{short_commit()}]"
    )


###############################################################################


def summary() -> dict:
    """
    Version summary.
    """

    return {
        "application": API_NAME,
        "version": API_VERSION,
        "release": RELEASE_NAME,
        "stage": RELEASE_STAGE,
        "build": BUILD_NUMBER,
        "commit": short_commit(),
    }

###############################################################################
# Diagnostics
###############################################################################

def diagnostics() -> dict:
    """
    Complete diagnostics for the version module.
    """

    return {
        "summary": summary(),
        "version": version_metadata(),
        "server": server_metadata(),
        "runtime": runtime_metadata(),
        "health": health_metadata(),
    }


###############################################################################


def export_version() -> dict:
    """
    Export complete version information.

    Used by:
      • /version endpoint
      • /health endpoint
      • diagnostics
      • monitoring
    """

    return {
        "application": API_NAME,
        "description": API_DESCRIPTION,
        "api_prefix": API_PREFIX,

        "version": API_VERSION,
        "semantic_version": semantic_version(),

        "build": {
            "number": BUILD_NUMBER,
            "date": BUILD_DATE,
            "environment": BUILD_ENVIRONMENT,
            "author": BUILD_AUTHOR,
        },

        "release": {
            "name": RELEASE_NAME,
            "stage": RELEASE_STAGE,
            "date": RELEASE_DATE,
            "changelog": CHANGELOG_VERSION,
        },

        "git": {
            "commit": GIT_COMMIT,
            "short_commit": short_commit(),
            "branch": GIT_BRANCH,
            "tag": GIT_TAG,
            "dirty": GIT_DIRTY,
        },

        "runtime": runtime_metadata(),
    }    

