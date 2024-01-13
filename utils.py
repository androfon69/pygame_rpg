import pygame
from csv import reader
from os import walk

def import_csv_layout(csv_path):
    terrain = []
    
    with open(csv_path) as map:
        layout = reader(map, delimiter = ',')
        for row in layout:
            terrain.append(list(row))
        return terrain
    
def import_surface_folder(images_path):
    surface_list = []
    
    for _,__,files in walk('images_path'):
        for image in files:
            full_path = images_path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list