from dataclasses import dataclass
from src.middlewares.auth import Verification
@dataclass
class UserLogin:
    id:int
    username:str
    password:str
@dataclass
class UserVerification:
    id:int
    username:str
    verification_code:str



