import sys
import os.path


def get_path_user():
    path_user_arg = sys.argv
    csv_folder = os.getcwd() + '/csv'

    if len(path_user_arg) == 3:
        if os.path.isdir(path_user_arg[1]):
            csv_folder = path_user_arg[1] + '/csv'
            if not os.path.exists(csv_folder):
                os.makedirs(csv_folder)
        else:
            print('Please enter a valid path folder')
            exit()
    else:
        print('Please enter a path folder and a url')

    return csv_folder
