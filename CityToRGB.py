from PIL import Image
from numpy import interp
import pandas as pd
#install library "openpxyl" as well 

df = pd.read_excel("uscities.xlsx")

city = 'Houston'
state = 'Texas'
def getLatLong(city, state):
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
        long = cityDataArr[3]
        coords = [lat, long]
        return coords
    else:
        print("city not found")

def make_risk_index(lat, long, sampleSquareSize):

    #Set up images
    fire_img = Image.open("fires.png")

    
    width, height = fire_img.size
    pixel_rgb = fire_img.convert("RGB")

    #Get x and y positions of pixel representing city
    img_y = interp(lat, [23.765829, 49.523027], [1,height])
    img_x = interp(long, [-125.591848,-66.375709], [1,width])
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
    
print(make_risk_index(getLatLong(city, state)[0], getLatLong(city, state)[1], 10))
