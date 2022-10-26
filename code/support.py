import pygame
from os import walk


def import_folder(path):
    """
    import files & create surfaces from them
    return list of all surfaces
    """
    surface_list = []

    # walk through folders & subfolders to get list of filenames
    for folder_name, sub_folder, image_files in walk(path):
        for image in sorted(image_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


