import mysql.connector
import random
from geopy import distance
import story
connection= mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database= 'time_travellers_quest',
    user='root',
    password= '12345',
    autocommit=True,
    collation = 'utf8mb4_unicode_ci'
   )

def fetch_airports ():
    sql= """ SELECT airport.name AS airport_name, country.name AS country_name, ident, type, latitude_deg, longitude_deg
    FROM airport, country 
    WHERE airport.iso_country = country.iso_country AND country.continent = "AS"
    AND type="large_airport"
     ORDER BY RAND() LIMIT 32;"""
    cursor= connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def fetch_targets():
    sql = f"SELECT * FROM target"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def create_player (p_name, start_money, start_range, start_time, current_airport,air_ports):
    sql = "INSERT INTO player (name,money,given_range,time,current_airport_id) VALUES (%s, %s, %s, %s, %s)"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql,(p_name,start_money,start_range,start_time, current_airport))
    play_id= cursor.lastrowid

    targets= fetch_targets()
    target_list=[]
    for target in targets:
        for i in range(0, target['probability'], 1):
            target_list.append(target['id'])

    airports_with_targets= air_ports[1:].copy()
    random.shuffle(airports_with_targets)

    for i, targ_id in enumerate(target_list):
        sql= "INSERT INTO target_location (target_id, player_id, location) VALUES (%s, %s, %s)"
        cursor= connection.cursor(dictionary=True)
        cursor.execute(sql,(targ_id, play_id,airports_with_targets[i]["ident"]))
    return play_id

def get_airport_by_icao(icao):
    sql= f"""SELECT airport.name AS airport_name, country.name AS country_name, ident, type, latitude_deg, longitude_deg
    FROM airport, country
    WHERE airport.iso_country = country.iso_country AND
    ident=%s"""
    cursor=connection.cursor(dictionary=True)
    cursor.execute(sql,(icao,))
    result=cursor.fetchone()
    return result

def check_target(pl_id, current_airport):
    sql = f"""SELECT target_location.id, target.id as target_id, name, value
    FROM target_location JOIN target ON target.id= target_location.target_id
    WHERE player_id= %s AND location= %s"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (player_id, current_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return result

def calculate_distance_by_coordinates(current_airport, target_airport):
    first = get_airport_by_icao(current_airport)
    second= get_airport_by_icao(target_airport)
    return distance.distance((first['latitude_deg'], first['longitude_deg']),( second['latitude_deg'], second['longitude_deg'])).km

def airports_in_domain(icao_code,air_ports,player_range):
    in_domain_airports=[]
    for air_port in air_ports:
        dist_ance= calculate_distance_by_coordinates(icao_code, air_port['ident'])
        if 0<dist_ance<=player_range:
            in_domain_airports.append(air_port)
    return in_domain_airports

def update_game(icao, player_range, player_money, pl_id):
    sql = f'''UPDATE player SET current_airport_id = %s, given_range = %s, money = %s WHERE id = %s'''
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao, player_range, player_money, pl_id))

def update_time(pla_id, airport_id):
    sql= "SELECT time FROM player WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql,(player_id,))
    result = cursor.fetchone()
    current_time = result['time']
    new_time= current_time -1
    sql_update_time= "UPDATE player SET time = %s WHERE id = %s"
    cursor.execute(sql_update_time,(new_time,player_id))
    return new_time

print("Welcome dear player to the realm of time traveller's quest! Are you ready to save the future?")
storyDialog= input("Would you like to have a guide about game flow? If yes then type yes: ")
if storyDialog == 'yes':
    for line in story.getStory():
        print(line)

print("When you would like to begin please type in the player name:")
player_name=input()

game_over= False
win_game= False

money= 3000
pl_range= 1500
time= 15

total_airports= fetch_airports()
begin_airport = total_airports[0]['ident']

present_airport= begin_airport
player_id= create_player(player_name,money,pl_range,time,begin_airport,total_airports)

while not game_over:
    airport= get_airport_by_icao(present_airport)
    print(f'''Dear time traveller, you are at {airport['airport_name']}, {airport['ident']}.''')
    print(f"You have Rs {money} amount of money, {pl_range} km of range, and {time} minutes.")
    print("Please note that you lose 1 minute for every airport you visit.")
    print("If you are ready then the floor is yours. Only you can change the history and save the world.")
    input("\033[95mPress ENTER to continue.\033[0m")

    time= update_time(player_id, present_airport)

    target= check_target(player_id, present_airport)
    if target:
        print(f"\033[31mYayy! You have found {target['name']} and it is worth Rs {target['value']}.\033[0m")
        q1= input("Do you want to redeem it for money (RS 200), range (100 km)? M= money and R=range.Press ENTER to skip.""")

        if not q1 == "":
            if q1 == "M":
                money = money - 200
            elif q1 == "R":
                pl_range = pl_range - 100
            if target['value'] > 0:
                money += target['value']
                print(f"\033[32mYour updated amount of money is {money} and range is {pl_range}.\033[0m")
            elif target['value'] == 0:
                win_game = True
                break
    input("\033[95mPress ENTER to continue.\033[0m")

    if money>0:
        print("Dear time traveller, if you want to buy fuel here is your chance to do so.")
        q2= input("\033[32mThe rate is Rs 1= 1km. Enter amount of money or press ENTER to skip \033[0m")
        if not q2 == "":
            q2= float(q2)
            while q2 > money:
                print(f"You are broke. You don't have enough amount of money to buy fuel.")
                q2 = float(input("\033[32mPlease enter valid amount of money or press ENTER to skip\033[0m"))
                if q2 == "":
                    break
            if q2<=money:
                pl_range= pl_range + q2
                money= money - q2
                print(f"\033[32mYour updated amount of money is {money} and range is {pl_range}.\033[0m")

    airports= airports_in_domain(present_airport,total_airports,pl_range)
    print(f"Time Traveller you have {len(airports)} in domain.")
    if len(airports)==0:
        print("Dang! You have no fuel available to visit any airport.")
        game_over= True
    else:
        print(f"Airports:")
        for airport in airports:
            airport_distance= calculate_distance_by_coordinates(present_airport,airport['ident'])
            print(f"Airport name:{airport['airport_name']}, ICAO code: {airport['ident']}, Distance: {airport_distance} ")
        travel= input("ENTER the ICAO code of the airport you want to travel to.")
        distance_travelled= calculate_distance_by_coordinates(present_airport,travel)
        pl_range= pl_range - distance_travelled

        update_game(distance_travelled, pl_range, money, player_id)
        present_airport = travel


if win_game:
    print("\033[95mCongrats! You have won the game.\033[0m")
    print("\033[34mYou found the event airport and successfully stopped the bomb blast.\033[0m")
    print("\033[34mYou have managed your resources well and achieved the target within given time.\033[0m")
    print("\033[34mYou are now being teleported to present to your original location through our Nexus Gate.\033[0m")
else:
    print("You have lost the game. You can still try again to save the world with a new gaming session.")