import PIL
from PIL import Image, ImageOps
from tkinter import filedialog

import PIL.ImageEnhance
import PIL.ImageOps

#constants 
DEFAULT_BRIGHTNESS = 1.0
DEFAULT_CONTRAST = 1.0

# You can add as many characters as you want in the list (1-255)
# the first character in this case " " (blank space) -> is the brightest
# and the last character "@" -> is the darkest
default_character_list = [" ", ".", "*", "%", "#", "@"]
circulater_character_list = [" ", ".", "°", "*", "o", "0", "#", "@"]


# define characters() -> takes in the "character list" and assigns "Min" and "Max" Pixel brightness value to each character
def define_characters(char_list):
    # divisions is the gap between each characters brightness val (max_val - min_val )
    divisions = 255 / len(char_list)  
    defined_dict = {}
    min_val = 0
    max_val = divisions

    for character in char_list:
        defined_dict.update({character: {"min_val": min_val, "max_val": max_val}})
        min_val = max_val + 1
        max_val += divisions

    return defined_dict


# ask_filepath -> gets the "file path" of the image if it exists
def ask_filepath():
    while True:
        filepath = filedialog.askopenfilename(
            filetypes=(("PNG/JPG", ("*.png", "*.jpg")), ("ALL", "*")),
            defaultextension=".jpg",
            title="Select An Image File",
        )

        if filepath:
            return filepath
        else:
            print("Please Select An Image")
            user_input = input("Press Any Button To continue... or 'q' to QUIT : ")
            if user_input.strip().lower() == "q":
                quit()


# get_image() -> takes in a "file path/other variables" and returns an "image" after resizing
def get_image(filepath, inverted=False, brightness=DEFAULT_BRIGHTNESS, contrast=DEFAULT_CONTRAST):
    with Image.open(filepath) as image:
        width, height = image.size
        image = image.resize((width // 10, height // 18))
        image = PIL.ImageEnhance.Brightness(image).enhance(brightness)
        image = PIL.ImageEnhance.Contrast(image).enhance(contrast)
        image = image if inverted == False else PIL.ImageOps.invert(image=image)
        image = PIL.ImageOps.grayscale(image=image)
        width, height = image.size
        return image


# print_image()  -> takes in an "image" and a "defined character dictionary"
def print_image(image, defined_characters):
    width, height = image.size
    for y in range(height):
        row_string = ""
        for x in range(width):
            brightness = image.getpixel((x, y))
            for key, value in defined_characters.items():

                if (
                    brightness >= defined_characters[key]["min_val"]
                    and brightness <= defined_characters[key]["max_val"]
                ):

                    row_string += key

        print(row_string)


print("Welcome To Image To ASCII Convertor !")

while True:
    brightness =input("Enter a Brightness Value(0.0 - 5.0) or Enter to continue. : ")
    contrast = input("Enter an Contrast Value(0.0 - 5.0) or Enter to continue. : ")

    if brightness.strip() =="" and contrast.strip() == "":
            print("Using Default Values.")
            brightness = DEFAULT_BRIGHTNESS
            contrast = DEFAULT_CONTRAST
            break

    try:
        brightness = float(brightness)
        contrast = float(contrast)
        break
    except ValueError:
            print("Please Enter a Digit or press Enter.. :")

print("")
print("Do You want the image to be inverted ?")
invert = input("Pess 'y' for YES or any other button to continue.. :")
is_inverted = True if invert.strip().lower() == "y" else False


# define a dictionary of character each with their own "min" and "max" val
defined_characters = define_characters(circulater_character_list)

filepath = ask_filepath()
image = get_image(filepath, is_inverted ,  brightness=brightness, contrast=contrast)

print_image(image, defined_characters)
