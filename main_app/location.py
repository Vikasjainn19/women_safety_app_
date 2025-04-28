# location.py (Cleaned Version)
import requests
import logging

logger = logging.getLogger(__name__)

def get_location_info():
    """Fetches approximate location info from ipinfo.io (used as fallback only)."""
    try:
        res = requests.get('https://ipinfo.io/', timeout=10)
        res.raise_for_status()
        data = res.json()
        lat, lon = data.get('loc', ',').split(',')
        city = data.get('city')
        state = data.get('region')
        location = data.get('loc')
        return lat, lon, location, city, state
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Location fetch failed: {e}")
        return None, None, None, None, None
