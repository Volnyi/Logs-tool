import os
from PIL import Image, ImageDraw, ImageFont
import random

# Generate NPCs. Examples some near
# Aseprite api - https://www.aseprite.org/docs/cli/

"""Layers"""
layers_name = ['hair', 'clothes_up', 'clothes_down', 'clothes_shoes']
"""Aseprite default dir, can be changing"""
aseprite_path = 'D:\\Programs\\Steam\\steamapps\\common\\Aseprite\\aseprite.exe'
dir_default = ''
dir_export = ''


class Export:
    """Exporting aseprite files to png"""
    def __init__(self):
        self.aseprite_path = aseprite_path
        self.dir_default = dir_default
        self.dir_export = dir_export

    def export_layers(self, layers_name):
        """Exporting all items for man and women"""
        for folder in os.listdir(self.dir_default):
            nested_dir = self.dir_default + folder
            for aseprite_file in os.listdir(nested_dir):
                for one_layer_name in layers_name:
                    os.system(self.aseprite_path + ' -b ' + ' --layer ' + one_layer_name + ' ' + self.dir_default +
                              '\\' + aseprite_file + ' --filename-format ' + '\'{path}/{title}_{tag}.{extension}\'' +
                              '--scale 6 --sheet ' + self.dir_export + folder + '\\' + one_layer_name + '\\' +
                              aseprite_file + '.png')
                print(aseprite_file + '.png is Done')
            print('folder ' + folder + 'is Done')

    def export_one_layer(self, sex, one_layer_name):
        os.system(self.aseprite_path + ' -b ' + ' --layer ' + 'dark_shadow' + ' ' + self.dir_default + sex +
                  '.aseprite' + ' --filename-format ' + '\'{path}/{title}_{tag}.{extension}\''
                  + ' --scale 6 --sheet ' + self.dir_export + one_layer_name + '.png')
        print(one_layer_name + '.png is Done')

    def export_files(self):
        """Exporting all files in dir"""
        for file in os.listdir(self.dir_default):
            os.system(self.aseprite_path + ' -b ' + self.dir_default + file + ' --filename-format ' +
                      '\'{path}/{title}_{tag}.{extension}\' --scale 6 --sheet ' + self.dir_export + file + '.png')
            print(file + 'is Done')


def add_image(input_image, main_image, save_name):
    """Overlaying one picture on top of another"""
    input = Image.open(input_image, 'r')
    main = Image.open(main_image, 'r')
    input.paste(main.convert('RGB'), (0, 0), main)
    input.save(save_name)
    print('Generate is Done')


def add_in_folder(dir_first_file, dir_second_file, dir_fin):
    """Overlaying all images from one folder on top of all pictures from another folder"""
    for item_one in os.listdir(dir_first_file):
        for item_two in os.listdir(dir_second_file):
            print(item_one + ' add ' + item_two)
            final_file = dir_fin + item_one + item_two + '.png'
            add_image(dir_first_file + item_one, dir_second_file + item_two, final_file)
            print('Generate is Done')


def generate_NPC(value, dir_fin, dir_for_NPCs):
    """Generating NPCs with all needed layers"""
    i = value
    while i >= 0:
        body = random.choice(os.listdir(dir_fin + 'skin\\'))
        clothes = random.choice(os.listdir(dir_fin + 'clothes\\'))
        print(body + ' add ' + clothes)
        shadow_light = dir_fin + 'light_shadow.png'
        shadow_dark = dir_fin + 'dark_shadow.png'
        final_file = dir_for_NPCs + clothes + '.png'
        add_image(dir_fin + 'skin\\' + body, dir_fin + 'clothes\\' + clothes, final_file)
        add_image(final_file, shadow_dark, final_file)
        add_image(final_file, shadow_light, final_file)
        i -= 1
        print('NPC is Done')
