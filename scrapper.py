from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pandas as pd

def construct_url(date, time, longitude, latitude):
    return f"https://earth.nullschool.net/#{date}/{time}Z/wind/surface/level/grid=on/equirectangular=-225.00,0.00,180/loc={longitude},{latitude}"

def get_wind_speed_and_direction(driver, url):
    driver.get(url)
    try:
        wind_speed_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='spotlight-panel']/div[2]/div"))
        )
        aria_label = wind_speed_element.get_attribute('aria-label')
        print("Captured text:", aria_label) 

        if 'km/h' in aria_label:
            parts = aria_label.split('@')
            if len(parts) > 1:
                direction = parts[0].strip().rstrip('°') 
                speed = parts[1].strip().split()[0]    
                return direction, speed
        return None, None 
    except Exception as e:
        print(f"Error while trying to get wind speed and direction: {str(e)}")
        return None, None

def main():
    driver = webdriver.Chrome()
    data_csv = pd.read_csv('/Users/rafiandrianto/Desktop/DataScience/data/Modified_DateLongLat.csv')
    all_data = []

    for index, row in data_csv.iterrows():
        #format the date from MM/DD/YYYY to YYYY/MM/DD
        date = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').strftime('%Y/%m/%d')
        latitude = row['Latitude']
        longitude = row['Longitude']
        
        #specify time
        time = "0300"
        time_obj = datetime.datetime.strptime(time, "%H%M") + datetime.timedelta(hours=9)
        formatted_time = time_obj.strftime("%H:%M")  #format as HH:MM

        url = construct_url(date, time, longitude, latitude)
        direction, speed = get_wind_speed_and_direction(driver, url)
        all_data.append({
            "Date": date,
            "Time": formatted_time,
            "Latitude": latitude,
            "Longitude": longitude,
            "Wind Direction": direction,
            "Wind Speed (km/h)": speed
        })

    driver.quit()

    #convert to DataFrame and save to CSV
    try:
        df = pd.DataFrame(all_data)
        df.to_csv('/Users/rafiandrianto/Desktop/DataScience/data/ScrapedWind.csv', index=False)
        print("Data successfully written to CSV.")
    except Exception as e:
        print(f"Error writing data to CSV: {str(e)}")

if __name__ == "__main__":
    main()


