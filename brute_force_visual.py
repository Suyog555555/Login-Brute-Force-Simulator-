from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ✅ Credentials to test
username = "admin"
passwords = ["1234", "admin",  "password123"]  # Replace or load from wordlist

# ✅ Launch browser
driver = webdriver.Chrome()  # Requires ChromeDriver installed
driver.get("http://127.0.0.1:5000/")  # Make sure your Flask app is running

for pwd in passwords:
    time.sleep(1)  # Delay for visibility

    # Find input fields
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    # Clear fields
    username_input.clear()
    password_input.clear()

    # Enter values
    username_input.send_keys(username)
    password_input.send_keys(pwd)

    # Submit form
    password_input.send_keys(Keys.RETURN)

    # Optional: Print result message from page
    time.sleep(1)
    try:
        msg = driver.find_element(By.CLASS_NAME, "msg").text
        print(f"Trying '{pwd}' → {msg}")
    except:
        print(f"Trying '{pwd}' → No message")

    # Refresh for next attempt
    driver.get("http://127.0.0.1:5000/")

# ✅ Done
print("Finished brute force simulation.")
driver.quit()
