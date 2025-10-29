# CarbonLite (super simple CO2 trip thing)

This is just a tiny program I made to see how much CO2 my trips make and what I'd save if I switched some of them to bus/bike/walk/train. It saves stuff into a CSV so I can look at it later.

## What it does
- I type how many miles a trip was and what I used (car, bus, bike, etc).
- It tells me the CO2 for that trip.
- Then I can pick a cleaner option and see how much I'd save each week if I switched 1–3 days.
- It logs everything to `logs/trips.csv`.

## How to run (Windows)
1. Install Python from https://www.python.org/downloads/  
   (when installing, check **Add Python to PATH**)
2. Go to your GitHub repo page → click **Code** → **Download ZIP**.
3. Right-click the ZIP → **Extract All…**
4. Open the new folder. Click the address bar at the top, type `powershell`, press **Enter**.
5. Run this:
   ```powershell
   python --version
