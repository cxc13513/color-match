import os
import requests
import pdb


def get_files_in_folder(path):
    '''Find all files in path input and save down file names as a list.

    INPUT: path to folder (string)
    OUTPUT: list of file names
    '''
    files_list = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files_list.append(str(path+file))
    return files_list


def save_down_pics_from_links(urls_list, path):
    '''Pull, rename and save down jpeg of picture from url list into folder.

    INPUT: list of urls (string)
           filepath to folder to save down to
           maximum number of jpegs already exist in folder
           (so don't write over existing pictures)

    OUTPUT: string to let you know when it's all saved down into folder
    '''
    # find number of jpegs already in folder, and start numbering after that
    # so don't overwrite existing jpegs!!
    max_num_already_exist = len(get_files_in_folder(path))
    for index, url in enumerate(urls_list):
        name = str(index+max_num_already_exist)
        ext = ".jpg"
        full = path+name+ext
        img_data = requests.get(url).content
        with open(full, 'wb') as handler:
            handler.write(img_data)
    print("All saved down in path")
