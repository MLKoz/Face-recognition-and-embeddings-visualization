import os, shutil

class Fsystem:
    def check_or_create_the_system_file(self):
        if os.path.isdir('./photos') == True:
            print("Photos directory already exist")
        else:
            print("Creating photos directory")
            os.mkdir('./photos')


    def create_directory_for_person(self, id):
        if os.path.isdir('./photos/' + str(id)) == True:
            print("Error personal photos directory already exist, ID:", id)
        else:
            os.mkdir('./photos/' + str(id))


    def add_photo_for_person(self, id, image, photo_number):
        if os.path.isdir('./photos/' + str(id)) == True:
            image.save('./photos/' + str(id) + "/" + str(photo_number) + ".jpg")
        else:
            self.create_directory_for_person(id)
            self.add_photo_for_person(id, image, photo_number)


    """def add_photo_for_person(self, id, path_source_photo, photo_number):
        if os.path.isdir('./photos/' + str(id)) == True:
            shutil.copy2(path_source_photo, './photos/' + str(id) + "/" + str(photo_number) + ".jpg")
            print("ID przy dodawaniu =",id)
        else:
            # uruchamianie od nowa dialogu bazy (odswiezenie ilosci zdjec itp)
            #print("Error")
            self.create_directory_for_person(id)
            self.add_photo_for_person(id,path_source_photo,photo_number)"""


    """def change_numeration_photos_for_person(self, id):
        for i, filename in enumerate(os.listdir('./photos/' + str(id))):
            os.rename('./photos/' + str(id) + '/' + filename, './photos/' + str(id) + '/' + str(i) + ".jpg")"""


    def delete_photo(self, id_person, number_photo):
        try:
            os.remove('./photos/' + str(id_person) + '/' + str(number_photo) + '.jpg')
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))


    def delete_directory_and_photos(self, id):
        shutil.rmtree('./photos/'+str(id), ignore_errors=True)


    def return_list_files_for_person_id(self, id):
        return os.listdir('./photos/' + str(id))
