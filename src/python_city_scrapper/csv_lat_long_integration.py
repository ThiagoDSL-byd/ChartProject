import requests
import pandas as pd
import json

def fetch_json_data(url):
    # Fetch JSON data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    json_data = response.content.decode('utf-8-sig')

    return json.loads(json_data)

def add_lat_long_to_csv(json_data, csv_path, output_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
    
    # Create a lookup dictionary from the JSON data
    city_coordinates = {
        item["nome"].lower(): (item["latitude"], item["longitude"])
        for item in json_data
    }
    
    # Prepare a list to hold the rows of the new DataFrame
    rows = []

    # Match cities and add latitude and longitude
    for index, row in df.iterrows():
        city_name = row["Município"].strip().lower()
        if city_name in city_coordinates:
            latitude, longitude = city_coordinates[city_name]
            rows.append({"city": row["Município"], "latitude": latitude, "longitude": longitude})
    
    # Create a new DataFrame from the collected rows
    result_df = pd.DataFrame(rows, columns=["city", "latitude", "longitude"])
    
    # Save the result DataFrame to a new CSV file
    result_df.to_csv(output_path, sep=',', index=False, encoding='utf-8')
    
if __name__ == "__main__":
    # JSON URL and paths to the input/output CSV files
    json_url = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/json/municipios.json"
    csv_input_path = "cities_by_population.csv"
    csv_output_path = "cities_with_coordinates.csv"
    
    # Fetch JSON data
    json_data = fetch_json_data(json_url)
    
    # Process the CSV file and add latitude and longitude
    add_lat_long_to_csv(json_data, csv_input_path, csv_output_path)
    
    print(f"Updated CSV file saved to {csv_output_path}")
