import re
import urllib.parse

class RuleEngine:
    @staticmethod
    def _levenshtein(s1, s2):
        if len(s1) < len(s2):
            return RuleEngine._levenshtein(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    @staticmethod
    def analyze(url: str, signals: dict) -> dict:
        penalties = 0
        reasons = []

        # Parse domain for typosquatting check
        try:
            domain = urllib.parse.urlparse(url).netloc
            if not domain:
                 domain = url.split('/')[0] # Fallback for non-standard URLs
        except:
             domain = ""

        # Typosquatting Targets
        targets = ["microsoft.com", "google.com", "facebook.com", "apple.com", "amazon.com", "netflix.com", "paypal.com", "instagram.com", "linkedin.com"]
        
        for target in targets:
            # Check if domain looks like target but isn't exact match (and isn't a subdomain of target)
            if target in domain and not domain.endswith(target):
                 # e.g. "microsoft-support.com"
                 pass 
            elif domain != target and not domain.endswith("." + target):
                dist = RuleEngine._levenshtein(domain, target)
                # If distance is small (1 or 2) and ratio of length is high
                if 1 <= dist <= 2 and len(domain) > 5:
                    penalties += 50
                    reasons.append(f"Potential Typosquatting detected: '{domain}' is similar to '{target}'")
                    break
                # Homograph check (simple visual simulation for 'rn')
                if "rn" in domain and target.replace("m", "rn") in domain:
                     penalties += 60
                     reasons.append(f"Homograph Typosquatting detected: '{domain}' attempts to mimic '{target}'")
                     break

        # Rule 1: IP Address
        if signals.get("has_ip"):
            penalties += 40
            reasons.append("URL uses an IP address instead of a domain")

        # Rule 2: Non-HTTPS
        if not signals.get("has_https"):
            penalties += 10
            reasons.append("URL is not using HTTPS")

        # Rule 3: Length
        if signals.get("url_length", 0) > 75:
            penalties += 5
            reasons.append("URL is suspiciously long")

        # Rule 4: Suspicious Keywords
        if signals.get("suspicious_keywords"):
            penalties += 20
            reasons.append(f"Suspicious keywords found: {', '.join(signals.get('suspicious_keywords'))}")

        # Rule 5: Multiple Subdomains
        if signals.get("subdomains_count", 0) > 3:
            penalties += 15
            reasons.append("Excessive number of subdomains")

        # Rule 6: At symbol (@) used to obfuscate
        if "@" in url:
            penalties += 30
            reasons.append("URL contains '@' symbol (often used for obfuscation)")

        return {
            "score_deduction": min(penalties, 100),
            "reasons": reasons
        }
