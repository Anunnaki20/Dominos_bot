import tkinter as tk
import Dominos_bot as Dominos_bot

# Globals
HEIGHT = 600
WIDTH = 800
PROVINCE_OPTIONS = ["Alberta",
                    "British Columbia",
                    "Manitoba",
                    "New Brunswick",
                    "Nova Scotia",
                    "Northwest Territories",
                    "Nunavut",
                    "Ontario",
                    "Prince Edward Island",
                    "Quebec",
                    "Saskatchewan",
                    "Yukon"
                    ]
MAJOR_CITY = {"Alberta": ["Calgary", "Edmonton", "Red Deer"],
              "British Columbia": ["Vancouver"],
              "Saskatchewan": ["Saskatoon", "Regina"]}

province_selected = "Alberta"
city_global = None

def upper_check():
    string = ""
    try:
        if int(upper.get()) < int(lower.get()):
            string += "End search needs to be greater then the lower one\n"
        if int(upper.get()) > 10000:
            string += "End search can't be greater than 10000\n"
    except:
        string = "ERROR no input in the coupon end search\n"
    return string


def lower_check():
    string = ""
    try:
        if int(lower.get()) < 0:
            string += "Start of the coupon search needs to be greater then 0\n"
        if int(lower.get()) > 9999:
            string += "Start of the coupon search can't be greater than 9999\n"
    except:
        string = "ERROR no input in the coupon start search\n"
    return string


def postal_code_check():
    string = ""
    try:
        if len(postal_code.get()) > 7:
            string += "Postal code is greater then 7 characters\n"
        if len(postal_code.get()) < 6:
            string += "Postal code is not the proper length\n"
    except:
        string = "ERROR no postal code given\n"
    return string


root = tk.Tk()
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# background image
background_image = tk.PhotoImage(file='Gui_photos/vapor_wave.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# frames
button_frame = tk.Frame(root, bg='#000000', bd=5)
button_frame.place(relx=0.5, rely=0.97, relwidth=0.2, relheight=0.1, anchor='s')

drop_frame_province = tk.Frame(root, bg='#000000', bd=5)
drop_frame_province.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.1, anchor='n')

postal_code_frame = tk.Frame(root, bg='#000000', bd=5)
postal_code_frame.place(relx=0.5, rely=0.16, relwidth=0.8, relheight=0.08, anchor='n')

drop_frame_city = tk.Frame(root, bg='#000000', bd=5)
drop_frame_city.place(relx=0.5, rely=0.25, relwidth=0.8, relheight=0.1, anchor='n')

Time_delay_frame = tk.Frame(root, bg='#000000', bd=5)
Time_delay_frame.place(relx=0.5, rely=0.36, relwidth=0.8, relheight=0.08, anchor='n')

lower_frame = tk.Frame(root, bg='#000000', bd=5)
lower_frame.place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.08, anchor='n')

upper_frame = tk.Frame(root, bg='#000000', bd=5)
upper_frame.place(relx=0.5, rely=0.54, relwidth=0.8, relheight=0.08, anchor='n')

display_frame = tk.Frame(root, bd=5)
display_frame.place(relx=0.5, rely=0.65, relwidth=0.8, relheight=0.2, anchor='n')


def test(selection):
    global city_global
    city_global = selection


# Create the city drop down from the province option
def city_drop_down(selection):
    global province_selected, city_global
    province_selected = selection
    city = tk.StringVar(root)
    city.set(MAJOR_CITY[selection][0])
    city_global = MAJOR_CITY[selection][0]
    drop_down_city = tk.OptionMenu(drop_frame_city, city, *MAJOR_CITY[selection], command=test)
    drop_down_city.place(relx=0.5, relwidth=0.5, relheight=1)


drop_down_city_label = tk.Label(drop_frame_city, text="Select city here: ")
drop_down_city_label.place(relx=0, relwidth=0.5, relheight=1)

# Drop down menu for selecting the province
province = tk.StringVar(root)
province.set(PROVINCE_OPTIONS[0])
drop_down_prov = tk.OptionMenu(drop_frame_province, province, *PROVINCE_OPTIONS, command=city_drop_down)
drop_down_prov.place(relx=0.5, relwidth=0.5, relheight=1)
drop_down_label = tk.Label(drop_frame_province, text="Select province here: ")
drop_down_label.place(relx=0, relwidth=0.5, relheight=1)

city_drop_down(province.get())

# Input box for postal code
postal_code = tk.Entry(postal_code_frame)
postal_code.place(relx=0.5, relwidth=0.5, relheight=1)
postal_code_label = tk.Label(postal_code_frame, text="Enter postal_code here: ")
postal_code_label.place(relx=0, relwidth=0.5, relheight=1)

# Input box for time delay
default = tk.StringVar(root, value='1')
time_delay = tk.Entry(Time_delay_frame, font=20, textvariable=default)
time_delay.place(relx=0.5, relwidth=0.5, relheight=1)
time_delay_label = tk.Label(Time_delay_frame, text="Enter time delay here\n (NOTE: for fast internet put 1): ")
time_delay_label.place(relx=0, relwidth=0.5, relheight=1)

# Input box for lower
lower = tk.Entry(lower_frame, font=20)
lower.place(relx=0.5, relwidth=0.5, relheight=1)
lower_label = tk.Label(lower_frame, text="Enter the start of the coupon search: ")
lower_label.place(relx=0, relwidth=0.5, relheight=1)

# Input pox for upper delay
upper = tk.Entry(upper_frame, font=20)
upper.place(relx=0.5, relwidth=0.5, relheight=1)
upper_label = tk.Label(upper_frame, text="Enter the end of the coupon search: ")
upper_label.place(relx=0, relwidth=0.5, relheight=1)

# Display
display = tk.Entry(display_frame)
display.place(relwidth=1, relheight=1)


def run():
    string = ""
    string += upper_check()
    string += lower_check()
    string += postal_code_check()
    if string == "":
        Dominos_bot.main(int(time_delay.get()),
                         int(lower.get()),
                         int(upper.get()),
                         city_global,
                         postal_code.get(),
                         province_selected)
    label['text'] = string


# Run Button
button = tk.Button(button_frame, text="RUN", command=lambda: run())
button.place(relx=0, relwidth=1, relheight=1)

label = tk.Label(display_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()
