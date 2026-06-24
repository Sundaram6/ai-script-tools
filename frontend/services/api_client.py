import httpx
import logging

BACKEND_URL = "http://localhost:8000"

def generate_monologue(params: dict) -> dict:
    try:
        response = httpx.post(f"{BACKEND_URL}/generate", json=params, timeout=60.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error generating monologue: {e}")
        return {"success": False, "error": "Could not connect to backend server."}

def regenerate_monologue(params: dict) -> dict:
    try:
        response = httpx.post(f"{BACKEND_URL}/regenerate", json=params, timeout=60.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error regenerating monologue: {e}")
        return {"success": False, "error": "Could not connect to backend server."}

def get_history(limit: int = 10) -> list:
    try:
        response = httpx.get(f"{BACKEND_URL}/history", params={"limit": limit}, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        return []

def get_health() -> dict:
    try:
        response = httpx.get(f"{BACKEND_URL}/health", timeout=5.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching health: {e}")
        return {"status": "error"}

def get_analytics() -> dict:
    try:
        response = httpx.get(f"{BACKEND_URL}/analytics", timeout=10.0)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching analytics: {e}")
        return {}
