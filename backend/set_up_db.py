import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

# children table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Children(
    Child_Id integer Primary key autoincrement,
    first_name text not null,
    surname text not null,
    date_of_birth date,
    School text,
    Grade text,
    Class text,
    Parent_Id integer not null,
    foreign key(Parent_Id) references Parents(Parent_Id))
    """
)

# parents table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Parents(
    Parent_Id integer primary key autoincrement,
    first_name text not null,
    surname text not null,
    phone_number integer,
    email text
    )
    """
)

# Teachers table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Teachers(
    Teacher_Id integer primary key autoincrement,
    first_name text not null,
    surname text not null,
    email text
    )
    """
)

#bookings table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Bookings(
    Booking_Id integer primary key autoincrement,
    Child_Id integer not null,
    booking_type_id integer not null,
    booking_date date not null,
    status text default 'Scheduled',
    foreign key (child_Id) references Children(Child_Id),
    foreign key (booking_type_Id) references Booking_types(Booking_Id)
    )
    """

)

#booking types table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Booking_types(
    Booking_Id integer primary key autoincrement,
    Booking_type text unique not null
    )
    """
)

#absence logs
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Absence_logs(
    Absence_Id integer primary key autoincrement,
    Child_Id integer not null,
    absence_date Date not null,
    reason text,
    logged_by text,
    foreign key(Child_Id) references Children(Child_Id)
    )
    """
)

db.commit()
db.close()