import threading
from playwright.sync_api import sync_playwright
import time
import random
import faker
import re
import os

def driver_click(page, selector, timeout=600):
    try:
        element1 = f"{selector}"
        print(f"Clicking: {element1}")
        page.locator(selector).click(timeout=timeout * 1000)
        print(f"Finished Clicking: {element1}")
    except Exception as e:
        print(f"An error occurred: {e}")

def driver_type(page, selector, text, timeout=600):
    try:
        element1 = f"{selector}"
        print(f"Typing: {element1} | {text}")
        page.locator(selector).fill(text, timeout=timeout * 1000)
        print(f"Finished Typing: {element1} | {text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def driver_select(page, selector, option, timeout=600):
    try:
        element1 = f"{selector}"
        print(f"Selecting: {element1} | {option}")
        page.locator(selector).select_option(value=option, timeout=timeout * 1000)
        print(f"Finished Selecting: {element1} | {option}")
    except Exception as e:
        print(f"An error occurred: {e}")

def wait_until_element_gone(page, selector, timeout=600):
    page.locator(selector).wait_for(state='hidden', timeout=timeout * 1000)

def read_line_from_file(filename):
    with open(filename, 'r') as file:
        line = [line.strip() for line in file if line.strip()]
    return line

def generate_random_name():
    first_names = read_line_from_file('info/first_names.txt')
    last_names = read_line_from_file('info/last_names.txt')
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

def get_random_address():
    def parse_address(line1, line2):
        pattern = re.compile(r'^(.*), ([A-Z]{2}) (\d{5})$')
        match = pattern.match(line2.strip())
        if match:
            city, state, zipcode = match.groups()
            return {
                'street': line1.strip(),
                'city': city.strip(),
                'state': state.strip(),
                'zipcode': zipcode.strip()
            }
        return None

    with open('info/addresses.txt', 'r') as file:
        lines = file.readlines()

    parsed_addresses = []
    for i in range(0, len(lines), 2):
        line1 = lines[i].strip()
        if i+1 < len(lines):
            line2 = lines[i+1].strip()
            parsed_address = parse_address(line1, line2)
            if parsed_address:
                parsed_addresses.append(parsed_address)

    if parsed_addresses:
        random_address = random.choice(parsed_addresses)
        return random_address['state'], random_address['city'], random_address['zipcode']
    else:
        return None, None, None

def get_cc_info():
    fake = faker.Faker('en_US')

    card = random.choice(read_line_from_file('info/cc.txt')).split('|')
    
    card_number = card[0]
    card_expire_month = card[1]
    if card_expire_month.startswith('0'):
        card_expire_month = card_expire_month[1:]
    card_expire_year = card[2]
    cvv = card[3]
    
    state, city, zipcode = get_random_address()

    address_line_2 = ""
    first_name, last_name = generate_random_name()
    name = f"{first_name} {last_name}"
    address = fake.street_address()

    if " Apt." in address:
        address_line_2 = address.split(" Apt.")[1]
        address = address.split(" Apt.")[0]
        address_line_2 = f"Apt.{address_line_2}"
    if " Suite" in address:
        address_line_2 = address.split(" Suite")[1]
        address = address.split(" Suite")[0]
        address_line_2 = f"Suite{address_line_2}"
    return card_number, card_expire_month, card_expire_year, cvv, name, address, address_line_2, city, state, zipcode

def create_account(code):
    fake = faker.Faker('en_US')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            viewport={'width': random.randint(700, 1000), 'height': random.randint(700, 1000)}  # Change these values to set the desired aspect ratio
        )
        page = context.new_page()

        first_name, last_name = generate_random_name()
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 27)
        birth_year = random.randint(1980, 2001)
        try:
            # emailname = input("Email: ")
            # password = input("Password: ")
            page.goto(f'https://www.xbox.com/en-US/xbox-game-pass/invite-your-friends/redeem?offerId={code}')
            driver_click(page, '#mectrl_headerPicture')
            salt = random.randint(100000000, 9999999999)

            
            driver_click(page, '#signup')
            driver_click(page, '#liveSwitch')
            salt = random.randint(1000, 9999)
            emailname = f"{first_name}{last_name}{salt}"
            driver_type(page, '#usernameInput', f"{emailname}")
            driver_click(page, '#nextButton')
            password = f"{last_name}{salt}"
            driver_type(page, '#Password', f"{password}")
            driver_click(page, '#nextButton')
            driver_type(page, '#firstNameInput', f"{first_name}")
            driver_type(page, '#lastNameInput', f"{last_name}")
            driver_click(page, '#nextButton')
            page.get_by_test_id("BirthMonth").select_option(f"{birth_month}")
            page.get_by_test_id("BirthDay").select_option(f"{birth_day}")
            driver_type(page, '#BirthYear', f"{birth_year}")
            driver_click(page, '#nextButton')

            # driver_type(page, '#i0116', f"{emailname}")
            # driver_click(page, '#idSIButton9')
            # driver_type(page, '#i0118', f"{password}")
            # driver_click(page, '#idSIButton9')


            not_complete = True
            while not_complete:
                first_word = fake.word().capitalize()
                second_word = fake.word().capitalize()
                username = f"{first_word}{second_word}{salt}"
                if len(username) < 20:
                    not_complete = False
            time.sleep(0.5)
            driver_type(page, '#create-account-gamertag-input', f"{username}")

            time.sleep(2)
            page.wait_for_selector('#inline-continue-control')
            page.locator('#inline-continue-control').click()

            wait_until_element_gone(page, '#create-account-gamertag-suggestion-1')
            time.sleep(1)
            page.get_by_role("button", name="Yes").click()
            driver_click(page, '#inline-continue-control')
            wait_until_element_gone(page, '#inline-continue-control')
            time.sleep(1)
            driver_click(page, '//button[contains(@class, "c-button f-primary") and text()="REDEEM NOW"]')

            iframe = page.frame(name="redeem-sdk-hosted-iframe")
            
            not_complete = True
            # bruhthisisshit = 0
            
            while not_complete:
                print("Debug 2")
                time.sleep(3)

                page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_role("button", name="Get Started! Add a way to pay.").click()
                driver_click(iframe, '#displayId_credit_card_visa_amex_mc_discover')
                
                card_number, card_expire_month, card_expire_year, cvv, name, address, address_line_2, city, state, zipcode = get_cc_info()

                driver_type(iframe, '#accountToken', f"{card_number}")
                driver_type(iframe, '#accountHolderName', f"{name}")
                driver_select(iframe, '#input_expiryMonth', card_expire_month)
                driver_select(iframe, '#input_expiryYear', card_expire_year)
                driver_type(iframe, '#cvvToken', f"{cvv}")
                driver_type(iframe, '#address_line1', f"{address}")
                if address_line_2 != "":
                    driver_type(iframe, '#address_line2', f"{address_line_2}")
                page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_label("City*").fill(f"{city}")
                page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_label("State*").select_option(f"{state.lower()}")
                page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_placeholder("20001").fill(f"{zipcode}")
                page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_label("Save").click()
                time.sleep(10)

                elements = page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").locator("#pidlddc-error-accountToken")
                if elements.count() > 0:
                    print("Debug 3")
                    driver_click(iframe, '#pidlddc-button-cancelButton')
                else:
                    print("Debug 4")
                    not_complete = False

            page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_role("button", name="Add profile address").click()
            driver_type(iframe, '#address_line1', f"{address}")
            driver_type(iframe, '#city', f"{city}")
            page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").locator("#input_region").select_option(f"{state.lower()}")
            driver_type(iframe, '#postal_code', f"{zipcode}")
            page.frame_locator("iframe[name=\"redeem-sdk-hosted-iframe\"]").get_by_label("Save").click()
            driver_click(iframe, '#pidlddc-button-addressUseButton')
            time.sleep(3)
            driver_click(iframe, 'button.primary--kLopxQTl.base--goua8jma[data-bi-dnt="true"]')

            time.sleep(20)

            page.goto(f'https://www.minecraft.net/en-us/login')
            driver_click(page, 'a.btn.btn-primary.btn-block.signin-msa-button.flex-wrap[data-testid="MSALoginButtonLink"]')
            time.sleep(10)
            page.goto(f'https://www.minecraft.net/en-us/msaprofile/redeem?setupProfile=true')
            driver_type(page, '#change-java-profile-name', f"{username}")
            driver_click(page, 'button.MC_Button.MC_Button_Hero.MC_Style_Green_5.redeem__text-transform[data-aem-contentname="Set Profile Name"]')
            time.sleep(2)

        except Exception as e:
            print(f"bruh wtf why crash thats so racist: {e}")
        finally:
            cookies = page.context.cookies()
            os.makedirs(f'accounts/{username}', exist_ok=True)
            with open(f'accounts/{username}/{username}.txt', 'w') as file:
                for cookie in cookies:
                    domain = cookie['domain']
                    is_secure = 'TRUE' if cookie['secure'] else 'FALSE'
                    path = cookie['path']
                    is_http_only = 'FALSE'
                    expiration = str(cookie['expires']) if 'expires' in cookie else '0'
                    name = cookie['name']   
                    value = cookie['value']
                    file.write(f"{domain}\t{is_secure}\t{path}\t{is_http_only}\t{expiration}\t{name}\t{value}\n")
            with open(f'accounts/{username}/{username}_USER_PASS.txt', 'w') as file:
                file.write(f"{emailname}@outlook.com:{password}\n")
            context.close()

with open('info/codes.txt', 'r') as file:
    codes = [line.strip() for line in file if line.strip()]

threads = []
for code in codes:
    thread = threading.Thread(target=create_account, args=(code,))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("All tasks completed.")