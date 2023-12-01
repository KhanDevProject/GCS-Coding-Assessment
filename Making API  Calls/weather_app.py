# import all the necessary libraries 
from tkinter import *
from configparser import ConfigParser
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import customtkinter as ctk

# OpenWeatherMap API URL with placeholders for city name and API key
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
# Configuration file containing API keys and other settings
config_file = 'config.ini'
# Create a ConfigParser object to read the configuration file
config = ConfigParser()
# Read the API key from the configuration file
config.read(config_file)
api_key = config['api_key']['key']


# Function to retrieve weather information for a given city using an API
def get_weather(city):
    # Make a request to the weather API using the provided city and API key
    result = requests.get(url.format(city, api_key))
    # Check if the request was successful
    if result:
        # Parse the JSON response
        json = result.json()
        # Extract relevant weather information from the JSON response
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        humidity = json['main']['humidity']
        # Create a tuple containing the weather details
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather, humidity)
        # Return the tuple with weather information
        return final
    else:
        # Return None if the request was not successful
        return None


# Function to add a city to the list of favorite cities
def add_to_favorites():
    # Get the city name from the input field
    city = city_text.get()
    # Check if the city is not already in the list of favorite cities
    if city not in favorite_cities:
        # Check if the maximum limit of 3 favorite cities has not been reached
        if len(favorite_cities) < 3:
            # Add the city to the list of favorite cities
            favorite_cities.append(city)
            # Update the displayed list of favorite cities in the widget
            update_favorites_list()
            # Update the displayed weather details for favorite cities
            show_favorite_weathers()
            # Force an update before displaying the message box
            app.update_idletasks()
            # Show a success message indicating the added city
            messagebox.showinfo('Success', f'{city} added to favorites!')
        else:
            # Show a warning if the maximum limit of 3 favorite cities is reached
            messagebox.showwarning('Warning', 'Maximum limit of 3 favorite cities reached!')
    else:
        # Show an information message if the city is already in favorites
        messagebox.showinfo('Info', f'{city} is already in favorites.')

# Function to remove a city from the list of favorite cities
def remove_from_favorites():
    # Get the index of the selected city in the favorites_listbox
    selected_index = favorites_listbox.curselection()
    # Check if a city is selected
    if selected_index:
        # Remove the selected city from the favorite_cities list
        removed_city = favorite_cities.pop(selected_index[0])
        # Update the displayed list of favorite cities in the widget
        update_favorites_list()
        # Update the displayed weather details for favorite cities
        show_favorite_weathers()
        # Show a success message indicating the removed city
        messagebox.showinfo('Success', f'{removed_city} removed from favorites!')
    else:
        # Show an information message if no city is selected for removal
        messagebox.showinfo('Info', 'Please select a city to remove.')


# Function to update the list of favorite cities in the favorites_listbox widget
def update_favorites_list():
    # Clear the current content in the favorites_listbox widget
    favorites_listbox.delete(0, END)

    # Iterate through the list of favorite cities and add them to the widget
    for favorite_city in favorite_cities:
        favorites_listbox.insert(END, favorite_city)


# Function to display weather details for favorite cities
def show_favorite_weathers():
    # Clear previous content in the favorites_weather_txt widget
    favorites_weather_txt.delete('1.0', END)
    # Iterate through the favorite cities and fetch weather details
    for city in favorite_cities:
        # Retrieve weather information for the current city
        weather = get_weather(city)
        # Check if weather information is available for the city
        if weather:
            # Display weather details for the current city in the widget
            favorites_weather_txt.insert(END, f'{city}: {weather[2]:.2f}°C, {weather[3]:.2f}°F, {weather[5]}, Humidity: {weather[6]}\n')
        else:
            # Display an error message if weather information cannot be fetched for the city
            favorites_weather_txt.insert(END, f'Error fetching weather for {city}\n')


