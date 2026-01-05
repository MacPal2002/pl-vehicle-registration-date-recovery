`Forked from: IgorWalkowiak/historia-pojazdu`

# 🚗 PL Vehicle History - First Registration Date Recovery

#### Automated tool to find the missing **First Registration Date** required by the official [Gov.pl - Sprawdź historię pojazdu](https://www.gov.pl/web/gov/sprawdz-historie-pojazdu) service.

---
### System Requirements

Before you start, make sure you have the following installed on your computer:
* **Python 3.10** or newer.
* Stable internet connection.

If you don't have Python, download it from [python.org](https://www.python.org/downloads/). During installation on Windows, make sure to check the **"Add Python to PATH"** option.

### Prerequisites

To use the program, prepare:
- **Registration number**
- **VIN** (17 characters)
- **Year or years** you want to check (e.g., `2026` or `2025, 2026`)

### How to run step-by-step

Open your terminal and follow these steps:

   ```bash
   git clone https://github.com/MacPal2002/pl-vehicle-registration-date-recovery.git
   cd historia-pojazdu

   python3 -m venv .venv
   
   # Activate virtual environment:
   source .venv/bin/activate # Linux/MacOS
   source .venv\Scripts\activate    # Windows

   python3 -m pip install -r requirements.txt

   python3 src/main.py
   ```


### Disclaimer
The program uses publicly available information. The data you enter is used solely for a one-time check. This program was created for educational purposes.
