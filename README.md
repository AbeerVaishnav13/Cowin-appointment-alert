# Cowin Appointment Alert App
This is a simple python app for checking the CoWin server for available appointments according to the PIN code of your area and notifying available appointments by playing a loud siren when it is available.

# Dependencies & Installation
1. **PyDub**: This is a library to play the audio bundles with this app.
```
$ pip install --upgrade pydub
```

2. **Requests:** This library is essential to retrieve information about appointments from the CoWin server.
```
$ pip install --upgrade requests
```

# How to run?
```
$ python3 check_appoint.py
```

# Input parameters
1. **PIN code:** Enter the PIN-code/ZIP-code of your area.
2. **Day and Month:** Enter the day and month for which you want to check the appointments.
```
Disclaimer: The app automatically checks for appointments for upto 4 days from the date given by you.
```
3. **Time interval:** This is the time interval with which you cant to check for available appointments.
4. **Centers to track:** This is a list of centers that you cant to keep track for. Just enter the full name of the centers or a part of their name.



Try the app out and get updates on the vaccinations easily! :)
