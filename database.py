import sqlite3

class Database:
    def __init__(self):
        self.create_persons_table()


    def create_persons_table(self):
        con = sqlite3.connect("db.db")
        con.execute("CREATE TABLE IF NOT EXISTS persons(\
                    id INTEGER PRIMARY KEY,\
                    Firstname text,\
                    Lastname text,\
                    Gender int,\
                    DoB text,\
                    Nationality int,\
                    Race int,\
                    Count_photos int)")
        con.commit()
        con.close()


    def add_person_record(self, Firstname, Lastname, Gender, DoB, Nationality, Race):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("INSERT INTO persons VALUES (NULL, ?, ?, ?, ?, ?,?, 1)",
                        (Firstname, Lastname, Gender, DoB, Nationality, Race))
            x=cur.lastrowid
            con.commit()
            con.close()
            return x
        except:
            print("Error during add record to db")
            if con is not None:
                con.close()
            return -1


    def view_date(self):
        con = sqlite3.connect("db.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM persons")
        rows = cur.fetchall()
        con.close()
        return rows


    def view_date_order_by_firstname_and_lastname(self):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM persons order by Firstname, Lastname")
            rows = cur.fetchall()
            con.close()
            return rows
        except:
            print("Error during view_date_order_by_firstname_and_lastname")
            if con is not None:
                con.close()
            return -1


    def delete_record(self,id):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("DELETE FROM persons WHERE id=?",(id,))
            con.commit()
            con.close()
        except:
            print("Error during delete record")
            if con is not None:
                con.close()


    def get_number_of_people_in_database(self):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT count(*) from persons")
            liczba = cur.fetchone()
            con.close()
            #print(liczba[0])
            return liczba[0]
        except:
            print("blad podczas fast test")
            return 0
        finally:
            con.close()


    def get_amount_one_race_people(self, race):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT count(*) from persons where Race = ?",(race,))
            liczba = cur.fetchone()
            con.close()
            return liczba[0]
        except:
            print("blad podczas get_amount_one_race_people")
            if con is not None:
                con.close()
            return 0


    def get_amount_one_gender_people(self, gender):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT count(*) from persons where Gender = ?",(gender,))
            liczba = cur.fetchone()
            con.close()
            #print(liczba[0])
            return liczba[0]
        except:
            print("blad podczas get_amount_one_gender_people")
            return 0
        finally:
            con.close()


    def get_data_about_person(self,id):
        rows = -1
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT Firstname, Lastname, id, Gender, "
                        "Race from persons WHERE id=?",(id,))
            rows = cur.fetchall()
            con.close()
            return rows
        except:
            print("Error during get_data_about_person")
            if con is not None:
                con.close()
            return []



    def get_all_data_about_person(self, id):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT * from persons WHERE id=?",(id,))
            rows = cur.fetchone()
            con.close()
            return rows
        except:
            print("blad podczas get_all_data_about_person")
        finally:
            con.close()

    def get_photos_amount_for_person(self, id):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            print("jestem0")
            cur.execute("SELECT Count_photos FROM persons WHERE id=?",(id,))
            print("JEstem",id)
            liczba = cur.fetchone()
            con.close()
            #print(liczba[0])
            return liczba[0]
        except Exception as err:
            print("blad podczas photos amount for person")
            print(str(err))
        finally:
            con.close()


    def update_photos_amount(self, id, number):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("UPDATE persons SET Count_photos = ? WHERE id = ?",(number,id,))
            con.commit()
            con.close()
        except Exception as err:
            print("Błąd update photos amount")
            print(str(err))
            if con is not None:
                con.close()


    def update_personal_data(self, id, firstname, lastname, gender, born_date, born_place, race):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("UPDATE persons SET Firstname = ?, Lastname = ?, Gender = ?, DoB = ?, Nationality = ?,\
             Race = ? WHERE id = ?",(firstname,lastname,gender, born_date, born_place, race, id,))
            con.commit()
            con.close()
        except Exception as err:
            print("Error during update_personal_data")
            print(str(err))
            if con is not None:
                con.close()


    def get_last_insert_row_id(self):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT LAST_INSERT_ROWID()")
            liczba = cur.fetchone()
            con.close()
            #print(liczba[0])
            return liczba[0]
        except:
            print("blad podczas fast test")
        finally:
            con.close()


    def search_person_via_data(self, firstname="", lastname="",
                               nationality="", dob="", race=""):
        try:
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            cur.execute("SELECT * from persons WHERE Firstname=? or"
                        " Lastname=? or Nationality=? or DoB=? or Race=?",
                        (firstname,lastname,nationality,dob,race))
            rows = cur.fetchall()
            con.close()
            return rows
        except:
            print("Error during search_person_via_data")
            if con is not None:
                con.close()
            return []


#db = Database()