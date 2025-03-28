from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

driver = None
options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
driver_path = "C:/chromedriver-win64/chromedriver.exe"
options.add_argument(r"--user-data-dir=C:\Users\zoraw\AppData\Local\BraveSoftware\Brave-Browser\User Data")
options.add_argument(r"--profile-directory=Default")

def init_driver():
    global driver
    if driver is None or driver.session_id is None or len(driver.window_handles) == 0:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    # elif len(driver.window_handles) == 0:
    #     driver.quit()
    #     driver = webdriver.Chrome(service=service, options=options)

def open_youtube():
    check_window()
    print("opening youtube")
    try:
        init_driver()
        driver.get("https://www.youtube.com")
    except Exception as e:
        print(f"Error opening YouTube: {e}")

def play_pause_video():
    check_window()
    try:
        init_driver()
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.SPACE)  # YouTube shortcut for play/pause
    except Exception as e:
        print(f"Error controlling video: {e}")

def check_window():
    global driver
    print("checking open drvers")
    try:
        # Check if the current window is still open
        if driver and len(driver.window_handles) == 0:
            driver.quit()  # Close the driver if no windows are open
            driver = None
            # app.quit()  # Close the PyQt app
    except Exception as e:
        # print(f"Error checking window: {e}")
        driver.quit()  # Close the driver if no windows are open
        driver = None