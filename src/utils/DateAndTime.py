from datetime import datetime,timedelta

from sympy.physics.units import years


class DateAndTime:
    def current_date(self):
        now=datetime.now()
        full_date=str(now.strftime("%Y-%m-%d %H:%M:%S"))
        date_only=str(now.strftime("%Y-%m-%d"))
        time_only=str(now.strftime("%H:%M:%S"))
        return [full_date,date_only,time_only]
    def verfication_expiry_time_checker(self,date1:str,num:int):
        date1d=datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date2d = datetime.strptime(self.current_date()[0], "%Y-%m-%d %H:%M:%S")
        if date2d > date1d+timedelta(days=num):
            return "Code Expired Generate new code"
        else:
            return "You passed verification"

