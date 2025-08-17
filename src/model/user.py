import datetime
from dataclasses import dataclass
@dataclass
class UserModel():
    # System Verification Process
    id:int
    username:str
    pass1:str
    pass2:str
    verfication_code: str
    verfication_status: bool
    user_role:str
    # contact
    phone_number:int
    email_address:str
    postal_address:str
    # Personal information
    first_name:str
    last_name:str
    date_of_birth:datetime.datetime
    gender:str
    #Identificatiom of location
    place_of_birth:str
    country:str
    city:str
    home_village:str
    current_location:str
    house_address_or_number:str
    # Identification Document
    camera_photo: bytes
    identity_issue_date: datetime.datetime
    identity_expiry_date: datetime.datetime
    identity_number: int
    identity_card_photo_front_file:bytes
    identity_card_photo_back_file:bytes
    passport_number:int
    passport_photo_file:bytes
    




