class SchoolManagementSystem:
    def __init__(self):
        self.users :list[str] = [
            # System Owners & Developers (65Bugs Pty Ltd)
            'System Owner',
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
            'UI Or UX Designer',
            'Technical Support Specialist',
            'Trainer Or User Support',
            'Cybersecurity Specialist',

            # Ministry & HQ Level
            'Minister of Education',
            'Permanent Secretary',
            'Deputy Permanent Secretary',
            'Chief Education Officer',
            'Regional Or District Education Officer',
            'School Inspector',
            'Policy Maker',
            'Curriculum Developer',

            # School Management
            'School Principal',
            'Vice Principal',
            'Head of House or Head of Department',
            'Head of Subject or Senior Teacher',
            'School Administrator',
            'Bursar or Finance Officer',
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
            'Donor Or Partner Organization',
        ]
    def get_all_users(self)->list[str]:
        return self.users
    def index(self)->dict:
        # 2. UPDATE (can modify existing content)
        update_content: list[str] = [
            'System Owner', 'Project Manager', 'Lead Developer', 'Frontend Developer',
            'System Administrator', 'UI Or UX Designer', 'School Principal',
            'Vice Principal', 'School Administrator', 'Minister of Education',
            'Chief Education Officer'
        ]

        # 3. DELETE (can remove content)
        delete_content: list[str] = [
            'System Owner', 'Lead Developer', 'System Administrator',
            'School Principal', 'Minister of Education'
        ]

        # 4. INSERT (can add new content)
        insert_content: list[str] = [
            'System Owner', 'Project Manager', 'Frontend Developer',
            'UI Or UX Designer', 'School Administrator', 'School Principal',
            'Vice Principal', 'Curriculum Developer'
        ]

        return {
            "add_only": "System Owner",
            "update_only": "<EMAIL>",
            "delete_only": "0812345678",
            "view_only": "123 Main Street, Lagos, Nigeria"
        }