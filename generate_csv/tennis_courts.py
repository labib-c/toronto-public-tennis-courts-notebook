from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

# Specify the path to the HTML file
html_file_path = 'Tennis Court Listings – City of Toronto.html'  # Replace with the actual file path

# Load the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table in the HTML
table = soup.find('table')  # Assuming there's only one table in the HTML

# Extract table headers
headers = []
header_row = table.find('thead').find_all('th') if table.find('thead') else table.find('tr').find_all('th')
for th in header_row:
    headers.append(th.text.strip())

# Extract table rows
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cells = row.find_all(['td', 'th'])
    row_data = []
    for cell in cells:
        # Check if the cell contains the "Map It" link
        link = cell.find('a', title="map it")
        if link and 'href' in link.attrs:
            # Parse the href to extract lat and lng
            href = link['href']
            query_params = parse_qs(urlparse(href).fragment)
            loc = query_params.get('location', [''])[0]
            lat = query_params.get('lat', [''])[0]
            lng = query_params.get('lng', [''])[0]
            # Add the lat/lng tuple to the "Map It" column
            row_data.append((loc, lat, lng))
        elif cell.find('strong') and 'Club:' in cell.text:
            # Extract the club name from the <strong> tag
            club_name = cell.find('strong').next_sibling.strip()
            row_data.append(club_name)
        else:
            # Add the cell text if it's not the "Map It" cell
            row_data.append(cell.text.strip())
    rows.append(row_data)

# Write the data to a CSV file
output_file = 'tennis_courts_toronto.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header
    csvwriter.writerow(headers)
    # Write the rows
    csvwriter.writerows(rows)

print(f"Data has been exported to {output_file}")