from PIL import Image

from numpy import interp

import pandas as pd

import time

# install library "openpyxl" as well

df = pd.read_excel("uscities.xlsx")

state = input("Enter your state:")

city = input("Enter your city:")

temp_img = Image.open("tempreture_map.png")


temp_img.resize((800, 488), Image.ANTIALIAS)

temp_width, temp_height = temp_img.size

temp_rgb = temp_img.convert("RGB")

humidity_img = Image.open("humidities.png")


humidity_img.resize((800, 488), Image.ANTIALIAS)

hum_width, hum_height = humidity_img.size

hum_rgb = humidity_img.convert("RGB")
vegetation_img = Image.open("vegetations.png")

vegetation_img.resize((800, 488), Image.ANTIALIAS)

veg_width, veg_height = vegetation_img.size

veg_rgb = vegetation_img.convert("RGB")


def getLatlongitude(city, state):

    cityRowArr = df[df['city'] == city].index.values

    cityRowNumber = -1  # -1 means no row number exists

    # Check if state is correct as well
    for i in range(0, len(cityRowArr)):

        if df.loc[cityRowArr[i]][1] == state:  # index 0 = city, 1 = state, 2 = lat, 3 = long

            # note that the row index is two less than the row number in excel
            cityRowNumber = cityRowArr[i]

    # make sure that city exists
    if cityRowNumber != -1:

        cityDataArr = df.loc[cityRowNumber]

        lat = cityDataArr[2]

        longitude = cityDataArr[3]
        coords = [lat, longitude]

        return coords

    else:
        print("city not found")


