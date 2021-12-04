import requests, json, tkinter


def geocode(address):
    params = {
        'access_token': "pk.eyJ1IjoidGVjaGVyZXRpYyIsImEiOiJja3FlNGVuYjcwNWdrMnBwZXY1ZG9obHN3In0.OmN8b-Ys8zo6TXYnZ1tclg",
        'limit': int(input('Введите количество ответов, которые вы хотите получить(максимум 10): ')),
        'types': 'address,poi'
        #'bbox': [57., 58., 59., 59.]
    }

    def code_to_URL(string):
        res = ''
        '''
        for i in '.,':
            string = string.replace(i, '')
        '''
        for el in string:

            if not el:
                n = "%20"
            elif r'\x' in str(el.encode()):
                n = "%".join([i.upper() for i in str(el.encode())[2:-1].split(r'\x')])
            else:
                n = el
            res += n
        return '%20'.join(res.split())

    print(address)
    encoded_address = code_to_URL(address)
    print(encoded_address)
    geo = requests.get(f"http://api.mapbox.com/geocoding/v5/mapbox.places/{encoded_address}.json", params=params)
    # print(*geo.text.split(','), sep='\n')
    di = dict(json.loads(geo.text))

    if di:
        for feature in di['features']:
        #print(feature)
            print(f"{'Место развлечения - ' if 'poi' in feature['place_type'] else 'Адрес - '}"
                  f"{feature['place_name']}, {feature['geometry']['coordinates'][::-1]}")
        return f"Координаты {address}: {di['features'][0]['geometry']['coordinates'][::-1]}"
    return 'Not found'

while True:
    print(geocode(input()))
'''
def show_coords():
    res = geocode(input_form.get())
    output.configure(text=f'Результат: {res}')
    print(res)



display = tkinter.Tk()
display.title('Geocoder')
display.geometry('800x600')
input_form = tkinter.Entry(display)
inst = tkinter.Label(text='Введите адрес')
output = tkinter.Label(text='Результат:')
conv = tkinter.Button(text='Узнать координаты', command=show_coords)
title = tkinter.Label(display, text='Geocoder', font=('Cambria', 75), fg='red')

title.place(x=190, y=0)
input_form.place(x=20, y=150)
inst.place(x=25, y=170)
output.place(x=300, y=150)
conv.place(x=150, y=150)
display.mainloop()
'''
