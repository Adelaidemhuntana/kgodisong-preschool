from crud import *

child_1 = [(546, "chaba", "lala", "2022-03-18", "wtc", 4, "C", 1)]
child_list = [
    (123, "Sello", "Letswalo", "2003-07-09", "wtc", 12, "B", 1),
    (132, "sanele", "Mokoena", "2010-05-12", "wtc", 5, "A", 2),
    (334, "Lerato", "Nkosi", "2012-03-18", "wtc", 3, "C", 1)]

parents_list = [
    (111, "Mom1", "Sur1", "0821234567", "mom1@example.com"),
    (222, "Dad2", "Sur2", "0839876543", "dad2@example.com"),
    (435, "Mom3", "Sur3", "0845556677", "mom3@example.com")
]

teachers_list = [
    (545, "Bob", "Chaba", "bob.chaba@example.com"),
    (657, "Alice", "Mokoena", "alice.mokoena@example.com"),
    (868, "John", "Nkosi", "john.nkosi@example.com")
]
Booking_types_list = [("Dental",),("Eye Test",)]
#adding parents
# adding teachers
# adding children
parent = Parent()
teacher = Teacher()
child = Children()
absence = Absence_log()
book = Bookings()
types = Booking_types()

#adding
# teacher.add_teacher(teachers)
# parent.add_parent(parents)
#child.add_child(child_1)

#removing
# teacher.remove_teacher(123)
# child.remove_child(123)
# parent.remove_parent(123)



#logging absence
#absence.log_absence(124,"2020","sick",111)
#absence.view_absence_history(124)

# book.create_booking(123,1,"2020-07-09")
# book.cancel_booking(123,"2020-07-09")


# types.add_booking_types(Booking_types_list)

