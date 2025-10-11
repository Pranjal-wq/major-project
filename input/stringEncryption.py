# input/stringDecryptor.py
import re

def xor_decrypt(enc_list, key=42):
    """XOR decrypt a list of integers to a string."""
    try:
        return ''.join(chr(c ^ key) for c in enc_list)
    except Exception:
        return None

class StringDecryptor:
    """Detects and decrypts XOR-encrypted strings in code."""
    def __init__(self, key=42):
        self.key = key

    def detect_strings(self, code: str):
        """Detect candidate encrypted strings as list of integers."""
        pattern = re.compile(r'[\[{]([0-9,\s]+)[\]}]')
        results = []
        for match in pattern.finditer(code):
            str_bytes = match.group(1)
            try:
                enc_list = [int(b.strip()) for b in str_bytes.split(',') if b.strip().isdigit()]
                decrypted = xor_decrypt(enc_list, self.key)
                if decrypted and all(32 <= ord(ch) <= 126 for ch in decrypted):
                    results.append({
                        "original": match.group(0),
                        "decrypted": decrypted,
                        "position": match.start(),
                        "reason": "XOR-encrypted string detected and decrypted"
                    })
            except Exception:
                continue
        return results

    def detect_and_clean(self, code: str):
        """Detect encrypted strings, replace them, and return changes and final code."""
        results = self.detect_strings(code)
        cleaned_code = code
        # Apply replacements from end to start to avoid index shifting
        for res in reversed(results):
            start_idx = cleaned_code.find(res['original'])
            if start_idx != -1:
                cleaned_code = cleaned_code[:start_idx] + f'"{res["decrypted"]}"' + cleaned_code[start_idx+len(res['original']):]
                res['cleaned'] = f'"{res["decrypted"]}"'
        return results, cleaned_code