# Function to search for the weather of a specified city
def search():
    # Get the city name from the input field
    city = city_text.get()
    # Retrieve the weather information for the specified city
    weather = get_weather(city)
    # Check if weather information is available
    if weather:
        # Update the location label with city and country
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        # Load the weather icon and display it
        img = Image.open(f'weather_icons/{weather[4]}.png')
        img = img.resize((50, 50), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image.config(image=photo)
        image.image = photo
        # Update temperature label with Celsius and Fahrenheit values
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        # Update weather condition label
        weather_lbl['text'] = weather[5]
        # Update humidity label
        humditiy_lbl['text'] = 'Humidity: {}'.format(weather[6])
    else:
        # Display an error message if the city cannot be found
        messagebox.showerror('Error', 'Cannot find weather information for {}'.format(city))

# Create Tkinter window
app = ctk.CTk()
app.title("Weather App")
app.geometry("700x500")
app.iconbitmap('weather_icons\weather.ico')  # Set window icon

# Create the first frame for weather details
frame = ctk.CTkFrame(master=app, width=290, height=310)
frame.place(x=20, y=30)
frame_color = frame['bg']  # Store the background color of the frame

# Create the second frame for additional features or information
frame2 = ctk.CTkFrame(master=app, width=330, height=370)
frame2.place(x=330, y=30)


# Create a StringVar to hold the text in the city entry field
city_text = StringVar()

# Create an entry widget for the user to input the city name
city_entry = ctk.CTkEntry(master=frame, textvariable=city_text)
city_entry.insert(0, "Search City")  # Default text in the entry field
city_entry.bind("<FocusIn>", lambda event: city_entry.delete(0, "end"))  # Clear default text on focus
city_entry.bind("<FocusOut>", lambda event: city_entry.insert(0, "Search City"))  # Restore default text on focus out
city_entry.place(x=17, y=10)  # Position the entry field

# Create a search button with specified attributes
frame_color = frame['bg']
search_btn = ctk.CTkButton(master=frame, text='Search Weather', width=16, fg_color=(frame_color), command=search)
search_btn.place(x=167, y=10)  # Position the search button

# Create a label to display the location information with specified attributes
location_lbl = Label(frame, text='', font=('bold', 20), fg='white', bg='#2d2d2d')
location_lbl.place(x=23, y=55)  # Position the location label

# Label to display the weather icon
image = Label(frame, bg='#2d2d2d')
image.place(x=33, y=100)  # Position the weather icon label

# Label to display the temperature information
temp_lbl = Label(frame, text='', fg='white', bg='#2d2d2d')
temp_lbl.place(x=23, y=157)  # Position the temperature label

# Label to display the humidity information
humditiy_lbl = Label(frame, text='', fg='white', bg='#2d2d2d')
humditiy_lbl.place(x=23, y=180)  # Position the humidity label

# Label to display the weather condition
weather_lbl = Label(frame, text='', fg='white', bg='#2d2d2d')
weather_lbl.place(x=23, y=200)  # Position the weather condition label

# Button to add the current city to favorites
add_to_favorites_btn = ctk.CTkButton(master=frame2, text='Add to Favorites', fg_color=(frame_color), command=add_to_favorites)
add_to_favorites_btn.place(x=55, y=18)  # Position the "Add to Favorites" button

# Button to remove the selected city from favorites
remove_from_favorites_btn = ctk.CTkButton(master=frame2, text='Remove from Favorites', fg_color=(frame_color), command=remove_from_favorites)
remove_from_favorites_btn.place(x=55, y=50)  # Position the "Remove from Favorites" button

# Listbox to display favorite cities with specified attributes
favorites_listbox = Listbox(frame2, selectmode=SINGLE, font=(10), fg='white', bg='#2d2d2d', height=9)
favorites_listbox.place(x=40, y=90)  # Position the listbox for favorite cities

# Text widget to display weather details of favorite cities
favorites_weather_txt = Text(frame2, font=('bold', 10), fg='white', bg='#2d2d2d', height=4, width=44)
favorites_weather_txt.place(x=9, y=270)  # Position the text widget for weather details

# List to store favorite cities
favorite_cities = []  # Initialize an empty list to store favorite cities

# Start the Tkinter event loop
app.mainloop()
