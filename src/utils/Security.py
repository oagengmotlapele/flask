import base64
import json
import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from cryptography.fernet import Fernet, InvalidToken
class Security:
    def __init__(self):
        self.system_users = [
            # System Owners & Developers (65Bugs Pty Ltd)
            'System Owner (65Bugs Pty Ltd)',
            'Project Manager',
            'Business Analyst',
            'System Architect',
            'Lead Developer',
            'Backend Developer',
            'Frontend Developer',
            'Mobile App Developer',
            'Database Administrator',
            'DevOps Engineer',
            'System Administrator',
            'QA Tester',
            'UI/UX Designer',
            'Technical Support Specialist',
            'Trainer / User Support',
            'Cybersecurity Specialist',

            # Ministry & HQ Level
            'Minister of Education',
            'Permanent Secretary',
            'Deputy Permanent Secretary',
            'Chief Education Officer',
            'Regional/District Education Officer',
            'School Inspector',
            'Policy Maker',
            'Curriculum Developer',

            # School Management
            'School Principal',
            'Vice Principal',
            'Head of House (Head of Department)',
            'Head of Subject (Senior Teacher)',
            'School Administrator',
            'Bursar/Finance Officer',
            'Exams Officer',
            'Records Clerk',

            # Teaching & Academic Staff
            'Teacher',
            'Assistant Teacher',
            'Teacher Aide',
            'Guidance and Counselling Teacher',
            'Librarian',

            # Students & Parents
            'Student',
            'Parent',
            'Guardian',
            'Alumni',

            # Support & Operations
            'School Nurse',
            'Counsellor',
            'Sports Coordinator',
            'Lab Technician',
            'IT Technician',
            'Cleaner',
            'Security Guard',

            # External Stakeholders
            'Education NGO Representative',
            'Government Auditor',
            'Researcher',
            'Donor/Partner Organization',
        ]

        load_dotenv()
        self.key = os.environ.get("app_secrect")
        self.fernet = Fernet(self.generate_supported_fernet_key(self.key))
        self.salt = self.key

    def generate_supported_fernet_key(self,raw_key: str) -> bytes:
        """
        Takes any string and returns a valid 32-byte base64-encoded Fernet key.
        Pads or truncates as needed, handles non-ASCII characters.
        """
        # Encode to bytes (UTF-8)
        key_bytes = raw_key.encode('utf-8')

        # Truncate or pad to 32 bytes
        if len(key_bytes) < 32:
            key_bytes = key_bytes.ljust(32, b'0')  # pad with zeros
        else:
            key_bytes = key_bytes[:32]  # truncate to 32 bytes

        # Base64 encode to make it Fernet-compatible
        fernet_key = base64.urlsafe_b64encode(key_bytes)

        return fernet_key

    def create_session(self, user_id, user_role):
        """
        Creates an encrypted session dict with automatic expiry.
        Returns encrypted string.
        """
        session = {
            "user_id": user_id,
            "user_role": user_role,
            "date_and_time_of_login": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=1)).isoformat()
        }
        # Convert dict to JSON string
        session_json = json.dumps(session)
        # Encrypt JSON string
        encrypted = self.fernet.encrypt(session_json.encode())
        return encrypted

    def decrypt_session(self, encrypted_data):
        """
        Decrypts and verifies session.
        Automatically checks expiry.
        Returns session dict if valid, else None.
        """
        try:
            # Decrypt
            decrypted_bytes = self.fernet.decrypt(encrypted_data)
            session = json.loads(decrypted_bytes.decode())
            # Check expiry
            expires_at = datetime.fromisoformat(session["expires_at"])
            if datetime.now() > expires_at:
                return None  # Session expired
            return session
        except (InvalidToken, TypeError, ValueError):
            # Invalid or tampered session
            return None

    def role_rights(self,rights:dict) -> dict:
        pass
    def usr_id_rights(self,rights:dict) -> dict:
        pass

security = Security()
f=security.create_session(1,"IT Help desk")
print(f)
print(security.decrypt_session(f))
