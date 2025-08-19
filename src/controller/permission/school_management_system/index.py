from src.controller.users.SchoolManagementSystem import SchoolManagementSystem


class Index:
    def __init__(self):
        pass
    def root(self):
        for i in SchoolManagementSystem().get_all_users():
            data={
                "add": "System Owner",
                "update": "<EMAIL>",
                "delete": "0812345678",
                "view": "123 Main Street, Lagos, Nigeria"
            }