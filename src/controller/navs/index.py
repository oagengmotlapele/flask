import json
import matplotlib.colors as mcolors

class MenuGenerator:
    def __init__(self):
        # Automatically get all CSS4 colors from Matplotlib
        self.colors = list(mcolors.CSS4_COLORS.keys())

    def get_center_nav(self):
        """Return the center navigation menu"""
        return [
            {"icon": "fa fa-home", "txt": "Home", "href": "/", "depth": 0},
            {
                "icon": "fas fa-briefcase",
                "txt": "About us",
                "href": "#",
                "depth": 1,
                "sub": [
                    {"icon": "fa fa-sign-in", "txt": "Contact", "href": "/contact", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Team", "href": "/team", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Mission", "href": "/team", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Vision", "href": "/vision", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Milestone", "href": "/milestone", "depth": 0},
                ]
            },
            {
                "icon": "fas fa-tools",
                "txt": "Services",
                "href": "#",
                "depth": 2,
                "sub1": [
                    {"icon": "fa fa-sign-in", "txt": "Company Registration", "href": "/contact", "depth": 0},
                    {
                        "icon": "fa fa-sign-in",
                        "txt": "Application Development",
                        "href": "/mobile-application",
                        "depth": 1,
                        "sub": [
                            {"icon": "fa fa-sign-in", "txt": "Mobile Application", "href": "/contact", "depth": 0},
                            {"icon": "fa fa-sign-in", "txt": "Web Application", "href": "/team", "depth": 0},
                        ]
                    },
                    {"icon": "fa fa-sign-in", "txt": "Mission", "href": "/team", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Vision", "href": "/vision", "depth": 0},
                    {"icon": "fa fa-sign-in", "txt": "Milestone", "href": "/milestone", "depth": 0},
                ]
            }
        ]

    def get_right_nav(self):
        """Return the right navigation menu"""
        return [
            {
                "icon": "fas fa-fill-drip",
                "txt": "Theme",
                "href": "#",
                "depth": 1,
                "sub": [{"icon": "fa fa-sign-in", "txt": color, "href": f"/themes/{color}", "depth": 0} for color in self.colors]
            },
            {"icon": "fa fa-sign-in", "txt": "login", "href": "/login", "depth": 0},
            {"icon": "fa fa-user-plus", "txt": "register", "href": "/register", "depth": 0}
        ]

    def get_full_menu(self):
        """Return combined center and right navigation menus"""
        return {
            "center_nav": self.get_center_nav(),
            "right_nav": self.get_right_nav()
        }
