import random
import pandas as pd
import pyodbc
import sqlalchemy as sa

class Driver:
    def __init__(self, name, skill):
        """
        Initialize a Driver object with a name and skill level.
        """
        self.name = name
        self.skill = skill

class Car:
    def __init__(self, name, performance):
        """
        Initialize a Car object with a name and performance level.
        """
        self.name = name
        self.performance = performance
        self.tyre_condition = 100
        self.fuel_level = 100
        self.consumption_rate = random.randint(1, 3)

class Race:
    def __init__(self, race_number, track_length, laps):
        """
        Initializes a Race object with a race number, track length, and number of laps.
        """
        self.track_length = track_length
        self.laps = laps
        self.weather = "Sunny"
        self.track_condition = "Dry"
        self.drivers = []
        self.results = []
        self.race_number = race_number

    def add_driver(self, driver, car):
        """
        Adds a driver and their car to the race.
        """
        self.drivers.append((driver, car))

    def simulate_race(self):
        """
        Simulates the race, calculating lap times and populating results.
        """
        for lap in range(1, self.laps + 1):
            print(f"Lap {lap}/{self.laps}")
            for driver, car in self.drivers:
                lap_time = self.calculate_lap_time(car)
                print(f"{driver.name}: Lap time - {lap_time:.2f} seconds")
            print("")
        
        # After the race simulation, populate self.results with the finishing order
        sorted_drivers = sorted(self.drivers, key=lambda x: self.calculate_race_time(x[1]))
        for driver, _ in sorted_drivers:
            self.results.append(driver.name)
        
        race_results_data = []
        winner = self.results[0]
        for driver, car in self.drivers:
            race_result = {
                'RaceNumber': self.race_number,
                'DriverName': driver.name,
                'Car': car.name, # Use the class name of the car object
                'Winner': winner
            }
            race_results_data.append(race_result)
        
        # Convert race results data to Pandas DataFrame
        race_results_df = pd.DataFrame(race_results_data)

        # Create SQLAlchemy engine using pyodbc connection string
        engine = sa.create_engine('mssql+pyodbc://DESKTOP-Q10B922\SQLEXPRESS/Formula1Simulator?driver=ODBC+Driver+17+for+SQL+Server')

        # Write DataFrame to SQL Server table using SQLAlchemy engine
        race_results_df.to_sql('RaceResults', con=engine, if_exists='append', index=False)

    def calculate_lap_time(self, car):
        """
        Calculates the lap time for a given car.
        """
        skill_factor = random.uniform(0.9, 1.1)
        performance_factor = random.uniform(0.9, 1.1)
        if self.weather == "Rainy":
            weather_factor = 1.2
        else:
            weather_factor = 1.0
        tyre_factor = car.tyre_condition / 100
        fuel_factor = car.fuel_level / 100
        total_factor = skill_factor * performance_factor * weather_factor * tyre_factor * fuel_factor
        lap_time = (self.track_length / (car.performance * total_factor))
        car.fuel_level -= car.consumption_rate
        return lap_time

    def calculate_race_time(self, car):
        """
        Calculates the total race time for a given car.
        """
        total_race_time = 0
        for lap in range(1, self.laps + 1):
            total_race_time += self.calculate_lap_time(car)
        return total_race_time

# Example usage:
if __name__ == "__main__":
    #Simultates a race between drivers for a random amount of times
    
    for i in range(1,random.randint(1, 3)):
        print(f"Race: {i}")
        lewis = Driver("Lewis Hamilton", random.uniform(.85, .99))
        max = Driver("Max Verstappen", random.uniform(.85, .99))

        mercedes = Car("Mercedes", 1.1)
        red_bull = Car("Red Bull", 1.08)

        race = Race(track_length=5.8, race_number = i, laps=random.randint(5,20))
        race.add_driver(lewis, mercedes)
        race.add_driver(max, red_bull)

        race.simulate_race()
        
        print("Race Results:")
        for i, driver in enumerate(race.results, 1):
            print(f"{i}. {driver}")
   