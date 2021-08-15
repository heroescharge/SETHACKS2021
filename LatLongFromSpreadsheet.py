from PIL import Image

from numpy import interp

import pandas as pd
#install library "openpyxl" as well

df = pd.read_excel("uscities.xlsx")

state = input("Enter your state")
city = input("Enter your city")



def getLatlongitude(city, state):
    
    cityRowArr = df[df['city'] == city].index.values

    cityRowNumber = -1 #-1 means no row number exists

    #Check if state is correct as well
    for i in range(0, len(cityRowArr)):

        if df.loc[cityRowArr[i]][1] == state: #index 0 = city, 1 = state, 2 = lat, 3 = long

            cityRowNumber = cityRowArr[i] #note that the row index is two less than the row number in excel
            
    #make sure that city exists
    if cityRowNumber != -1:

        cityDataArr = df.loc[cityRowNumber]

        lat = cityDataArr[2]

        longitude = cityDataArr[3]

        return [lat,longitude]
    else:
        print("city not found")




def make_risk_index(lat, longitude, sampleSquareSize):

    #Set up images
    fire_img = Image.open("fires.png")
    
    width, height = fire_img.size

    pixel_rgb = fire_img.convert("RGB")

    #Get x and y positions of pixel representing city
    img_y = interp(lat, [23.765829, 49.523027], [1,height])

    img_x = interp(longitude, [-125.591848,-66.375709], [1,width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y
    
    r_values = []

    g_values = []

    b_values = []
    
    for x in range(-sampleSquareSize, sampleSquareSize):

        for y in range (-sampleSquareSize, sampleSquareSize):

            try:
                r, g, b = pixel_rgb.getpixel((img_x + x, img_y + y))
                
                if ((r >= 185 and r <= 215) and (b >= 20 and b <= 230) and (g >= 165 and g <= 200)):
                    pass

                else:
                    r_values.append(r)

                    g_values.append(g)

                    b_values.append(b)

            except:
                pass

    try:
        return round(sum(r_values)/len(r_values), 0), round(sum(g_values)/len(g_values), 0), round(sum(b_values)/len(b_values), 0)

    except:
        print("no non-ocean pixels found")
            

def get_temp(lat, longitude):

    temp_img = Image.open("tempreture_map.png")

    temp_img = temp_img.resize((360, 195))

    width, height = temp_img.size

    temp_rgb = temp_img.convert("RGB")

    #Get x and y positions of pixel representing city
    img_y = interp(lat, [24.382257, 50.532143], [1,height])

    img_x = interp(longitude, [-125.591848,-66.375709], [1,width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y

    r, g, b = temp_rgb.getpixel((img_x, img_y))

    if ((r >= 122 and r <= 128) and (g >= 21 and g <= 27) and (b >= 25 and b <= 31)):
        return "dark red"

    elif ((r >= 227 and r <= 233) and (g >= 16 and g <= 22) and (b >= 22 and b <= 28)):
        return "red"

    elif ((r >= 242 and r <= 248) and (g >= 167 and g <= 163) and (b >= 22 and b <= 28)):
        return "orange"

    elif ((r >= 237 and r <= 243) and (g >= 232 and g <= 238) and (b >= 47 and b <= 53)):
        return "yellow"

    elif  ((r >= 67 and r <= 73) and (g >=182 and g <= 188) and (b >= 137 and b <= 143)):
        return "blue"

    elif ((r >= 32 and r <= 38) and (g >= 80 and g <= 86) and (b >= 162 and b <= 168)):
        return "green"

    elif ((r >= 107 and r <= 113) and (g >= 62 and g <= 68) and (b >= 147 and b <= 153)):
        return "purple"

    elif ((r >= 222 and r <= 228) and (g >= 90 and g <= 97) and (b >= 155 and b <= 161)):
        return "pink" 

    elif ((r >= 250 and r <= 255) and (g >= 250 and g <= 255) and (b >= 250 and b <= 255)):
        return "Water"




def get_humidity(lat, longitude):

    #Set up images
    humidity_img = Image.open("humidities.png")

    width, height = humidity_img.size

    pixel_rgb = humidity_img.convert("RGB")

    img_y = interp(lat, [24.382257, 50.532143], [1,height])

    img_x = interp(longitude, [-125.591848,-66.375709], [1,width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y
    #Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((img_x, img_y))

    except:
        return "pixel does not exist"

    if ((r >= 200 and r <= 210) and (g >= 223 and g <= 233) and (b >= 242 and b <= 252)):
            return ("pixel part of ocean")

    elif ((r >= 224 and r <= 234) and (g >= 213 and g <= 223) and (b >= 199 and b <= 209)):
        return ("part of land")

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


def get_vegetation(lat, longitude):

    #Set up images
    vegetation_img = Image.open("vegetations.png")

    width, height = vegetation_img.size

    pixel_rgb = vegetation_img.convert("RGB")

    img_y = interp(lat, [24.382257, 50.532143], [1,height])

    img_x = interp(longitude, [-125.591848,-66.375709], [1,width])

    img_x = img_x.round()

    img_y = img_y.round()

    img_y = height - img_y
    #Get color of pixel
    try:
        r, g, b = pixel_rgb.getpixel((img_x, img_y))

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


def getFireRiskIndex(pixel_temp_color, pixel_humidity_color):

    #dictionaries for pixel color, risk index, and temp/humidity numbers
    temp_color_to_fire_risk_index= {"dark_red": 8, "red" : 7 , "orange": 6, "yellow": 5, "blue": 4, "green": 3, "purple": 2, "pink": 1}

    color_to_temp = {"dark_red": 72.5, "red" : 67.5 , "orange": 62.5, "yellow": 57.5, "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5}

    temp_to_color = {value : key for (key, value) in color_to_temp.items()}

    humidity_to_fire_risk_index = {"blue": 8, "dark_green": 7, "green" : 6, "yellow_green" : 5, "light_green" : 4, "yellow" : 3, "orange" : 2, "red" : 1}
    
    #calc fire risk index
    fire_risk_index = temp_color_to_fire_risk_index[pixel_temp_color] + humidity_to_fire_risk_index[pixel_humidity_color]

    print(fire_risk_index)





#START OF SIMULATION

def GetFireRiskFromLatLong(lat, longitude):

    coords = getLatlongitude(city, state)

    lat = coords[0]

    longitude = coords[1]

    temp = get_temp(lat, longitude)

    humidity = get_humidity(lat, longitude)

    fire_risk_index = getFireRiskIndex(temp, humidity)

    return fire_risk_index


def ShowSimulation(city, state):

    future_years = input("How many years do you want to see in the future? ")
    
    #Get initial temp
    temp_color_to_fire_risk_index= {"dark_red": 8, "red" : 7 , "orange": 6, "yellow": 5, "blue": 4, "green": 3, "purple": 2, "pink": 1}
    
    color_to_temp = {"dark_red": 72.5, "red" : 67.5 , "orange": 62.5, "yellow": 57.5, "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5}
    
    humidity_to_fire_risk_index = {"blue": 8, "dark_green": 7, "green" : 6, "yellow_green" : 5, "light_green" : 4, "yellow" : 3, "orange" : 2, "red" : 1}
    
    temp_to_color = {value : key for (key, value) in color_to_temp.items()}

    pixel_temp_color = get_temp(getLatlongitude(city, state)[0], getLatlongitude(city, state)[1])

    print(getLatlongitude(city, state)[0], getLatlongitude(city, state)[1])
    print(pixel_temp_color)

    pixel_humidity_color = get_humidity(getLatlongitude(city, state)[0], getLatlongitude(city, state)[1])

    temp = color_to_temp[pixel_temp_color]

    print(temp)
    
    #Keep increasing temp
    for i in range(int(future_years)):

        #increasing temperature as years continue
        temp = temp + 0.45

        try:
            new_temp_index = temp_to_color[temp]

            #if the temp color changes to a new color then return the new color and update the index
            if new_temp_index != pixel_temp_color:
                
                fire_risk_index = temp_color_to_fire_risk_index[new_temp_index] + humidity_to_fire_risk_index[pixel_humidity_color]
                
                print(fire_risk_index)
                
        except:

            print(fire_risk_index)

ShowSimulation(city, state)
