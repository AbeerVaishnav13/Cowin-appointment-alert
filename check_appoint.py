from time import sleep
import json
import requests

from pydub import AudioSegment
from pydub.playback import play

def main():
    day = input('Enter day: ')
    month = input('Enter month: ')
    time = int(input('Enter time interval for checking (min): '))

    f = open('./config.json',)
    config = json.load(f)
    pin = str(config['pin'])
    center_names = [s.lower() for s in config['center_names']]
    f.close()

    part1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pin + "&date="
    part2 = "-2021"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    cmds = [part1 + day + '-' + month + part2,
            part1 + str(int(day) + 1) + '-' + month + part2,
            part1 + str(int(day) + 2) + '-' + month + part2,
            part1 + str(int(day) + 3) + '-' + month + part2]

    song = AudioSegment.from_mp3('/Users/abeervaishnav/Documents/Coding/Python-programs/Cowin-alert/siren.mp3')

    open_centers = []

    print()
    print(f'Tracking update set to every {time}-minute(s).')
    while True:
        print(f'Checking... {day}, {int(day)+1}, {int(day)+2}, {int(day)+3}')
        open_centers = []
        for i in range(4):
            res = requests.get(cmds[i], headers=header)
            sessions = str(res.text)
            sessions_json = json.loads(sessions)

            for center in sessions_json['sessions']:
                for name in center_names:
                    if name in center['name'].lower():
                        open_centers.append([center['name'], int(day)+i, center['available_capacity'], center['min_age_limit']])

            if len(sessions_json['sessions']) > 0:
                print(f'\nAll available slots on {int(day)+i}/{month}')
                print('Center name : [Date] : [Doses] : (Age limit)')
                print('-----------------------------------------------------------------------')
                for center in sessions_json['sessions']:
                    print(f"{center['name']} : [{int(day)+i}/{month}] : [{center['available_capacity']} doses] : ({center['min_age_limit']}+)")

        print()

        if len(open_centers) > 0:
            print('\n\n\nSlots targetted by you:')
            print('Center name : [Date] : [Doses] : (Age limit)')
            print('-----------------------------------------------------------------------')
            for oc in open_centers:
                print(f'{oc[0]} : [{oc[1]}/{month}] : [{oc[2]} doses] : ({oc[3]}+)')

            print('\n\n\n')

            play(song)
            play(song)
            sleep(1.0)
            exit(0)

        sleep(time * 60.0)

if __name__ == "__main__":
    main()
