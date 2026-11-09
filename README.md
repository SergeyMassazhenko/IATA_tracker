# IATA Airport Route Distance Tracker

A modern, lightweight desktop application built with Python to analyze routes and calculate distances between airports worldwide using 3-letter IATA codes. 

## Key Features
* **Modern Windows 10 Native UI:** Styled using `CustomTkinter` with a clean, calm blue/gray aesthetics.
* **Offline Architecture:** Uses a local dictionary-based global database (`airports.json`), ensuring instantaneous execution and zero external network dependencies.
* **High Efficiency:** Low CPU and memory footprint, running on an event-driven loop that stays idle until execution is requested.
* **Robust Error Handling:** Validates IATA inputs and captures potential filesystem and analytical runtime exceptions gracefully without freezing the UI thread.

## Under the Hood
* **Language & Framework:** Python 3 (compatible with modern interpreters like 3.11+).
* **GUI Engine:** `CustomTkinter` (an elegant wrapper for standard Tkinter widgets).
* **Mathematical Core:** Implements the **Haversine Formula** to resolve great-circle distances between two geographic points on a spherical surface.

## How to Run Locally
1. Clone this repository or download the source files.
2. Ensure you have the `airports.json` database file placed in the root directory.
3. Install dependencies via your terminal or IDE package manager:
   ```bash
   pip install customtkinter requests
   ```
4. Run the main script:
   ```bash
   python IATA_tracker.py
   ```

## Future Roadmap (Next Steps)
- [ ] Add interactive dropdown lists (Comboboxes) sorted by countries to ease airport selection.
- [ ] Integrate a currency converter and fintech module based on ISO country codes.
- [ ] Implement flight time estimation based on aircraft cruise speed profiles.