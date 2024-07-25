# Kameo-embed-generator

This Python program generates JWPlayer integration codes for M3U8 links, automatically adjusting video qualities when the resolution is not 1920x1080.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/kzyweb/kameo-embed-generator.git
    ```

2. Install dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

1. Edit example.env by adding your R2 Token data and rename the .env without the example.

2. Make sure you have a valid M3U8 link for your video content.

3. Run the `app.pyw` by clicking it.

4. This will bring up a blank page where you must enter the necessary data.

5. The program will generate a JWPlayer integration code with video quality options adjusted based on resolution.

## Features

- Automatic adjustment of video qualities for resolutions other than 1920x1080.
- Easy generation of JWPlayer embed for M3U8 links.

## TODO

- [x] Add option for Cloudflare integration for better rendering and efficient content delivery.
- [x] Add support to 720p resolution.
- [ ] Make better UI DESIGN, with qt ?
- [ ] Package the code in one single file .exe.

## Disclaimer

Ensure you use this program in accordance with local laws and regulations regarding online video content distribution.

---

© 2024 Kzyweb & Kameo
