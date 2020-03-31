# OPEN WEATHER API ID'S
OW_APIKEY = '696685ad63e4a6008a974e16b11aa2f2'
CITY = 'Tashkent'
lon = 69.22
lat = 41.26
cnt = 10
CUR_CITY_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OW_APIKEY}'
CUR_LOC_URL = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_APIKEY}'
CITIES_IN_CIRCLE_URL= f'http://api.openweathermap.org/data/2.5/find?lat={lat}&lon={lon}&cnt={cnt}&appid={OW_APIKEY}'

TOKEN = '1122671928:AAEtjHw1wIBnzI0S8KCgWI2EASxFGgaYRWY'