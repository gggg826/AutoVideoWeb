"""
IP Geolocation utilities
Get country, city, and ISP information from IP addresses
"""
import httpx
from typing import Optional, Dict

# Using ip-api.com (free, no API key required)
# Rate limit: 45 requests per minute
IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"


async def get_ip_geolocation(ip_address: str) -> Optional[Dict[str, str]]:
    """
    Get geolocation data for an IP address

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

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(IP_API_URL.format(ip=ip_address))

            if response.status_code == 200:
                data = response.json()

                if data.get('status') == 'success':
                    return {
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
                else:
                    # API returned error
                    return None
            else:
                return None

    except Exception as e:
        # Log error but don't fail the request
        print(f"IP geolocation error for {ip_address}: {str(e)}")
        return None


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
