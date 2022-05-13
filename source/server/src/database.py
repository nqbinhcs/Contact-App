import sqlite3
from sqlite3 import Error
from utils import *



class ContactsDataBase():
    def __init__(self, name_data_base='source/server/contacts.db'):
        try:
            self.conn = sqlite3.connect(name_data_base)
            print(sqlite3.version)
        except Error as err:
            print(err)


    def create_table(self):
        try:
            self.conn.execute('''CREATE TABLE CONTACTS
                            (ID             INT            PRIMARY KEY     NOT NULL,
                            NAME           VARCHAR(50)                    NOT NULL,
                            PHONE          CHAR(10),
                            EMAIL          VARCHAR(50),
                            SMALLAVATAR    BLOB,
                            MAINAVATAR     BLOB
                            );''')
        except:
            pass

    def add_contact(self, id, name, phone, email, small_avt, main_avt):

        self.conn.execute("INSERT INTO CONTACTS (ID,NAME,PHONE,EMAIL,SMALLAVATAR,MAINAVATAR) \
                      VALUES (?, ?, ?, ?, ?, ?)", (id, name, phone, email, convert_to_binary_data(small_avt), convert_to_binary_data(main_avt)))

    
    def get_contact(self, contact_name):
        li = list(list(self.conn.execute("SELECT * FROM CONTACTS WHERE NAME = ?", [contact_name]))[0])
        li[-1] = convert_to_data(li[-1])
        li[-2] = convert_to_data(li[-2])
        return li

    def get_all_contacts(self):

        cursor = self.conn.execute(
            "SELECT * from CONTACTS")

        results = [(id, name, phone, email, convert_to_data(small_avt), convert_to_data(main_avt))
                   for (id, name, phone, email, small_avt, main_avt) in cursor]

        return results

    def print_table(self):

        table = pd.read_sql_query(
            "SELECT * from CONTACTS", self.conn)

        table['SMALLAVATAR'] = table['SMALLAVATAR'].map(lambda x: 'IMG')
        table['MAINAVATAR'] = table['MAINAVATAR'].map(lambda x: 'IMG')

        print(table)


def main():

    # Demo 

    # Create database
    db = ContactsDataBase()

    # Create table
    db.create_table()

    # Add Contacts
    db.add_contact(1, 'Nguyen Quang Binh', '077xxxxxxx',
                '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt.png')

    db.add_contact(2, 'Nguyen Trong Hieu', '078xxxxxxx',
                '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt.png')

    db.add_contact(3, 'Nguyen Bao Tin', '079xxxxxxx',
                '2012xxxx@student.hcmus.edu.vn', 'source/server/assets/images/avt.png', 'source/server/assets/images/avt.png')

    # Print table
    db.print_table()

    # Get list of all contacts
    list_contacts = db.get_all_contacts()

    # Get a contact by name
    contact = db.get_contact('Nguyen Quang Binh')

    print(contact)

    # Show main avatar <(")
    contact[-1].show()


if __name__ == "__main__":
    main()





