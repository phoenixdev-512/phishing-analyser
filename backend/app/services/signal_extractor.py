import urllib.parse
import re
import socket
from datetime import datetime

class SignalExtractor:
    @staticmethod
    def extract_signals(url: str) -> dict:
        signals = {
            "has_https": False,
            "has_ip": False,
            "url_length": len(url),
            "domain_age_days": None, # Placeholder for whois lookup
            "suspicious_keywords": [],
            "tld": "",
            "subdomains_count": 0
        }

        try:
            parsed = urllib.parse.urlparse(url)
            signals["has_https"] = parsed.scheme == "https"
            signals["tld"] = parsed.netloc.split('.')[-1] if '.' in parsed.netloc else ""
            signals["subdomains_count"] = len(parsed.netloc.split('.')) - 2 # Approx

            # Check for IP address
            try:
                socket.inet_aton(parsed.netloc)
                signals["has_ip"] = True
            except socket.error:
                signals["has_ip"] = False

            # Suspicious keywords
            keywords = ["security", "confirm", "bank", "update", "account", "login", "verify"]
            found_keywords = [kw for kw in keywords if kw in url.lower()]
            signals["suspicious_keywords"] = found_keywords

        except Exception as e:
            print(f"Error extracting signals: {e}")
        
        return signals
