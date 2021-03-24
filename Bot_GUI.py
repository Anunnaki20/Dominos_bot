import tkinter as tk

#Globals
HEIGHT = 500
WIDTH = 600
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

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# background image
background_image = tk.PhotoImage(file='Gui_photos/vapor_wave.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Button frame
button_frame = tk.Frame(root, bg='#80c1ff', bd=5)
button_frame.place(relx=0.5, rely=0.95, relwidth=0.2, relheight=0.1, anchor='s')

drop_frame = tk.Frame(root, bg='#80c1ff', bd=5)
drop_frame.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.1, anchor='n')

# Drop down menu for selecting the province
province = tk.StringVar(root)
province.set(PROVINCE_OPTIONS[0])
drop_down = tk.OptionMenu(drop_frame, province, *PROVINCE_OPTIONS)
drop_down.place(relx=0, relwidth=1, relheight=1)

button = tk.Button(button_frame, text="RUN")
button.place(relx=0, relwidth=1, relheight=1)



root.mainloop()



