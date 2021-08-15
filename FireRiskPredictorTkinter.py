from PIL import ImageTk,Image

from numpy import interp

import pandas as pd

import time

import tkinter

from tkinter import*




# def interaction(city, state):
#     fireRiskIndex = GetFireRiskFromCity(city, state)

#     fireRiskIndexYears = fireRiskIndex + 0.45* years/5
    

    
#install library "openpyxl" as well



df = pd.read_excel("uscities.xlsx")

temp_color_to_fire_risk_index= {"dark_red": 8, "red" : 7 , "orange": 6, "yellow": 5, "blue": 4, "green": 3, "purple": 2, "pink": 1}

humidity_to_fire_risk_index = {"blue": 1, "dark_green": 2, "green" : 3, "yellow_green" : 4, "light_green" : 5, "yellow" : 6, "orange" : 7, "red" : 8}

state = input("Enter your state (Ex. Texas): ")

city = input("Enter your city (Ex. Boston): ")



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
    else:
        return "red"






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





def getFireRiskIndex(pixel_temp_color, pixel_humidity_color):

    #dictionaries for pixel color, risk index, and temp/humidity numbers
    temp_color_to_fire_risk_index= {"dark_red": 8, "red" : 7 , "orange": 6, "yellow": 5, "blue": 4, "green": 3, "purple": 2, "pink": 1}

    color_to_temp = {"dark_red": 72.5, "red" : 67.5 , "orange": 62.5, "yellow": 57.5, "blue": 52.5, "green": 47.5, "purple": 42.5, "pink": 37.5}

    temp_to_color = {value : key for (key, value) in color_to_temp.items()}

    humidity_to_fire_risk_index = {"blue": 1, "dark_green": 2, "green" : 3, "yellow_green" : 4, "light_green" : 5, "yellow" : 6, "orange" : 7, "red" : 8}
    
    #calc fire risk index
    fire_risk_index = temp_color_to_fire_risk_index[pixel_temp_color] + humidity_to_fire_risk_index[pixel_humidity_color]
    return fire_risk_index





def GetFireRiskFromCity(city, state):

    lat = getLatlongitude(city, state)[0]

    longitude = getLatlongitude(city, state)[1]

    temp = get_temp(lat, longitude)

    humidity = get_humidity(lat, longitude)

    fire_risk_index = getFireRiskIndex(temp, humidity)

    return fire_risk_index





#Start of user interaction
"""try:
    try:
        years = int(input("How many years into the future would you like to see the impact of climate change? "))
    except:
        print("That is not a valid number!")
        
    fireRiskIndex = GetFireRiskFromCity(city, state)

    fireRiskIndexYears = fireRiskIndex + 0.45*years/5

    print("The chance of a fire emerging in your area will increase by ", round(100*fireRiskIndexYears/fireRiskIndex - 100, 0), "% over the next ", years," years")
    
    time.sleep(5)

    if (humidity_to_fire_risk_index[get_humidity(getLatlongitude(city, state)[0], getLatlongitude(city, state)[1])] > temp_color_to_fire_risk_index[get_temp(getLatlongitude(city, state)[0], getLatlongitude(city, state)[1])]):
        
        print("The main cause of these fires is humidity")

        time.sleep(6)

        print("To save planet Earth in the future by preventing changes in humidity, you can start by:")

        time.sleep(2)

        print("Waste less water. Using too much water can cause inbalances in water concentration in the atmosphere, changing the humidity.")
        
        time.sleep(6)

        print("Plant more trees and grow your own food. Plants help maintain the concentration of water in the soil and atmosphere, keeping humidity levels stable.")
    
    else:
        print("The main cause of these fires is global warming")

        time.sleep(6)

        print("To save planet Earth in the future by preventing increases in temperature, you can start by:")

        time.sleep(2)

        print("Generate less trash, make sure to recycle and compost as much as possible. Pollution traps heat which causes more fires.")
        
        time.sleep(6)

        print("Ride a bike or walk next time you need to go somewhere. The exhaust from car engines releases toxic pollutants into the atmosphere that warm the globe.")
    
    time.sleep(4)







    def Impact(fire_risk_index):
        affected_toll = 100 * pow(10, fire_risk_index/2.5 - 4)

        acres = 2000 * pow(10, fire_risk_index/2.5 - 4)

        cost = 2000000 * pow(10, fire_risk_index/2.5 - 4)

        return round(affected_toll, 0), round(acres, 0), round(cost, 0)
    
    print("The number of people impacted per fire will increase by ", Impact(fireRiskIndexYears)[0] - Impact(fireRiskIndex)[0], " people in ", years, " years")
    
    time.sleep(4)

    print("The number of acres destroyed per fire will increase by ", Impact(fireRiskIndexYears)[1] - Impact(fireRiskIndex)[1], " acres in ", years, " years")
    
    time.sleep(4)

    print("The repair costs per fire will increase by ", Impact(fireRiskIndexYears)[2] - Impact(fireRiskIndex)[2], " dollars in ", years, " years")

    print("Climate change is a serious issue.")

    time.sleep(3)

    print("Stop.")

    time.sleep(1)

    print("Climate change.")

    time.sleep(1)

    print("Now.")

except:

    print("Invalid input")"""

