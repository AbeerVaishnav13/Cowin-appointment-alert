from time import sleep
import json
import requests

from pydub import AudioSegment
from pydub.playback import play

def main():
    pin = input('Enter PIN code: ')
    day = input('Enter day: ')
    month = input('Enter month: ')
    time = int(input('Enter time interval for checking (min): '))
    num_centers = int(input('Enter number of centers to be tacked: '))

    open_centers = []
    center_names = []
    print()
    print('For the following step, enter the name of the center or a part of the name:-')
    for i in range(num_centers):
        center_names.append(input(f'Enter center-{i+1}: ').lower())

    part1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pin + "&date="
    part2 = "-2021"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    cmds = [part1 + day + '-' + month + part2,
            part1 + str(int(day) + 1) + '-' + month + part2,
            part1 + str(int(day) + 2) + '-' + month + part2,
            part1 + str(int(day) + 3) + '-' + month + part2]

    song = AudioSegment.from_mp3('./siren.mp3')

    print()
    print(f'Tracking update set to every {time}-minute(s).')
    while True:
        print('Checking...')
        open_centers = []
        for i in range(4):
            res = requests.get(cmds[i], headers=header)
            sessions = str(res.text)
            sessions_json = json.loads(sessions)

            for center in sessions_json['sessions']:
                for name in center_names:
                    if name in center['name'].lower():
                        open_centers.append([center['name'], int(day)+i])

        if len(open_centers) > 0:
            print('\n\n\n')
            for oc in open_centers:
                print(f'{oc[0]} on {oc[1]}th : OPEN!!!!!!!!!')

            print('\n\n\n')

            play(song)
            play(song)
            play(song)
            sleep(1.0)
            exit(0)

        sleep(time * 60.0)

if __name__ == "__main__":
    main()
