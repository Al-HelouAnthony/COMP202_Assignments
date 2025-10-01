import math
import random

#Constants
MIN_LAT = -90
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180
EARTH_RADIUS = 6378
STORM_STEPS = 5
EXIT_CHOICE = 3
SET_WAYPOINT = 1
MOVE_TO_WAYPOINT = 2
CHANCE_OF_STRIKE = 0.2
MAX_VICTORY_DISTANCE = 10
LOSS = 0

def degrees_to_radians(degrees):
    """
    (float) -> (float)
    Returns the angle in radians from an initial angle in degrees
    >>>degrees_to_radians(180)
    3.14
    >>>degrees_to_radians(30)
    0.52
    >>>degrees_to_radians(60)
    1.05
    """
    radians = degrees * math.pi / 180
    return round(radians, 2)


def get_valid_coordinate(val_name, min_float, max_float):
    """
    (str, float, float) -> (float)
    Returns the value of the float which is between the 2 floats inputed
    >>>get_valid_coordinate("latitude", -90, 90)
    What is your latitude ?80
    80
    >>>get_valid_coordinate("latitude", -100, 100)
    What is your latitude ?-120
    Invalid latitude
    What is your latitude ?95
    95
    >>>get_valid_coordinate("longitude", -200, 100)
    What is your longitude ?-180
    -180
    """
    coordinate = float(input("What is your " + val_name + " ?"))
    # Gets value strictly within the bounds
    while coordinate >= max_float or coordinate <= min_float :
        print("Invalid", val_name)
        coordinate = float(input("What is your " + val_name + " ?"))
    return coordinate


def get_gps_location():
    """
    Returns the values of the valid latitude and valid longitude
    
    Returns:
        (float, float): The valid values of latitude and longitude
    Examples:
    >>>get_gps_location()
    What is your latitude ?70
    What is your longitude ?100
    (70.0, 100.0)
    >>>get_gps_location()
    What is your latitude ?100
    Invalid latitude
    What is your latitude ?70
    What is your longitude ?200
    Invalid longitude
    What is your longitude ?100
    (70.0, 100.0)
    >>>get_gps_location()
    What is your latitude ?50
    What is your longitude ?120
    (50.0, 120.0)
    """
    valid_latitude = get_valid_coordinate("latitude", MIN_LAT, MAX_LAT)
    valid_longitude = get_valid_coordinate("longitude", MIN_LONG, MAX_LONG)
    return valid_latitude, valid_longitude

