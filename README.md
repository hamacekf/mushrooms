# Mushroom Growth probability in Czech Republic

This script fetches an image from Český hydrometeorologický ústav, processes it to detect specific color ranges, and calculates the probability of mushroom growth in a specified region. Additionally, it sends an email with the results. The code is automated via GitHub actions to send it on every Thursday.

## Dependencies

- `requests`
- `Pillow` (PIL)
- `numpy`
- `matplotlib`
- `opencv-python`
- `email`
- `smtplib`
- `sys`
- `datetime`
- `os`


## Usage

1. **Set up environment variables**:

    Ensure the following environment variables are set:

    - `EMAIL_USERNAME`: Your email username.
    - `EMAIL_PASSWORD`: Your email password.
    - `RECIPIENTS`: A comma-separated list of email recipients.

2. **Run the script**:

    ```bash
    python script.py
    ```

    The script performs the following steps:

    - Downloads an image from the specified URL.
    - Processes the image to detect specific color ranges.
    - Calculates the probability of mushroom growth in the specified region.
    - Displays the probabilities and the processed image.
    - Sends an email with the results.

## Functions

### `send_email(username, password, recipients, subject, body)`

Sends an email with the specified subject and body to the list of recipients.

### `visualize_color_ranges(color_ranges)`

Visualizes the color ranges defined for mushroom growth probabilities.

### `detect_and_display_probability(region_image, color_ranges)`

Detects and displays the probabilities of mushroom growth in the specified region of the image.

## Example

The script processes an image from [this URL](https://info.chmi.cz/bio/maps/houby_1.png), extracts a specific region, and calculates the probability of mushroom growth based on defined color ranges. The result is displayed and sent via email.

## Configuration

Edit the following variables in the script to customize the region and color ranges:

- `img_url`: URL of the image to be processed.
- `y_range` and `x_range`: Define the region of the image to be analyzed.
- `color_values`: Define the color ranges for different probability levels.

## Output

The script will print the dominant probability of mushroom growth in the specified region and send an email with the details.