def get_temp(lat, longitude):

    temp_img = Image.open("tempreture_map.png")
    temp_img.resize((800, 488), Image.ANTIALIAS)

    width, height = temp_img.size

    temp_rgb = temp_img.convert("RGB")

    # Get x and y positions of pixel representing city
    img_y = interp(lat, [24.382257, 50.532143], [1, height])

    img_x = interp(longitude, [-125.591848, -66.375709], [1, width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y

    r, g, b = temp_rgb.getpixel((img_x, img_y))

    if ((r >= 122 and r <= 128) and (g >= 21 and g <= 27) and (b >= 25 and b <= 31)):
        return "dark_red"

    elif ((r >= 227 and r <= 233) and (g >= 16 and g <= 22) and (b >= 22 and b <= 28)):
        return "red"

    elif ((r >= 242 and r <= 248) and (g >= 163 and g <= 167) and (b >= 22 and b <= 28)):
        return "orange"

    elif ((r >= 237 and r <= 243) and (g >= 232 and g <= 238) and (b >= 47 and b <= 53)):
        return "yellow"

    elif ((r >= 67 and r <= 73) and (g >= 182 and g <= 188) and (b >= 137 and b <= 143)):
        return "blue"

    elif ((r >= 32 and r <= 38) and (g >= 80 and g <= 86) and (b >= 162 and b <= 168)):
        return "green"

    elif ((r >= 107 and r <= 113) and (g >= 62 and g <= 68) and (b >= 147 and b <= 153)):
        return "purple"

    elif ((r >= 222 and r <= 228) and (g >= 90 and g <= 97) and (b >= 155 and b <= 161)):
        return "pink"

    elif ((r >= 250 and r <= 255) and (g >= 250 and g <= 255) and (b >= 250 and b <= 255)):
        return "water"

    else:
        return "red"


def get_humidity(lat, longitude):

    # Set up images
    humidity_img = Image.open("humidities.png")
    humidity_img.resize((800, 488), Image.ANTIALIAS)

    width, height = humidity_img.size

    pixel_rgb = humidity_img.convert("RGB")

    img_y = interp(lat, [24.382257, 50.532143], [1, height])

    img_x = interp(longitude, [-125.591848, -66.375709], [1, width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y
    # Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((img_x, img_y))

    except:
        return "pixel does not exist"

    if ((r >= 200 and r <= 210) and (g >= 223 and g <= 233) and (b >= 242 and b <= 252)):
        return ("water")

    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("water")

    else:

        if ((r >= 190 and r <= 200) and (g >= 65 and g <= 75) and (b >= 46 and b <= 56)):
            return "red"

        elif ((r >= 233 and r <= 243) and (g >= 155 and g <= 165) and (b >= 59 and b <= 69)):
            return "orange"

        elif ((r >= 248 and r <= 258) and (g >= 236 and g <= 246) and (b >= 76 and b <= 86)):
            return "yellow"

        elif ((r >= 169 and r <= 179) and (g >= 200 and g <= 210) and (b >= 113 and b <= 123)):
            return "light_green"

        elif ((r >= 129 and r <= 139) and (g >= 184 and g <= 194) and (b >= 85 and b <= 95)):
            return "yellow_green"

        elif ((r >= 98 and r <= 108) and (g >= 167 and g <= 177) and (b >= 78 and b <= 88)):
            return "green"

        elif ((r >= 56 and r <= 66) and (g >= 132 and g <= 142) and (b >= 71 and b <= 81)):
            return "dark_green"

        elif ((r >= 48 and r <= 58) and (g >= 127 and g <= 137) and (b >= 172 and b <= 182)):
            return "blue"

        else:
            return "red"


def get_temp_pixels(pixel_x, pixel_y, temp_rgb):
    try:
        r, g, b = temp_rgb.getpixel((pixel_x, pixel_y))
    
    except:
        return "water"

    if ((r >= 90 and r <= 115) and (g >= 20 and g <= 35) and (b >= 20 and b <= 40)):
        return "dark_red"

    elif ((r >= 170 and r <= 220) and (g >= 45 and g <= 100) and (b >= 35 and b <= 95)):
        return "red"

    elif ((r >= 190 and r <= 235) and (g >= 140 and g <= 165) and (b >= 50 and b <= 70)):
        return "orange"

    elif ((r >= 230 and r <= 245) and (g >= 210 and g <= 235) and (b >= 80 and b <= 95)):
        return "yellow"

    elif  ((r >= 25 and r <= 45) and (g >= 65 and g <= 85) and (b >= 145 and b <= 165)):
        return "blue"

    elif ((r >= 85 and r <= 105) and (g >= 160 and g <= 180) and (b >= 125 and b <= 145)):
        return "green"

    elif ((r >= 90 and r <= 110) and (g >= 55 and g <= 75) and (b >= 135 and b <= 150)):
        return "purple"

    elif ((r >= 180 and r <= 220) and (g >= 80 and g <= 105) and (b >= 130 and b <= 160)):
        return "pink" 

    elif ((r >= 250 and r <= 255) and (g >= 250 and g <= 255) and (b >= 250 and b <= 255)):
        return "water"
    else:
        return "yellow"


def get_humidity_pixels(pixel_x, pixel_y, pixel_rgb):

    # Set up images

    try:
        r, g, b = pixel_rgb.getpixel((pixel_x, pixel_y))

    except:
        return "water"

    if ((r >= 200 and r <= 210) and (g >= 223 and g <= 233) and (b >= 242 and b <= 252)):
        return ("water")

    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("water")

    else:

        if ((r >= 190 and r <= 200) and (g >= 65 and g <= 75) and (b >= 46 and b <= 56)):
            return "red"

        elif ((r >= 233 and r <= 243) and (g >= 155 and g <= 165) and (b >= 59 and b <= 69)):
            return "orange"

        elif ((r >= 248 and r <= 258) and (g >= 236 and g <= 246) and (b >= 76 and b <= 86)):
            return "yellow"

        elif ((r >= 169 and r <= 179) and (g >= 200 and g <= 210) and (b >= 113 and b <= 123)):
            return "light_green"

        elif ((r >= 129 and r <= 139) and (g >= 184 and g <= 194) and (b >= 85 and b <= 95)):
            return "yellow_green"

        elif ((r >= 98 and r <= 108) and (g >= 167 and g <= 177) and (b >= 78 and b <= 88)):
            return "green"

        elif ((r >= 56 and r <= 66) and (g >= 132 and g <= 142) and (b >= 71 and b <= 81)):
            return "dark_green"

        elif ((r >= 48 and r <= 58) and (g >= 127 and g <= 137) and (b >= 172 and b <= 182)):
            return "blue"

        else:
            return "yellow"


def get_vegetation(lat, longitude):

    # Set up images
    vegetation_img = Image.open("vegetations.png")
    vegetation_img.resize((800, 488), Image.ANTIALIAS)

    width, height = vegetation_img.size

    pixel_rgb = vegetation_img.convert("RGB")

    img_y = interp(lat, [24.382257, 50.532143], [1, height])

    img_x = interp(longitude, [-125.591848, -66.375709], [1, width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y
    # Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((img_x, img_y))

    except:

        return "water"

    if ((r >= 250) and (g >= 250) and (b >= 250)):
        return ("water")

    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("water")

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


def get_vegetation_pixels(pixel_x, pixel_y, pixel_rgb):

    # Set up images

    try:
        r, g, b = pixel_rgb.getpixel((pixel_x, pixel_y))

    except:

        return "water"

    if ((r >= 250) and (g >= 250) and (b >= 250)):
        return ("water")

    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("water")

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

# START OF SIMULATION


def futureSimulation(city, state):

    future_years = int(input(
        "Enter number of years into the future you wish to see the impact of climate change:"))

    blankmap = Image.open("blankmap.png")
    blankmap = blankmap.resize((800, 488), Image.ANTIALIAS)

    blankmappixels = blankmap.load()

    temp_color_to_fire_risk_index = {"dark_red": 6.25, "red": 5.5, "orange": 4.75,
                                     "yellow": 4, "blue": 3.25, "green": 2.5, "purple": 1.75, "pink": 1, "water": 0}

    color_to_temp = {"dark_red": 72.5, "red": 67.5, "orange": 62.5, "yellow": 57.5,
                     "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5, "water": 0}

    humidity_to_fire_risk_index = {"blue": 1, "dark_green": 1.75, "green": 2.5,
                                   "yellow_green": 3.25, "light_green": 4, "yellow": 4.75, "orange": 5.5, "red": 6.25, "water": 0}

    temp_to_color = {value: key for (key, value) in color_to_temp.items()}

    width, height = blankmap.size

    print(width, height)

    coords = getLatlongitude(city, state)

    pixel_rgb = blankmap.convert("RGB")

    img_y = interp(coords[0], [25.712922, 49.044568], [1, height])

    img_x = interp(coords[1], [-124.523822, -66.621243], [1, width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height-img_y

    size = 1000

    # increasing temperature as years continue

    for x in range(int(img_x) - size, int(img_x) + size):

        for y in range(int(img_y) - size, int(img_y) + size):

            # print(x,y)

            try:
                pixel_temp_color = get_temp_pixels(x, y, temp_rgb)

                pixel_humidity_color = get_humidity_pixels(x, y, hum_rgb)

                current_fire_risk_index = temp_color_to_fire_risk_index[pixel_temp_color] + humidity_to_fire_risk_index[pixel_humidity_color]

                temp = color_to_temp[pixel_temp_color]
                hum = humidity_to_fire_risk_index[pixel_humidity_color] -0.015*future_years

                temp = temp + 0.45*future_years

            except:
                pass

            try:

                if (temp >= 70):
                    new_temp_index = 6.25

                elif (temp >= 65):
                    new_temp_index = 5.5

                elif (temp >= 60):
                    new_temp_index = 4.75

                elif (temp >= 55):
                    new_temp_index = 4

                elif (temp >= 50):
                    new_temp_index = 3.25

                elif (temp >= 45):
                    new_temp_index = 2.5

                elif (temp >= 40):
                    new_temp_index = 1.75

                elif (temp >= 35):
                    new_temp_index = 1

                # if the temp color changes to a new color then return the new color and update the index

                fire_risk_index = new_temp_index + hum

                if get_vegetation_pixels(x, y, veg_rgb) == "None":

                    fire_risk_index = 0

                elif get_vegetation_pixels(x, y, veg_rgb) == "High":

                    fire_risk_index = fire_risk_index * 1.2

            except:

                if get_vegetation_pixels(x, y, veg_rgb) == "None":

                    fire_risk_index = 0

                elif get_vegetation_pixels(x, y, veg_rgb) == "High":

                    fire_risk_index = fire_risk_index * 1.1

            try:
                if (fire_risk_index >= 12 and fire_risk_index <= 16):
                    blankmappixels[x, y] = (255, 0, 0)

                if (fire_risk_index >= 8 and fire_risk_index <= 11):
                    blankmappixels[x, y] = (255, 165, 0)

                if (fire_risk_index >= 4 and fire_risk_index <= 7):
                    blankmappixels[x, y] = (255, 255, 0)

                if (fire_risk_index >= 0 and fire_risk_index <= 3):
                    blankmappixels[x, y] = (144, 238, 144)
                
                if get_humidity_pixels(x, y, hum_rgb) == "water":
                    blankmappixels[x, y] = (54, 195, 255)
                


            except:

                pass

    blankmap.save("blankmap.png")
    blankmap.show()

futureSimulation(city, state)