def data(city, state, year):
    fire_risk_increase(city, state, year)

    fire_risk(city, state, year)

    fri = Label(window, text = fire_risk_increase(city, state, year))
    fri.grid(row=1, column=4)

    frl = Label(window, text = "Fire Risk: " +fire_risk_level(city, state, year))
    frl.grid(row=2, column=4)

    at = Label(window, text = "affected: " + affected_toll(fire_risk(city,state)))
    at.grid(row=3, column=4)

    acrs = Label(window, text = "acres burned: " +acres(fire_risk(city, state)))
    acrs.grid(row=4, column=4)

    cost = Label(window, text = "cost: " +cost(fire_risk(city, state)))
    cost.grid(row=5, column=4)


def fire_risk_increase(city, state, years):
    fireRiskIndex = GetFireRiskFromCity(city, state)

    fireRiskIndexYears = fireRiskIndex + 0.45*years/5

    return "The chance of a fire emerging in your area will increase by ", round(100*fireRiskIndexYears/fireRiskIndex - 100, 0), "% over the next ", years," years"


def fire_risk_level(city, state, years):
    
    fire_risk_index = GetFireRiskFromCity(city, state)


    try:
        if (fire_risk_index >= 12 and fire_risk_index <= 16):
            return "super high"

        if (fire_risk_index >= 8 and fire_risk_index <= 11):
            return "very high"

        if (fire_risk_index >= 4 and fire_risk_index <= 7):
            return "high"

        if (fire_risk_index > 0 and fire_risk_index <=3):
            return "medium"

        if (fire_risk_index == 0):
            return "low"

    except:

        pass

def fire_risk(city, state):
    fireRiskIndex = GetFireRiskFromCity(city, state)
    return fireRiskIndex

def affected_toll(fire_risk_index):
        affected_toll = 100 * pow(10, fire_risk_index/2.5 - 4)
        return str(round(affected_toll, 0))

def acres(fire_risk_index):
    acres = 2000 * pow(10, fire_risk_index/2.5 - 4)
    return str(round(acres, 0))

def cost(fire_risk_index):
    cost = 2000000 * pow(10, fire_risk_index/2.5 - 4)
    return str(round(cost, 0))



    

window = Tk()

window.geometry("300x300")

window.title("Fire Prediction Model")


Fount_tuple_title = ("Cambria", 31, "bold")

Font_tuple_important_text = ("Cambria", 23, "bold")

Font_tuple_text = ("Cambria", 23)


canvas = Canvas(window, width = 300, height = 300)


canvas.grid(row = 0, rowspan= 5, column = 0, columnspan = 5)


city = Entry(window)

city.grid(row = 2, column = 0)

state = Entry(window)

state.grid(row = 3, column = 0)

year = Entry(window)

year.grid(row = 4, column = 0)

submit = Button(window, text= "submit fields", command = data(city.get(), state.get(), year.get()))
submit.grid(row= 5, column=0)


window.mainloop()




