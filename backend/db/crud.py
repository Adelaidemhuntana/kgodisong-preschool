import sqlite3
import datetime

class view_data:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        
    def get_parents(self):
        self.cursor.execute("SELECT * FROM Parents")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def get_children(self):
        self.cursor.execute("""SELECT c.First_name,c.surname,c.date_of_birth,c.School,c.Grade,c.Class, p.First_name 
                            FROM Children c 
                            join Parents p on p.Parent_id_number = c.Parent_id""")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def get_teachers(self):
        self.cursor.execute("SELECT * FROM Teachers")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def get_bookings(self):
        self.cursor.execute("SELECT * FROM Bookings")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def get_absence_logs(self):
        self.cursor.execute("SELECT * FROM Absence_logs")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)




class Children:
    def __init__(self, db_path="database.db"):
         self.db = sqlite3.connect(db_path)
         self.cursor = self.db.cursor()

    # cant add child with no linked parent
    def add_child(self,children):
        self.cursor.executemany("""
                            INSERT INTO Children(Child_id_number,First_name,Surname,
                            Date_of_birth,School,Grade,Class,Parent_id)
                            values(?,?,?,?,?,?,?,?)""",children)
        self.db.commit()
        print(f"child added")

        
    def remove_child(self,child_id_number):
        self.cursor.execute("DELETE FROM Children WHERE Child_id_number = ?",(child_id_number,))
        self.db.commit()
        print("child removed")

    def update_child_info(self):
        pass

class Teacher:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def add_teacher(self,Teacher):
        self.cursor.executemany("""
                            INSERT INTO Teachers(Teacher_id_number,First_name,
                            Surname,Email)
                            values(?,?,?,?)""",Teacher)
        self.db.commit()
        print(f"teacher added")
        
    def remove_teacher(self,teacher_id_number):
        self.cursor.execute("DELETE FROM Teachers WHERE Teacher_id_number = ?",(teacher_id_number,))
        self.db.commit()
        print("teacher removed")

    def update_teacher_info(self):
        pass

class Parent:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def add_parent(self,Parent):
        self.cursor.executemany("""
                            INSERT INTO Parents(Parent_id_number,First_name,Surname,
                            Phone_number,Email)
                            values(?,?,?,?,?)""",Parent)
        self.db.commit()
        print(f"parent added")
        
    def remove_parent(self,parent_id_number):
        self.cursor.execute("DELETE FROM Parents WHERE Parent_id_number = ?",(parent_id_number,))
        self.db.commit()
        print("parent removed")

    def update_parent_info(self):
        pass


class Bookings:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def create_booking(self,child_id, booking_type_id, booking_date):
        self.cursor.execute("""INSERT INTO Bookings (child_id, booking_type_id, booking_date)
        values (?, ?, ?)""",(child_id, booking_type_id, booking_date))
        self.db.commit()

    def update_booking_status(self):
        ...

    def cancel_booking(self,child_id,booking_date):
        self.cursor.execute("DELETE FROM Bookings WHERE Child_id = ?  and booking_date = ?",(child_id,booking_date))
        self.db.commit()
        
class Absence_log():
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def log_absence(self,child_id, absence_date, reason , logged_by):
        self.cursor.execute("""INSERT INTO Absence_logs (child_id, absence_date, reason , logged_by)
        values (?, ?, ?, ?)""",(child_id, absence_date, reason , logged_by))
        self.db.commit()

    def view_absence_history(self,child_id = None):
        if child_id != None:
            self.cursor.execute("SELECT * FROM Absence_logs WHERE child_id = ? order by absence_date DESC", (child_id,))
            rows = self.cursor.fetchall()
        else:
            self.cursor.execute("SELECT * FROM Absence_logs")
            rows = self.cursor.fetchall()
        self.db.commit()
        print(rows)
        return rows
    

class Booking_types:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def add_booking_types(self,types):
            self.cursor.executemany("""INSERT INTO Booking_types (Booking_type)
            values (?)""",types)
            self.db.commit()

if __name__ == "__main__":
    ...
        





# child = Children()
# child.add_child(123,"sello","letswalo","2000-07-09","WTC","12","b",12344)
        



