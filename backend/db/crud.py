import sqlite3

class Children:
    def __init__(self, db_path="database.db"):
         self.db = sqlite3.connect(db_path)
         self.cursor = self.db.cursor()

    def add_child(self,child_id_number,name,surname,dob,school,grade,class_,parent_id_number):
        self.cursor.execute("""
                            INSERT INTO Children(
                            Child_id_number,
                            First_name,
                            Surname,
                            Date_of_birth,
                            School,
                            Grade,
                            Class,
                            Parent_id
                            )
                            values(?,?,?,?,?,?,?,?)
                            """,(child_id_number,name,surname,dob,school,grade,class_,parent_id_number)
                            )
        self.db.commit()
        print(f"{name} {surname} added")
        
    def remove_child(self,child_id_number):
        self.cursor.execute("DELETE FROM Children WHERE Child_id_number = ?",(child_id_number))
        self.db.commit()
        print("child removed")

    def update_child_info(self):










# child = Children()
# child.add_child(123,"sello","letswalo","2000-07-09","WTC","12","b",12344)
        



