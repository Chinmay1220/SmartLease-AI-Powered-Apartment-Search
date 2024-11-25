import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# List of URLs and the base output folder
urls = [
    "https://www.trulia.com/building/gardner-street-apartments-75-84-gardner-st-allston-ma-02134-2459183108",
    "https://www.trulia.com/building/dot-block-1211-dorchester-ave-dorchester-ma-02125-2562347969",
    "https://www.trulia.com/building/harbor-point-24-oyster-bay-rd-boston-ma-02125-1001477589",
]
output_folder = r"C:\SEM_3\Big Data\poc_scrape"

# Function to scrape data for a given URL
def scrape_url(url, base_output_folder):
    # Create a folder for this specific URL
    folder_name = url.split("/")[-1]
    url_output_folder = os.path.join(base_output_folder, folder_name)
    os.makedirs(url_output_folder, exist_ok=True)

    # Send a GET request to the website
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(f"Error fetching the webpage for {url}: {e}")
        return

    # 1. Scrape all images
    image_folder = os.path.join(url_output_folder, "images")
    os.makedirs(image_folder, exist_ok=True)

    images = soup.find_all("img")
    if not images:
        print(f"No images found on the page for {url}.")
    else:
        for i, img in enumerate(images):
            img_url = img.get("src")
            if img_url:
                # Handle relative and malformed URLs
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif not img_url.startswith("http"):
                    img_url = urljoin(url, img_url)

                # Validate URL
                if img_url.startswith("http"):
                    try:
                        print(f"Downloading image: {img_url}")
                        img_data = requests.get(img_url).content
                        img_name = f"image_{i+1}.jpg"
                        with open(os.path.join(image_folder, img_name), "wb") as f:
                            f.write(img_data)
                    except Exception as e:
                        print(f"Failed to download image {img_url}: {e}")
                else:
                    print(f"Skipped invalid URL: {img_url}")

    # 2. Get apartment details
    apartment_details = {}
    try:
        # Updated apartment name selector using the class
        apartment_name_tag = soup.find("h1", class_="Text__TextBase-sc-13iydfs-0 EPOtA")
        apartment_name = apartment_name_tag.text.strip() if apartment_name_tag else "N/A"

        address = soup.find("div", {"data-testid": "home-details-summary-address"}).text.strip() if soup.find("div", {"data-testid": "home-details-summary-address"}) else "N/A"

        apartment_details["Apartment Name"] = apartment_name
        apartment_details["Address"] = address

        # Save details to a text file
        details_file = os.path.join(url_output_folder, "apartment_details.txt")
        with open(details_file, "w") as f:
            for key, value in apartment_details.items():
                f.write(f"{key}: {value}\n")
    except Exception as e:
        print(f"Error fetching apartment details for {url}: {e}")

    # 3. Get house description
    try:
        description = soup.find("div", {"data-testid": "home-description-text-description-text"}).text.strip() if soup.find("div", {"data-testid": "home-description-text-description-text"}) else "N/A"

        # Save description to a text file
        description_file = os.path.join(url_output_folder, "house_description.txt")
        with open(description_file, "w") as f:
            f.write(description)
    except Exception as e:
        print(f"Error fetching house description for {url}: {e}")

    # 4. Get Cost and Fees Section
    try:
        cost_and_fees = soup.find("div", {"data-testid": "rentalCostAndFees"})
        if cost_and_fees:
            cost_and_fees_text = cost_and_fees.get_text(separator="\n").strip()
            cost_and_fees_file = os.path.join(url_output_folder, "cost_and_fees.txt")
            with open(cost_and_fees_file, "w") as f:
                f.write(cost_and_fees_text)
            print(f"Cost and Fees section saved successfully for {url}.")
        else:
            print(f"Cost and Fees section not found for {url}.")
    except Exception as e:
        print(f"Error fetching Cost and Fees section for {url}: {e}")

    # 5. Get All Text from Home Highlights Container
    try:
        highlights_container = soup.find("div", {"data-testid": "home-highlights-container"})
        if highlights_container:
            highlights_text = highlights_container.get_text(separator="\n").strip()
            highlights_file = os.path.join(url_output_folder, "home_highlights.txt")
            with open(highlights_file, "w") as f:
                f.write(highlights_text)
            print(f"Home Highlights section saved successfully for {url}.")
        else:
            print(f"Home Highlights container not found for {url}.")
    except Exception as e:
        print(f"Error fetching Home Highlights container for {url}: {e}")

    print(f"Scraping completed successfully for {url}. Check the folder: {url_output_folder}")

# Loop through each URL and scrape the data
for url in urls:
    scrape_url(url, output_folder)
