import hashlib
import random
import string
from dataclasses import dataclass
import bcrypt
from zeep.xsd import Boolean


@dataclass
class Verification:
    def generate_verification_code(self)->str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def combine_hashed_text(self,*hashed_text):
        combined = ''.join(hashed_text)  # Concatenate all hashed passwords
        final_hashed = hashlib.sha256(combined.encode()).hexdigest()
        return final_hashed

    def verify_encryption(self,encryption1,encryption2)->Boolean:
        if encryption1 == encryption2:return True
        else: return False
    def encrypt_text(self,password):
        password = password
        first = password[:len(password) // 2]
        second = password[len(password) // 2:]
        even_password = ""
        odd_password = ""
        for i, j in enumerate(password):
            if i % 2 == 0:
                even_password += j
            elif i % 2 == 1:
                odd_password += j
        all_hass = []
        all_password = [password, first, second, odd_password, even_password]
        for i in all_password:
            for j in all_password:
                combined = i + j
                all_hass.append(hashlib.sha256(combined.encode()).hexdigest())
        return self.combine_hashed_text(*all_hass)