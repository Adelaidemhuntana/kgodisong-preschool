import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

# children table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Children(
    Child_id integer Primary key autoincrement,
    Child_id_number integer unique not null,
    First_name text not null,
    Surname text not null,
    Date_of_birth date,
    School text,
    Grade text,
    Class text,
    Parent_id integer not null,
    foreign key(Parent_id) references Parents(Parent_id))
    """
)

# parents table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Parents(
    Parent_id integer primary key autoincrement,
    Parent_id_number integer unique not null,
    First_name text not null,
    Surname text not null,
    Phone_number integer,
    Email text
    )
    """
)

# Teachers table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Teachers(
    Teacher_id integer primary key autoincrement,
    Teacher_id_number integer unique not null,
    First_name text not null,
    Surname text not null,
    Email text
    )
    """
)

#bookings table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Bookings(
    Booking_id integer primary key autoincrement,
    Child_id integer not null,
    Booking_type_id integer not null,
    Booking_date date not null,
    status text default 'Scheduled',
    foreign key (Child_id) references Children(Child_id),
    foreign key (Booking_type_id) references Booking_types(Booking_id)
    )
    """

)

#booking types table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Booking_types(
    Booking_id integer primary key autoincrement,
    Booking_type text unique not null
    )
    """
)

#absence logs
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Absence_logs(
    Absence_id integer primary key autoincrement,
    Child_id integer not null,
    Absence_date Date not null,
    Reason text,
    Logged_by text,
    foreign key(Child_id) references Children(Child_id)
    )
    """
)

db.commit()
db.close()