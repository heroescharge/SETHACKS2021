from PIL import Image
from numpy import interp
import pandas as pd
#install library "openpxyl" as well

x_veg_pixel = 194
y_veg_pixel = 257

def get_vegetation(xpix, ypix):

    #Set up images
    vegetation_img = Image.open("vegetations.png")
    width, height = vegetation_img.size
    pixel_rgb = vegetation_img.convert("RGB")
    #Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((xpix, ypix))
    except:
        return "pixel does not exist"

    if ((r >= 250) and (g >= 250) and (b >= 250)):
        return ("pixel part of ocean")
    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("part of land")
    else:
        if ((r <= 5) and (g <= 5) and (b <= 5)): 
            return "High"
        elif ((r >= 174 and r <= 194) and (g >= 192 and g <= 212) and (b >= 175 and b <= 195)):
            return "None"
        elif ((r >= 241 and r <= 261) and (g >= 219 and g <= 239) and (b >= 188 and b <= 208)): 
            return "High"
        elif ((r >= 220 and r <= 240) and (g >= 211 and g <= 231) and (b >= 159 and b <= 179)): 
            return "High"
        elif ((r >= 202 and r <= 222) and (g >= 227 and g <= 247) and (b >= 239 and b <= 259)):
            return "None"
        elif ((r >= 118 and r <= 138) and (g >= 149 and g <= 169) and (b >= 84 and b <= 104)): 
            return "High"
        elif ((r >= 171 and r <= 191) and (g >= 195 and g <= 215) and (b >= 167 and b <= 187)):
            return "Medium"
        elif ((r >= 132 and r <= 152) and (g >= 175 and g <= 195) and (b >= 145 and b <= 165)):
            return "Medium"
        else:
            return "High"
        
        
print(get_vegetation(x_veg_pixel, y_veg_pixel))
