"""
IP Geolocation utilities
Get country, city, and ISP information from IP addresses
"""
import httpx
from typing import Optional, Dict
from datetime import datetime, timedelta
import asyncio

# Using ip-api.com (free, no API key required)
# Rate limit: 45 requests per minute
IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"

# In-memory cache for IP geolocation results
# Format: {ip_address: (data, expiration_time)}
_geolocation_cache: Dict[str, tuple[Optional[Dict[str, str]], datetime]] = {}
_cache_lock = asyncio.Lock()

# Cache TTL: 24 hours (IP locations rarely change)
CACHE_TTL_HOURS = 24


async def get_ip_geolocation(ip_address: str) -> Optional[Dict[str, str]]:
    """
    Get geolocation data for an IP address (with caching)

    Args:
        ip_address: IP address to lookup

    Returns:
        Dictionary with geolocation data or None if failed
    """
    # Skip localhost and private IPs
    if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
        return {
            'country': 'Local',
            'country_code': 'LOCAL',
            'city': 'Localhost',
            'isp': 'Local Network'
        }

    # Check cache first
    async with _cache_lock:
        if ip_address in _geolocation_cache:
            cached_data, expiration = _geolocation_cache[ip_address]
            if datetime.now() < expiration:
                # Cache hit and not expired
                return cached_data
            else:
                # Cache expired, remove it
                del _geolocation_cache[ip_address]

    # Cache miss or expired, fetch from API
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(IP_API_URL.format(ip=ip_address))

            if response.status_code == 200:
                data = response.json()

                if data.get('status') == 'success':
                    result = {
                        'country': data.get('country'),
                        'country_code': data.get('countryCode'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'zip': data.get('zip'),
                        'lat': data.get('lat'),
                        'lon': data.get('lon'),
                        'timezone': data.get('timezone'),
                        'isp': data.get('isp'),
                        'org': data.get('org'),
                        'as': data.get('as')
                    }

                    # Store in cache
                    async with _cache_lock:
                        expiration = datetime.now() + timedelta(hours=CACHE_TTL_HOURS)
                        _geolocation_cache[ip_address] = (result, expiration)

                    return result
                else:
                    # API returned error, cache None to avoid repeated failed requests
                    async with _cache_lock:
                        expiration = datetime.now() + timedelta(hours=1)  # Shorter TTL for errors
                        _geolocation_cache[ip_address] = (None, expiration)
                    return None
            else:
                return None

    except Exception as e:
        # Log error but don't fail the request
        print(f"IP geolocation error for {ip_address}: {str(e)}")
        return None


def get_cache_stats() -> Dict[str, int]:
    """
    Get cache statistics

    Returns:
        Dictionary with cache size and hit rate info
    """
    return {
        'cache_size': len(_geolocation_cache),
        'cache_limit': 1000  # Soft limit
    }


async def clear_expired_cache():
    """
    Clear expired entries from cache
    Should be called periodically
    """
    async with _cache_lock:
        now = datetime.now()
        expired_keys = [
            ip for ip, (_, expiration) in _geolocation_cache.items()
            if now >= expiration
        ]
        for key in expired_keys:
            del _geolocation_cache[key]

        return len(expired_keys)


def format_location(country: Optional[str], city: Optional[str]) -> str:
    """
    Format location string for display

    Args:
        country: Country name
        city: City name

    Returns:
        Formatted location string
    """
    if country and city:
        return f"{city}, {country}"
    elif country:
        return country
    elif city:
        return city
    else:
        return "Unknown"
