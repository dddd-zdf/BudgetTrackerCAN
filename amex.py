# amex.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from credentials import get_credentials



def login(driver, url, username, password):
    # Use the credentials for American Express
    driver.get(url)
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'eliloUserID'))
    )
    password_input = driver.find_element(By.ID, 'eliloPassword')
    login_button = driver.find_element(By.ID, 'loginSubmit')

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

def switch_card(driver, card):
    # Logic to switch to the card using a specific element (XPath in this case)
    # Click on the element that corresponds to 'amex cobalt' card
    if card == 'amex gold':
        return
    else:
        card_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div[3]/card-selector/div/div[1]/div[2]/div[2]/div/div[2]')
        )
    )
        card_element.click()
        
        #wait until the table is updated after switching card by checking the id of the first transaction
        def has_id_changed(driver, initial_id, xpath):
            try:
                current_id = driver.find_element(By.XPATH, xpath).get_attribute("id")
                return current_id != initial_id
            except Exception as e:
                # If there's an error finding the element, we can assume the page might be updating
                return False

        # Define the XPath for the first <tr> element and get its initial ID
        first_tr_xpath = "//*[@id='transaction-table']/tbody/tr[1]"
        initial_tr_id = driver.find_element(By.XPATH, first_tr_xpath).get_attribute("id")
        
        # Wait until the ID of the first <tr> element changes
        WebDriverWait(driver, 10).until(
            lambda d: has_id_changed(d, initial_tr_id, first_tr_xpath)
        )


def get_last_transaction_id(cursor):
    cursor.execute("SELECT MAX(id) FROM transactions")
    return cursor.fetchone()[0]

def insert_transaction(cursor, transaction_data):
    cursor.execute("INSERT INTO transactions (id, date, cent, description, account) VALUES (?, ?, ?, ?, ?)", transaction_data)

def retrieve_transactions(driver, card, cursor, conn):
    # Switch to the specific card
    switch_card(driver, card)

    cursor.execute("SELECT MAX(id) FROM transactions WHERE card = ?", (card,))
    last_id = cursor.fetchone()[0]
    if last_id is None:
        last_id = '0'  # Set to '0' if there are no entries yet



    # Wait for the transactions to be visible and scrape them
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="transaction-table"]/tbody'))
    )
    transactions = table.find_elements(By.TAG_NAME, "tr")

    # Process each transaction
    for transaction in transactions:
        id = transaction.get_attribute("id")
        # Skip already recorded transactions
        if id == last_id:
            break
        # Extract the data from each transaction
        date = id[-8:]
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        description = transaction.find_element(By.CLASS_NAME, "description").text
        amount_str = transaction.find_element(By.CLASS_NAME, "amount").text
        cent = int(float(amount_str.replace('$', '').replace(',', '').strip()) * 100)
        
        # Insert the transaction into the database
        try:
            cursor.execute("INSERT INTO transactions (id, date, cent, description, card) VALUES (?, ?, ?, ?, ?)",
                           (id, date, cent, description, card))  # card used as the account identifier
            print("inserted " + id, date, cent, description, card)
        except sqlite3.IntegrityError:
            # This will skip the insert if the transaction id is already in the database
            continue

    # Commit changes
    conn.commit()

def setup_database():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date DATE,
            cent INTEGER,
            description TEXT,
            card TEXT
        )
        '''
    )
    conn.commit()
    return conn

if __name__ == "__main__":
    import yaml
    driver = webdriver.Chrome()
    conn = setup_database()
    cursor = conn.cursor()
    with open('configs.yaml', 'r') as config_file:
        configs = yaml.safe_load(config_file)
    username, password = get_credentials('amex')
    url = configs['amex']['url']

    try:

        login(driver, url, username, password)
        retrieve_transactions(driver, 'amex gold', cursor, conn)
        retrieve_transactions(driver, 'amex cobalt', cursor, conn)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        driver.quit()
