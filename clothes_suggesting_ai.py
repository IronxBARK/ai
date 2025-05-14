import random
import time
from decouple import config

class ClothingAI:
    ''' ClothingAI will take user temperature and suggest clothing items for each body part.'''
    def __init__(self):
        self.temperature = None
        self.clothing_data = None
        self.weather = None
        
        
    def main(self):
        ''' Main function to run the clothing suggestion AI. '''
        self.temperature = self.get_user_temperature()     # get user temperature
        self.weather = self.get_weather(self.temperature)    # get weather
        self.clothing_data = self.load_clothing_data(config("clothing_data"))[self.weather]  # get data acc. to weather
        
        # weather greet
        print(f"AH! The weather is {self.weather} today.")
        time.sleep(1)
        print("Preparing your cloth set...")
        time.sleep(1)
        
        upper = self._get_clothing("upper")  # get upper clothing
        lower = self._get_clothing("lower") # get lower clothing
        footwear = self._get_clothing("footwear") # get footwear
        sunglasses = self._get_clothing("sunglasses")  # get sunglasses
        accessories = self._get_clothing("accessories")

        print(f"\nYour clothing set for {self.weather} weather:")
        print(f"{upper} and {lower} with {footwear}.\nDon't forget your {sunglasses} and {accessories}!")
            
        
    def _get_clothing(self, type):
        ''' Main clothing function suggesting upper, lower, footwear, sunglasses and accessories'''
        
        data = self.clothing_data[type]
        if not data:
            return f"No {type}"
        
        choosen = random.choice(data)  # choosed cloth        
        self.clothing_data[type].remove(choosen)  # remove choosen cloth from list
        
        print(f"{type.title()} clothing: {choosen}")
        
        liked = input("Do you like this item? (y/n): ").strip().lower()
        return self._liked(choosen, liked, self._get_clothing, type) # check if user liked, if not, get another item
       
    def load_clothing_data(self, file):
        ''' Load clothing data from a JSON file. '''
        import json
        with open(file, 'r') as file:
            clothing_data = json.load(file)
        return clothing_data
    
    def get_user_temperature(self):
        ''' Get user temperature input. '''
        while True:
            try:
                temperature = float(input("Enter your temperature in Celsius: "))
                if temperature < -50 or temperature > 50:
                    raise ValueError("Temperature out of range.")
                return temperature
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid temperature.")
    
    def get_weather(self, temperature):
        ''' Get weather based on temperature '''
        weather_mapping = {
            "toocold": lambda temp: temp < 0,
            "cold": lambda temp: 0 <= temp <= 19,
            "normal": lambda temp: 20 <= temp <= 25,
            "hot": lambda temp: 26 <= temp <= 35,
            "toohot": lambda temp: temp > 35
        }
        
        for weather, condition in weather_mapping.items():
            if condition(temperature):
                return weather
        return None
    
    def _liked(self, choosen, inp, func, type):
        ''' Check if user liked the item. '''
        if inp == "y":
            return choosen
        elif inp == "n":
            print("Let's try again.")
            return func(type)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            return self._liked(choosen, input("Do you like this item? (y/n): ").strip().lower(), func, type)
        
if __name__ == "__main__":
    clothing_ai = ClothingAI()
    clothing_ai.main()
    
    
    
''' I know this is not the best code, am just learning though.
 I had another ideas like there will be all the suggestions and user can select one or 
 show all together outfits and more but i am just refining my skills '''