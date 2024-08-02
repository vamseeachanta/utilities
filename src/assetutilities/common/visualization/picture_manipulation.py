import logging
import os
from PIL import Image
import rembg


class PictureManipulation():

    def __init__(self, cfg=None):
        pass
    
    def remove_background(self, image):

    # Input and output paths
    input_path = "/Users/saiachanta/Desktop/pih_step08_elevation.jpg"
    output_path = "result5.png"

    # Check if input file exists
    if os.path.exists(input_path):
        # Check if the file is readable
        if os.access(input_path, os.R_OK):
            # Open the input image
            input_image = Image.open(input_path)

            # Process the image
            output_image = rembg.remove(input_image)

            # Save the output image
            output_image.save(output_path)
            print("Background removed successfully!")
        else:
            print("Input file is not readable.")
    else:
        print("Input file does not exist.")
        
    def resize_image(self, image, size):
        pass
    
    def crop_image(self, image, size):
        pass
    
    def overlap_images(self, cfg):
        from PIL import Image

        # Load PNG images
        image1 = Image.open("/Users/saiachanta/kk/result1.png")
        image2 = Image.open("/Users/saiachanta/kk/result2.png")
        image3 = Image.open("/Users/saiachanta/kk/result3.png")
        image4 = Image.open("/Users/saiachanta/kk/result5.png")

        # Create a blank canvas of the same size as input images
        canvas = Image.new("RGBA", image1.size, (255, 255, 255, 0))  # Create a transparent canvas

        # Overlay images onto the canvas
        canvas.paste(image1, (0, 0), mask=image1)
        canvas.paste(image2, (0, 0), mask=image2)
        canvas.paste(image3, (0, 0), mask=image3)
        canvas.paste(image4, (0, 0), mask=image4)

        # Save or display the resulting image
        canvas.save("/Users/saiachanta/kk/lastresult.png")
        canvas.show()
