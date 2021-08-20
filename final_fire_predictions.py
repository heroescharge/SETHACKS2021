from PIL import Image

from numpy import interp

latitude = 40.6943
longitude = -73.9249

blank_map = Image.open("blank_map.png")
blank_map.resize((800,488), Image.ANTIALIAS)
blank_map_pixels = blank_map.load()

temp_img = Image.open("temperature_map.png")
temp_img.resize((800,488), Image.ANTIALIAS)
temp_width, temp_height = temp_img.size
temp_rgb = temp_img.convert("RGB")


humidity_img = Image.open("humidity_map.png")
humidity_img.resize((800,488), Image.ANTIALIAS)
hum_width, hum_height = humidity_img.size
hum_rgb = humidity_img.convert("RGB")


vegetation_img = Image.open("vegetation_map.png")
vegetation_img.resize((800,488), Image.ANTIALIAS)
veg_width, veg_height = vegetation_img.size
veg_rgb = vegetation_img.convert("RGB")


def get_temp(pixel_x, pixel_y, temp_rgb):


    r, g, b = temp_rgb.getpixel((pixel_x, pixel_y))


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

    elif ((r >= 0 and r <= 5) and (g >= 0 and g <= 5) and (b >= 0 and b <= 5) ):
            return "black"

    else:
        return "yellow"




def get_humidity(pixel_x, pixel_y, hum_rgb):

    #Set up images

    r, g, b = hum_rgb.getpixel((pixel_x, pixel_y))


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

        elif ((r >= 0 and r <= 5) and (g >= 0 and g <= 5) and (b >= 0 and b <= 5) ):
            return "black"

        else:
            return "yellow"









def get_vegetation(pixel_x, pixel_y, veg_rgb):

    #Set up images

    r, g, b = veg_rgb.getpixel((pixel_x, pixel_y))

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
            return "Low"

        elif ((r >= 220 and r <= 240) and (g >= 211 and g <= 231) and (b >= 159 and b <= 179)): 
            return "High"

        elif ((r >= 202 and r <= 222) and (g >= 227 and g <= 247) and (b >= 239 and b <= 259)):
            return "None"

        elif ((r >= 118 and r <= 138) and (g >= 149 and g <= 169) and (b >= 84 and b <= 104)): 
            return "High"

        elif ((r >= 171 and r <= 191) and (g >= 195 and g <= 215) and (b >= 167 and b <= 187)):
            return "Medium"

        elif ((r >= 125 and r <= 152) and (g >= 160 and g <= 195) and (b >= 90 and b <= 165)):
            return "Medium"

        elif ((r >= 0 and r <= 5) and (g >= 0 and g <= 5) and (b >= 0 and b <= 5) ):
            return "black"

        else:
            return "Medium"






#START OF SIMULATION



def futureSimulation():
    
    future_years = int(input("Enter number of years into the future you wish to see the impact of climate change"))

    temp_color_to_fire_risk_index= {"dark_red": 8, "red" : 7 , "orange": 6, "yellow": 5, "blue": 4, "green": 3, "purple": 2, "pink": 1, "water": 0, "black": 0}
    color_to_temp = {"dark_red": 72.5, "red" : 67.5 , "orange": 62.5, "yellow": 57.5, "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5, "water": 0, "black": 0}
    humidity_to_fire_risk_index = {"blue": 1, "dark_green": 2, "green" : 3, "yellow_green" : 4, "light_green" : 5, "yellow" : 6, "orange" : 7, "red" : 8, "water": 0, "black": 0}

    width, height = blank_map.size

    img_y = interp(latitude, [25.712922, 49.044568], [1,height])
    img_x = interp(longitude, [-124.523822,-66.621243], [1,width])

    img_x = img_x.round()
    img_y = img_y.round()

    img_y = height-img_y

    #increasing temperature as years continue

    for x in range(0, width):    
        for y in range(0, height):
        
            pixel_temp_color = get_temp(x,y, temp_rgb)
            pixel_humidity_color = get_humidity(x,y, hum_rgb)

            fire_risk_index = temp_color_to_fire_risk_index[pixel_temp_color] + humidity_to_fire_risk_index[pixel_humidity_color]
            
            temp = color_to_temp[pixel_temp_color]
            temp = temp + 0.45*future_years

            if (temp >= 70): 
                new_temp_index = 8

            elif (temp >= 65):
                new_temp_index = 7

            elif (temp >= 60):
                new_temp_index = 6

            elif (temp >= 55):
                new_temp_index = 5

            elif (temp >= 50):
                new_temp_index = 4

            elif (temp >= 45):
                new_temp_index = 3

            elif (temp >= 40):
                new_temp_index = 2

            elif (temp >= 35):
                new_temp_index = 1

            else:
                new_temp_index = 0

            #if the temp color changes to a new color then return the new color and update the index
                
            fire_risk_index = new_temp_index + humidity_to_fire_risk_index[pixel_humidity_color]
            
            if get_vegetation(x,y, veg_rgb) == "None":
                fire_risk_index = 0
            
            elif get_vegetation(x,y, veg_rgb)== "High":
                fire_risk_index = fire_risk_index * 1.25

            elif get_vegetation(x, y, veg_rgb) == "water" or get_vegetation(x, y, veg_rgb) == "black":
                fire_risk_index = 0

            if (fire_risk_index >= 11 and fire_risk_index <= 16):
                blank_map_pixels[x,y] = (255, 0, 0)

            if (fire_risk_index >= 8 and fire_risk_index <= 10):
                blank_map_pixels[x,y] = (255, 165, 0)

            if (fire_risk_index >= 4 and fire_risk_index <= 7):
                blank_map_pixels[x,y] = (255, 255, 0)

            if (fire_risk_index > 0 and fire_risk_index <=3):
                blank_map_pixels[x,y] = (144, 238, 144)

            if (fire_risk_index == 0):
                blank_map_pixels[x,y] = (255, 255, 255)


        blank_map.save("blank_map.png")
    blank_map.show()     
                                

futureSimulation()
