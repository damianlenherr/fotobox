from PIL import Image, ImageFont, ImageDraw
from PIL.ExifTags import TAGS
from pillow_lut import load_hald_image
import os
from pathlib import Path

logo_path = 'logo.png'

class ImageProcessor:
    def __init__(self, image_path):
        print("Edit started on path {}".format(image_path))
        self.image = Image.open(image_path)
        self.crop()

        # Insert text
        # get date from exif metadata
        exif_data = self.image.getexif()
        for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTime":
                    date = value
        self.insert_text(date, 20, 1030, 30, 10)
        
        # Insert logo
        logo = Image.open(logo_path)
        self.insert_logo(logo, 1920 - 120, 1080 - 120, .1)
        
        # Apply filter (color look up table)
        self.apply_lut('MY-LUT.png')

    def crop(self):
        width = self.image.size[0]
        height = self.image.size[1]
        ratio = float(width) / height
        if ratio <= 16.0 / 9:
            # if picture is less wide than 16/9
            new_width = 1920
            new_height = round(1920.0 / ratio)
            left = 0
            right = 1920
            top = new_height / 2 - 540
            bottom = top + 1080
        else:
            # if picture is wider than 16/9
            new_width = round(1080.0 * ratio)
            new_height = 1080
            left = new_width / 2 - 960
            right = left + 1920
            top = 0
            bottom = 1080
        self.image = self.image.resize((new_width, new_height))
        self.image = self.image.crop((left, top, right, bottom))
        return 0

    def insert_text(self, text, x, y, size, border):
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("AndaleMono.ttf", size)
        # take bounding box, add border and coordinates
        bbox = tuple(map(sum, zip(font.getbbox(text), (-border, -border, border, border), (x,y,x,y))))
        # make a transparent image for the text, initialized to transparent text color
        layer = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)
        # draw.text((x, y),"Sample Text",(r,g,b))
        border_bbox = (bbox[0] - border, bbox[1] - border, bbox[2] + border, bbox[3] + border)

        draw.rectangle(bbox, (0, 0, 0, 255))
        draw.text((x, y), text, (255, 255, 255, 255), font=font)
        del draw
        self.image = self.image.convert('RGBA')
        self.image = Image.alpha_composite(self.image, layer)
        return 0
    
    def insert_logo(self, logo, x, y, ratio):
        logo = logo.resize((round(logo.size[0] * ratio), round(logo.size[1] * ratio)))
        layer = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        layer.paste(logo, (x, y))
        self.image = Image.alpha_composite(self.image, layer)
        return 0
    
    def apply_lut(self, lut_path):
        lut = load_hald_image(lut_path)
        self.image = self.image.filter(lut)
        return 0
    
    def save_as_sequence(self, edited_path):
        i = 0
        while os.path.exists(os.path.join(edited_path, "crop-%s.png" % i)):
            i += 1
        filename = "crop-%s.png" % i
        filename = os.path.join(edited_path, filename)        
        Path(edited_path).mkdir(parents=True, exist_ok=True) #Make folder if it does not already exist
        self.image.save(filename)
        print(os.path.join(edited_path, "crop-%s.png" % i))
        return filename
