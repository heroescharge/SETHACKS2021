from PIL import Image

from numpy import interp

import pandas as pd
def get_temp(lat, longitude):

    temp_img = Image.open("tempreture_map.png")

    width, height = temp_img.size

    temp_rgb = temp_img.convert("RGB")

    #Get x and y positions of pixel representing city
    img_y = interp(lat, [24.382257, 50.532143], [1,height])

    img_x = interp(longitude, [-125.591848,-66.375709], [1,width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y

    r, g, b = temp_rgb.getpixel((img_x, img_y))

    print(r,g,b)

    if ((r >= 122 and r <= 128) and (g >= 21 and g <= 27) and (b >= 25 and b <= 31)):
        return "dark_red"

    elif ((r >= 227 and r <= 233) and (g >= 16 and g <= 22) and (b >= 22 and b <= 28)):
        return "red"

    elif ((r >= 242 and r <= 248) and (g >= 163 and g <= 167) and (b >= 22 and b <= 28)):
        return "orange"

    elif ((r >= 237 and r <= 243) and (g >= 232 and g <= 238) and (b >= 47 and b <= 53)):
        return "yellow"

    elif  ((r >= 67 and r <= 73) and (g >= 182 and g <= 188) and (b >= 137 and b <= 143)):
        return "blue"

    elif ((r >= 32 and r <= 38) and (g >= 80 and g <= 86) and (b >= 162 and b <= 168)):
        return "green"

    elif ((r >= 107 and r <= 113) and (g >= 62 and g <= 68) and (b >= 147 and b <= 153)):
        return "purple"

    elif ((r >= 222 and r <= 228) and (g >= 90 and g <= 97) and (b >= 155 and b <= 161)):
        return "pink" 

    elif ((r >= 250 and r <= 255) and (g >= 250 and g <= 255) and (b >= 250 and b <= 255)):
        return "water"
    
print(get_temp(35, -119))


