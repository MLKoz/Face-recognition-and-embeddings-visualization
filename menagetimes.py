from datetime import datetime


def save_time_tofile(namefile):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("gen_time/" + namefile, 'w') as file:
        file.write(now)


def read_time_from_file(namefile):
    with open(namefile, 'r') as file:
        x = file.read()
        return x
