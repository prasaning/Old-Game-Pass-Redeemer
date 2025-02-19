# Game Pass Redeemer  

## Overview
This script was made for minecraft alt shops. It was one of the first redeemers made for xbox game passes redeeming.  
It uses playwright so it wasn't really that efficient in the long run. The code it's self is decent for the time.  
Since people were used to using cookies, I made it so the code also saved the cookie of the account.  
This was also a good way to bypass the account locks since the session id was still active while the acc was locked.

## Features
- Automated Xbox/Minecraft account creation.
- Code redemption from `info/codes.txt`.
- Fake user data generation (name, address, payment details).
- Parallel processing using threading.
- Saves account credentials and session cookies.

## Requirements
### Dependencies
Ensure you have the following installed:
- Python 3.x
- Playwright
- Faker

Install dependencies with:
```bash
pip install playwright faker
playwright install
```

### Files Needed
Ensure the following files are present:
- `info/codes.txt` – List of Xbox/Minecraft codes.
- `info/first_names.txt` & `info/last_names.txt` – Name databases.
- `info/addresses.txt` – Fake addresses.
- `info/cc.txt` – Fake credit card details.

## Usage
### Running the Script
```bash
python script.py
```
The script will:
1. Launch a browser.
2. Navigate to Xbox’s redeem page.
3. Generate and input fake user details.
4. Redeem a code and attempt to bypass payment.
5. Save the created account credentials.

### Output
- Created accounts will be stored in `accounts/`.
- User credentials saved in `accounts/{username}/{username}_USER_PASS.txt`.
- Session cookies saved for reuse.

## Disclaimer
**This script is for educational purposes only.** Unauthorized account creation and code redemption violate Microsoft’s Terms of Service and may lead to legal consequences. Use responsibly.

