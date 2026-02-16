import requests
import logging

logger = logging.getLogger(__name__)

class GeoEnricher:
    def __init__(self):
        self.cache = {}

    def get_location(self, ip_address):
        """
        Returns {'country': 'US', 'city': 'New York'} for a given IP.
        Uses ip-api.com (Free limit: 45 requests/minute).
        """
        # Start simplistic: Ignore local IPs
        if ip_address.startswith("192.168") or ip_address.startswith("10.") or ip_address == "127.0.0.1":
            return {"country": "Local LAN", "city": "Internal"}
        
        if ip_address in self.cache:
            return self.cache[ip_address]

        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,city", timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    result = {
                        "country": data['country'],
                        "city": data['city'],
                        "lat": data.get('lat', 0.0),
                        "lon": data.get('lon', 0.0)
                    }
                    self.cache[ip_address] = result
                    return result
        except Exception as e:
            logger.debug(f"GeoIP failed for {ip_address}: {e}")
        
        return {"country": "Unknown", "city": "Unknown"}