def distance_two_points(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    (float, float, float, float) -> (float)
    Returns the distance between the locations based on the Haversine formula
    >>>distance_two_points(5.508888, -73.561668, 19.432608, -99.133209)
    3723.31
    >>>distance_two_points(35, 120, 30, 100)
    1915.62
    >>>distance_two_points(70, 60, 10, 170)
    9744.23
    """
    new_lat_1 = degrees_to_radians(latitude_1)
    new_long_1 = degrees_to_radians(longitude_1)
    new_lat_2 = degrees_to_radians(latitude_2)
    new_long_2 = degrees_to_radians(longitude_2)
    
    #Computes Haversine formula
    a = (math.sin((new_lat_1 - new_lat_2) / 2)
    * math.sin((new_lat_1 - new_lat_2) / 2)
    + math.cos(new_lat_1) * math.cos(new_lat_2)
    * math.sin((new_long_1 - new_long_2) / 2)
    * math.sin((new_long_1 - new_long_2) / 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    d = EARTH_RADIUS * c
    return round(d, 2)


def get_random_number():
    """
    Returns random number from [-1,1)
    
    Returns:
        (float): Random value between -1 and 1
    Examples:
    >>>get_random_number()
    -0.5807541394342068
    >>>get_random_number()
    -0.05956431560052833
    >>>get_random_number()
    0.8049810743683241
    
    """
    #Converts random number range to [-1,1)
    return 2 * random.random() - 1 


def apply_wave_impact(position, min_float, max_float):
    """
    (float, float, float) -> (float)
    Returns the new position rounded to 2 decimals by adding the
    initial position to the random generated number
    >>>apply_wave_impact(0, -5, 5)
    -0.92
    >>>apply_wave_impact(1, -7, 7)
    0.65
    >>>apply_wave_impact(2, -10, 10)
    2.76
    """
    new_position = position + get_random_number()
    while new_position <= min_float or new_position >= max_float:
        #Gets a position strictly within the bounds
        new_position = position + get_random_number()
    return round(new_position, 2)


def wave_hit_vessel(vessel_lat, vessel_long):
    """
    (float, float) -> (float, float)
    Returns the new computed coordinates
    >>>wave_hit_vessel(20, -77.56)
    (20.31, -78.37)
    >>>wave_hit_vessel(60,120)
    (59.36, 120.73)
    >>>wave_hit_vessel(80,-100)
    (80.88, -100.08)
    """
    new_vessel_lat = apply_wave_impact(vessel_lat, MIN_LAT, MAX_LAT)
    new_vessel_long = apply_wave_impact(vessel_long, MIN_LONG, MAX_LONG)
    return new_vessel_lat, new_vessel_long

def check_boundaries(coordinate, min_float, max_float):
    """
    (float, float, float) -> (float)
    Returns position after being checked if it is between boundaries
    >>>check_boundaries(100, 20, 120)
    100
    >>>check_boundaries(100, 20, 90)
    90
    >>>check_boundaries(100, 110, 120)
    110
    """
    # Returns a value that isn't exceeding the bounds
    if coordinate < min_float:
        return min_float
    elif coordinate > max_float:
        return max_float
    else:
        return coordinate

def move_toward_waypoint(current_lat, current_long, wpt_lat, wpt_long):
    """
    (float, float, floaat, float) -> (float, float)
    Returns updated positions after checked if between boundaries
    >>>move_toward_waypoint(87, 110, 90, 140)
    (89.89, 138.9)
    >>>move_toward_waypoint(87, 110, 90, 140)
    (90, 178.99)
    >>>move_toward_waypoint(-10, -59, 0, -110)
    (-1.82, -100.74)
    """
    scale = random.random() + 1 # Generates random number from [1,2)
    new_lat = current_lat + (wpt_lat - current_lat)/scale
    new_lat = round(check_boundaries(new_lat, MIN_LAT, MAX_LAT), 2)
    new_long = current_long + (wpt_long - current_long)/scale
    new_long = round(check_boundaries(new_long, MIN_LONG, MAX_LONG), 2)
    return new_lat, new_long

def menu_display():
    """
    Displays the menu of the vessel
    
    Example:
    >>>menu_display()
    Please select an option below: 
    1) Set waypoint
    2) Move toward waypoint and Status report
    3) Exit boat menu
    """
    print("Please select an option below: ")
    print("1) Set waypoint")
    print("2) Move toward waypoint and Status report")
    print("3) Exit boat menu")
    

def vessel_menu():
    """
     Displays the vessel's menu and lets the user interact with it
     
     Its display different options that the user can choose from in order to
     acheive a specific task; reaching the desired waypoint. Using the
     functions earlier defined, it computes if the vessel arrives to the
     waypoint desired according to its initial position and evaluating the
     wave impact on the vessel as well as if the strom will hit the vessel.
     It displays in the end whether the vessel has succefully arrived or not.
     
     Parameters:
     None
     Returns:
     None
    """
    waypoint_set = False
    storm_count = STORM_STEPS
    victory = False
    
    print("Welcome to the boat menu!")
    crnt_lat, crnt_long = get_gps_location()
    
    menu_display()
    choice = int(input("Choose: ")) 
    
    while choice != EXIT_CHOICE and storm_count != LOSS and victory != True:
        #Repeats until one condition is met
        if choice == SET_WAYPOINT:
            #If user chooses 1, it asks him for waypoint coordinates
            print("Enter waypoint coordinates.")
            wpt_lat, wpt_long = get_gps_location()
            print("Waypoint set to latitude of",wpt_lat,"and "\
            "longitude of",wpt_long)
            waypoint_set = True
            menu_display()
            choice = int(input("Choose: "))
        
        elif choice == MOVE_TO_WAYPOINT:
            #If user chooses 2, it moves the vessel towards
            #waypoint
            if waypoint_set:
                crnt_lat, crnt_long = move_toward_waypoint(crnt_lat,
                                                         crnt_long,
                                                         wpt_lat, wpt_long)
                print("Captain Log: Journeyed towards waypoint.")
                
                if random.random() < CHANCE_OF_STRIKE:
                    #Vessel is hit by wave at a 20% chance
                    crnt_lat, crnt_long = wave_hit_vessel(crnt_lat, crnt_long)
                    print("Captain Log: Wave impact recorded")
                
                print("Current position is latitude of ", crnt_lat,"and "\
                      "longitude of ", crnt_long)
                distance = distance_two_points(crnt_lat, crnt_long,
                                               wpt_lat, wpt_long)
                print("Distance to waypoint:", distance, "km" )
                
                if distance > MAX_VICTORY_DISTANCE:
                    storm_count -= 1
                    print("T-minus: ", storm_count)
                    
                    if storm_count == 0:
                        print("Mission failed: storm hit before arrival." )
                
                else:
                    print("Mission success: waypoint reached before storm.")
                    victory = True
                
                if storm_count > 0 and victory == False:
                    #if mission still not over, display menu
                    menu_display()
                    choice = int(input("Choose: "))
            
            else:
                print("No waypoint set.")
                menu_display()
                choice = int(input("Choose: "))
    
    if choice == EXIT_CHOICE: 
        print("Console closed by captain.")
