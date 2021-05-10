from time import sleep
import json
import requests
from tabulate import tabulate

from pydub import AudioSegment
from pydub.playback import play

def handle_input():
    day = input('Enter day: ')
    month = input('Enter month: ')
    time = int(input('Enter time interval for checking (min): '))
    num_days = int(input('Enter number of days to check after the entered day/month: '))

    if num_days > 4:
        print('[X] Error: Number of tracking days from day/month entered can only be upto 4 days.')
        exit(-1)

    return day, month, time, num_days

def load_config():
    f = open('./config.json',)
    config = json.load(f)
    pin = str(config['pin'])
    age = config['min_age_limit']

    if age not in [18, 45]:
        print('[X] Error: Minimum age limit can only be either 18 or 45 as per govt. rules.')
        exit(-1)

    center_names = [s.lower() for s in config['center_names']]
    f.close()
    return pin, age, center_names

def get_data(url, header, center_names, day, month, age, it):
    open_centers = []
    res = requests.get(url, headers=header)
    sessions = str(res.text)
    sessions_json = json.loads(sessions)

    for center in sessions_json['sessions']:
        for name in center_names:
            if name in center['name'].lower() and center['min_age_limit'] >= age:
                open_centers.append([center['name'],
                                     f'{int(day)+it}/{month}',
                                     center['available_capacity'],
                                     f"{center['min_age_limit']}+"])

    if len(sessions_json['sessions']) > 0:
        all_open_centers = []
        for center in sessions_json['sessions']:
            all_open_centers.append([center['name'],
                                     f'{int(day)+it}/{month}',
                                     center['available_capacity'],
                                     f"{center['min_age_limit']}+"])

        print(f'\nAll available slots on {int(day)+it}/{month}')
        print(tabulate(all_open_centers,
                       ['Center name', 'Date', 'Doses', 'Age limit'],
                       tablefmt='orgtbl'), '\n')

    return open_centers

def print_open_centers(open_centers, siren, month):
    print('\n\n\nSlots targetted by you:')
    print(tabulate(open_centers,
                   ['Center name', 'Date', 'Doses', 'Age limit'],
                   tablefmt='orgtbl'))
    print('\n\n\n')

    play(siren)
    play(siren)
    sleep(1.0)
    exit(0)

def main():
    day, month, time, num_days = handle_input()
    pin, age, center_names = load_config()
    siren = AudioSegment.from_mp3('./siren.mp3')
    open_centers = []

    part1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pin + "&date="
    part2 = "-2021"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    print(f'\nTracking update set to every {time}-minute(s).')
    try:
        while True:
            open_centers = []
            print(f'Checking... From {day}/{month} to {int(day)+num_days-1}/{month}')
            for i in range(num_days):
                url = part1 + str(int(day)+i) + '-' + month + part2
                open_centers += get_data(url, header, center_names, day, month, age, i)

            print()
            if len(open_centers) > 0:
                print_open_centers(open_centers, siren, month)
            sleep(time * 60.0)

    except KeyboardInterrupt:
        print('\nExiting...')
        exit(0)

if __name__ == "__main__":
    main()
