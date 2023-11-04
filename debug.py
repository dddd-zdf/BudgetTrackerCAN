from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import *
import sqlite3

driver = webdriver.Chrome()

# Navigate to the login page
driver.get('https://global.americanexpress.com/myca/intl/istatement/canlac/statement.do?Face=en_CA&method=displayStatement&account_key=3CEF27AED122159731EE13220E647C1F&BPIndex=0#/')



username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'eliloUserID'))
)

password_input = driver.find_element(By.ID, 'eliloPassword')
login_button = driver.find_element(By.ID, 'loginSubmit')
credentials = credentials('amex')

print(credentials)

# Input your username and password
username_input.send_keys(credentials['Username'])
password_input.send_keys(credentials['Password'])


# Click the login button
login_button.click()

# Wait for the next page to load (you may need to customize this)
# You can use WebDriverWait or time.sleep for this purpose
username_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'eliloUserID'))
)

# Get the page source after login
table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="transaction-table"]/tbody'))
)

transactions = table.find_elements(By.TAG_NAME, "tr")


conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()
cursor.execute(
'''
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        date DATE,
        cent INTEGER,
        description TEXT,
        account INTEGER
    )
''')

cursor.execute("SELECT MAX(id) FROM transactions")
last_id = cursor.fetchone()[0]

print(last_id)


account = 1

for transaction in transactions:
    id = transaction.get_attribute("id")
    if id <= last_id:
        continue
    date = id[-8:]
    date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    description = transaction.find_element(By.CLASS_NAME, "description").text
    amount_str = transaction.find_element(By.CLASS_NAME, "amount").text
    cent = int(float(amount_str.replace('$', '').strip())*100)
    cursor.execute("INSERT INTO transactions (id, date, cent, description, account) VALUES (?, ?, ?, ?, ?)", (id, date, cent, description, account))

conn.commit()
conn.close()
driver.quit()
