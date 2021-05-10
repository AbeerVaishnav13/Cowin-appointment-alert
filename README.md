# Cowin Appointment Alert App
This is a simple python app for checking the CoWin server for available appointments according to the PIN code of your area and notifying available appointments by playing a loud siren when it is available.

# Dependencies & Installation
1. **PyDub**: This is a library to play the audio bundles with this app.
2. **Requests:** This library is essential to retrieve information about appointments from the CoWin server.
3. **Tabulate:** To pretty-print the schedules as an ascii-table.
```
$ pip install --upgrade pydub requests tabulate
```

# How to run?
1. Edit the `config.json` file and put your **PIN code** and the **Center names** (either full name or a unique part of the name) that you want to track.
2. Execute the python file `check_appoint.py` as shown below.
```
$ python3 check_appoint.py
```

# Input parameters
1. **Day and Month:** Enter the day and month for which you want to check the appointments.
**Disclaimer: The app automatically checks for appointments for upto 4 days from the date given by you.** <br>

2. **Time interval:** This is the time interval with which you want to check for available appointments.
<br>
<br>
<br>


Try the app out and get updates on the vaccinations easily! :)
