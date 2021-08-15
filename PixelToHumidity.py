from PIL import Image
from numpy import interp
import pandas as pd
#install library "openpxyl" as well

x_humidity_pixel = 97
y_humidity_pixel = 45

def get_humidity(xpix, ypix):

    #Set up images
    humidity_img = Image.open("humidities.png")
    width, height = humidity_img.size
    pixel_rgb = humidity_img.convert("RGB")
    #Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((xpix, ypix))
    except:
        return "pixel does not exist"

    if ((r >= 200 and r <= 210) and (g >= 223 and g <= 233) and (b >= 242 and b <= 252)):
            return ("pixel part of ocean")
    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("part of land")
    else:        
        if ((r >= 190 and r <= 200) and (g >= 65 and g <= 75) and (b >= 46 and b <= 56)): 
            return 10
        elif ((r >= 233 and r <= 243) and (g >= 155 and g <= 165) and (b >= 59 and b <= 69)):
            return 25
        elif ((r >= 248 and r <= 258) and (g >= 236 and g <= 246) and (b >= 76 and b <= 86)): 
            return 35
        elif ((r >= 169 and r <= 179) and (g >= 200 and g <= 210) and (b >= 113 and b <= 123)): 
            return 45
        elif ((r >= 129 and r <= 139) and (g >= 184 and g <= 194) and (b >= 85 and b <= 95)):
            return 55
        elif ((r >= 98 and r <= 108) and (g >= 167 and g <= 177) and (b >= 78 and b <= 88)): 
            return 65
        elif ((r >= 56 and r <= 66) and (g >= 132 and g <= 142) and (b >= 71 and b <= 81)):
            return 75
        elif ((r >= 48 and r <= 58) and (g >= 127 and g <= 137) and (b >= 172 and b <= 182)):
            return 90
        else
            return 10

        
print(get_humidity(x_humidity_pixel, y_humidity_pixel))
