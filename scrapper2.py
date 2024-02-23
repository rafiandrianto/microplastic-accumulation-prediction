from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import time

# def extract_and_parse_data(url, date, lat, lon):
#     driver.get(url)
#     try:
#         data_element = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div')
#         data = data_element.get_attribute('aria-label')
#         if "m/s" in data and " @ " in data:
#             direction, speed = data.split(" @ ")
#             direction = direction.replace("°", "")
#             speed = speed.strip(" m/s")
#             return [date, lat, lon, direction, speed]
#         else:
#             return None
#     except NoSuchElementException:
#         return None

# driver = webdriver.Chrome()

# input_file_path = '/Users/rafiandrianto/Desktop/DataScience/data/Modified_DateLongLat.csv'
# output_file_path = '/Users/rafiandrianto/Desktop/DataScience/data/ScrapedOceanCurrent.csv'

# with open(input_file_path, mode='r', newline='') as infile:
#     reader = csv.DictReader(infile)
#     with open(output_file_path, mode='w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(['Date', 'Latitude', 'Longitude', 'Ocean Current Direction', 'Ocean Current Speed (m/s)'])

#         for row in reader:
#             if '/' in row['Date'] and len(row['Date'].split('/')) == 3:
#                 month, day, year = row['Date'].split('/')
#                 formatted_date = f"{year}/{month}/{day}/"
#                 full_date = formatted_date + "0300Z"
#                 date = "/".join(full_date.split("/")[0:3])

#                 data_row = None
#                 for i in range(-9, 8):
#                     if data_row:
#                         break
#                     for j in range(-9, 8):
#                         lat = float(row['Latitude']) + (i * 0.1)
#                         lon = float(row['Longitude']) + (j * 0.1)
#                         coordinates = f"loc={lon},{lat}"
#                         url = f"https://earth.nullschool.net/#{full_date}/ocean/surface/currents/orthographic=-218.21,27.84,420/{coordinates}"
#                         data_row = extract_and_parse_data(url, date, lat, lon)
#                         if data_row:
#                             writer.writerow(data_row)
#                             break
#                 if not data_row:
#                     writer.writerow([date, row['Latitude'], row['Longitude'], 'None', 'None'])
#                     print(f"No data found after iterations for {date}, {row['Latitude']}, {row['Longitude']}.")

# driver.quit()

def extract_and_parse_data(url, date, lat, lon):
    driver.get(url)
    time.sleep(2)  
    try:
        data_element = driver.find_element(By.XPATH, '/html/body/main/div[3]/div[2]/div[2]/div')
        data = data_element.get_attribute('aria-label')
        if "m/s" in data and " @ " in data:
            direction, speed = data.split(" @ ")
            direction = direction.replace("°", "")
            speed = speed.strip(" m/s")
            return [date, lat, lon, direction, speed]
        else:
            return [date, lat, lon, "", ""]
    except NoSuchElementException:
        return [date, lat, lon, "", ""]

driver = webdriver.Chrome()

input_file_path = '/Users/rafiandrianto/Desktop/DataScience/data/Modified_DateLongLat.csv'
output_file_path = '/Users/rafiandrianto/Desktop/DataScience/data/ScrapedOceanCurrentV2.csv'

with open(input_file_path, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    with open(output_file_path, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date', 'Latitude', 'Longitude', 'Ocean Current Direction', 'Ocean Current Speed (m/s)'])

        for row in reader:
            if '/' in row['Date'] and len(row['Date'].split('/')) == 3:
                month, day, year = row['Date'].split('/')
                formatted_date = f"{year}/{month}/{day}/"
                full_date = formatted_date + "0300Z"
                date = "/".join(full_date.split("/")[0:3])

                lat = float(row['Latitude'])
                lon = float(row['Longitude'])
                coordinates = f"loc={lon},{lat}"
                url = f"https://earth.nullschool.net/#{full_date}/ocean/surface/currents/orthographic=-218.21,27.84,420/{coordinates}"
                data_row = extract_and_parse_data(url, date, lat, lon)
                writer.writerow(data_row)

driver.quit()
