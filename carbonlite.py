# CarbonLite - super simple trip CO2 calculator
# made by a high schooler, not NASA lol
# it logs your trips to logs/trips.csv and gives "what if I switch modes" weekly savings

import os
import csv
from datetime import datetime

# quick n dirty CO2 per mile (kg CO2e)
EMISSION_FACTORS = {
    "car_gas": 0.404,     # gas car
    "car_hybrid": 0.239,  # hybrid
    "car_ev": 0.122,      # electric car (US avg grid)
    "bus": 0.089,         # per passenger-mile
    "train": 0.041,       # per passenger-mile
    "bike": 0.0,
    "walk": 0.0,
}

MODES = [
    ("car_gas", "Gas car"),
    ("car_hybrid", "Hybrid"),
    ("car_ev", "Electric car"),
    ("bus", "Bus"),
    ("train", "Train"),
    ("bike", "Bike"),
    ("walk", "Walk"),
]

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "trips.csv")


def make_log():
    # make folder/file if they don't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "date", "miles", "mode", "emissions_kg"])


def pick_mode():
    print("\nTravel modes:")
    for i, (_, label) in enumerate(MODES, start=1):
        print(f"  {i}. {label}")
    while True:
        choice = input(f"Pick a number (1-{len(MODES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(MODES):
            idx = int(choice) - 1
            return MODES[idx][0], MODES[idx][1]
        print("Bad input. Try again.")


def calc_emissions(miles, mode_key):
    factor = EMISSION_FACTORS.get(mode_key, 0.0)
    return miles * factor


def add_trip():
    today = datetime.now().strftime("%Y-%m-%d")
    date = input(f"\nTrip date (press Enter for {today}): ").strip()
    if date == "":
        date = today

    while True:
        miles_txt = input("Miles (like 3.5): ").strip()
        try:
            miles = float(miles_txt)
            if miles <= 0:
                print("needs to be > 0")
                continue
            break
        except:
            print("not a number, try again")

    mode_key, mode_label = pick_mode()
    co2 = calc_emissions(miles, mode_key)
    print(f"\nEmissions for this trip: {co2:.3f} kg CO2e ({mode_label})")

    make_log()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([datetime.now().isoformat(timespec="seconds"), date, miles, mode_key, round(co2, 6)])
    print(f"Saved to {LOG_FILE}")

    # what-if savings (switching 1-3 days/week to another mode)
    print("\nWhat-if time: try switching this same trip some days each week to a cleaner mode.")
    alt_key, alt_label = pick_mode()
    if alt_key == mode_key:
        print("You picked the same mode, so 0 savings (obviously).")
        return

    while True:
        days_txt = input("Days per WEEK you'd switch (1-3): ").strip()
        if days_txt.isdigit() and 1 <= int(days_txt) <= 3:
            days = int(days_txt)
            break
        print("pick 1, 2, or 3")

    curr = calc_emissions(miles, mode_key)
    alt = calc_emissions(miles, alt_key)
    diff = max(curr - alt, 0.0)
    weekly = diff * days
    print(f"\nIf you switch {days} day(s)/week to {alt_label}, you save ~{weekly:.3f} kg CO2e per week.")
    print("Not perfect science, but you get the idea.\n")


def show_totals():
    make_log()
    trips = 0
    total = 0.0
    if not os.path.exists(LOG_FILE):
        print("\nNo trips yet.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            trips += 1
            total += float(row["emissions_kg"])
    print(f"\nTrips logged: {trips}")
    print(f"Total emissions: {total:.3f} kg CO2e (from all your trips in the CSV)\n")


def menu():
    print("\n=== CarbonLite (simple CO2 thing) ===")
    print("1) Add a trip")
    print("2) Show totals")
    print("3) Exit")
    return input("Choose 1-3: ").strip()


def main():
    make_log()
    while True:
        choice = menu()
        if choice == "1":
            add_trip()
        elif choice == "2":
            show_totals()
        elif choice == "3":
            print("bye")
            break
        else:
            print("bro pick 1, 2, or 3")


if __name__ == "__main__":
    main()
