import sqlite3
from sqlite3 import Error
from utils import *


class ContactsDataBase():
    def __init__(self, name_data_base='source/server/database/contacts.db'):
        try:
            self.conn = sqlite3.connect(
                name_data_base, check_same_thread=False)
            print(sqlite3.version)
        except Error as err:
            print(err)

    def create_table(self):
        try:
            self.conn.execute('''CREATE TABLE CONTACTS
                            (ID            INT            PRIMARY KEY     NOT NULL,
                            NAME           VARCHAR(50)                    NOT NULL,
                            PHONE          CHAR(10),
                            EMAIL          VARCHAR(50),
                            THUMBNAIL      VARCHAR(100),
                            AVATAR         VARCHAR(100)
                            );''')
        except:
            pass

    def add_contact(self, id, name, phone, email, thumbnail, avatar):

        self.conn.execute("INSERT INTO CONTACTS (ID,NAME,PHONE,EMAIL,THUMBNAIL,AVATAR) \
                      VALUES (?, ?, ?, ?, ?, ?)", (id, name, phone, email, thumbnail, avatar))

        self.conn.commit()

    # def get_contact(self, contact_name):
    #     li = list(list(self.conn.execute("SELECT * FROM CONTACTS WHERE NAME = ?", [contact_name]))[0])
    #     li[-1] = convert_to_data(li[-1])
    #     li[-2] = convert_to_data(li[-2])
    #     return li

    # def get_all_contacts(self):

    #     cursor = self.conn.execute(
    #         "SELECT * from CONTACTS")

    #     results = [(id, name, phone, email, convert_to_data(small_avt), convert_to_data(main_avt))
    #                for (id, name, phone, email, small_avt, main_avt) in cursor]

    #     return results

    def get_all_contacts(self):
        '''
        pop_up -> Two options:
        [1]: all information (id, name)
        [2]: all information (id, name, thumbnail)
        '''
        cursor = self.conn.execute(
            "SELECT ID,NAME from CONTACTS")

        results = [(id, name)
                   for (id, name) in cursor]
        return results

    def get_all_contacts_thumbnail(self):

        cursor = self.conn.execute(
            "SELECT ID, THUMBNAIL from CONTACTS")

        results = [thumbnail
                   for (id, thumbnail) in cursor]
        return results

    def get_contact(self, contact_id):
        '''
        pop_up -> Two options:
        [1]: all information (id, name, phone, email)
        [2]: all information (id, name, phone, email, avatar)
        '''
        result = list(list(self.conn.execute(
            "SELECT ID,NAME,PHONE,EMAIL FROM CONTACTS WHERE ID = ?", [contact_id]))[0])

        return result

    def get_contact_avatar(self, contact_id):
        '''
        pop_up -> Two options:
        [1]: all information (id, name, phone, email)
        [2]: all information (id, name, phone, email, avatar)
        '''
        result = list(list(self.conn.execute(
            "SELECT AVATAR FROM CONTACTS WHERE ID = ?", [contact_id]))[0])

        return result[0]

    def print_table(self):

        table = pd.read_sql_query(
            "SELECT * from CONTACTS", self.conn)

        # table['SMALLAVATAR'] = table['SMALLAVATAR'].map(lambda x: 'IMG')
        # table['MAINAVATAR'] = table['MAINAVATAR'].map(lambda x: 'IMG')

        print(table)


def main():

    # Demo

    # Create database
    db = ContactsDataBase()

    # Create table
    db.create_table()

    # Add Contacts
    # db.add_contact(1, 'Nguyen Quang Binh', '077xxxxxxx',
    #                '2012xxxx@student.hcmus.edu.vn', 'source/server/database/thumbnails/Image_1.png', 'source/server/database/avatars/Image_1.png')

    # db.add_contact(2, 'Nguyen Trong Hieu', '078xxxxxxx',
    #                '2012xxxx@student.hcmus.edu.vn', 'source/server/database/thumbnails/Image_2.png', 'source/server/database/avatars/Image_2.png')

    # db.add_contact(3, 'Nguyen Bao Tin', '079xxxxxxx',
    #                '2012xxxx@student.hcmus.edu.vn', 'source/server/database/thumbnails/Image_3.png', 'source/server/database/avatars/Image_3.png')

    # Print table
    db.print_table()

    # Get list of all contacts
    print(db.get_all_contacts())

    # Get a contact by name
    print(db.get_contact(1))

    # Get list of all contacts
    print(db.get_all_contacts_thumbnail())

    # Get a contact by name
    print(db.get_contact_avatar(1))

    # Show main avatar <(")
    # contact[-1].show()


if __name__ == "__main__":
    main()
