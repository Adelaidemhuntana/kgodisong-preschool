import sqlite3

class Children:
    def __init__(self, db_path="database.db"):
         self.db = sqlite3.connect(db_path)
         self.cursor = self.db.cursor()

    #cant add child with no linked parent
    def add_child(self,child_id_number,name,surname,dob,school,grade,class_,parent_id_number):
        self.cursor.execute("""
                            INSERT INTO Children(Child_id_number,First_name,Surname,
                            Date_of_birth,School,Grade,Class,Parent_id)
                            values(?,?,?,?,?,?,?,?)""",
                            (child_id_number,name,surname,dob,school,grade,class_,parent_id_number))
        self.db.commit()
        print(f"child {name} {surname} added")

        
    def remove_child(self,child_id_number):
        self.cursor.execute("DELETE FROM Children WHERE Child_id_number = ?",(child_id_number))
        self.db.commit()
        print("child removed")

    def update_child_info(self):
        pass

class Teacher:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def add_teacher(self,Teacher_id_number,name,Surname,Email):
        self.cursor.execute("""
                            INSERT INTO Teachers(
                            Teacher_id_number,
                            First_name,
                            Surname,
                            Email,
                            )
                            values(?,?,?,?)""",(Teacher_id_number,name,Surname,Email))
        self.db.commit()
        print(f"teacher {name} {Surname} added")
        
    def remove_teacher(self,teacher_id_number):
        self.cursor.execute("DELETE FROM Teachers WHERE Teacher_id_number = ?",(teacher_id_number))
        self.db.commit()
        print("teacher removed")

    def update_teacher_info(self):
        pass

class Parent:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def add_parent(self,Parent_id_number,name,Surname,phone_number,Email):
        self.cursor.execute("""
                            INSERT INTO Parents(
                            Parent_id_number,
                            First_name,
                            Surname,
                            Phone_number,
                            Email text
                            )
                            values(?,?,?,?,?)""",(Parent_id_number,name,Surname,phone_number,Email))
        self.db.commit()
        print(f"parent {name} {Surname} added")
        
    def remove_parent(self,parent_id_number):
        self.cursor.execute("DELETE FROM Parents WHERE Parent_id_number = ?",(parent_id_number))
        self.db.commit()
        print("parent removed")

    def update_parent_info(self):
        pass


class Bookings:
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def create_booking(self):
        ...

    def update_booking_status(self):
        ...

    def cancel_booking(self):
        ...



class Absence_log():
    def __init__(self, db_path="database.db"):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def log_absence(self):
        ...

    def view_absence_history():
        ...





# child = Children()
# child.add_child(123,"sello","letswalo","2000-07-09","WTC","12","b",12344)
        



