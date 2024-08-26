#!/usr/bin/env python3

from edit_image import ImageProcessor

def main():
    processed_image = ImageProcessor('capt0157.jpg')
    filename = processed_image.save_as_sequence('edited')

if __name__ == "__main__":
    main()
