# Media Channel Download Link Gatherer

This Python script retrieves and organizes download links for media content (videos, photos) from specified media channels. It recursively processes subchannels and outputs a JSON file containing the download links and filenames of the highest-quality available resources.

## Features

- 📥 Retrieves the best quality download links for videos.
- 🔄 Supports recursive processing of channels and subchannels.
- 💾 Outputs the gathered download links to a JSON file (`download.json`).
- 🖥️ Terminal color codes for enhanced readability.

## Prerequisites

- **Python 3.6+**
- **Required Python packages:**
  - `argparse` (standard library)
  - `requests`
  - `unidecode`

Ensure you have the `ms_client` library installed and correctly configured. The `ms_client.client.MediaServerClient` class is expected to provide `api` and `check_server` methods.

## Installation

1. Clone the repository or download the script file.
2. Install required packages using pip:
    ```bash
    pip install requests unidecode
    ```
3. Place the `ms_client` library in your Python path if it's not already available.

## Usage

Run the script with the following command:

```bash
python3 script_name.py --conf <path_to_configuration_file> --channel <channel_oid>

Arguments

    --conf: The path to the configuration file for ms_client. The path can be either local or a Unix socket (e.g., unix:/path/to/socket).
    --channel: The channel_oid (channel ID) from which to gather media download links.

Example

python3 script_name.py --conf /path/to/config.json --channel abc123

This command will process channel abc123, retrieve all available download links, and save them to download.json in the current directory.
Output

The script outputs a JSON file (download.json) in the following format:

[
  {
    "filename": "Example Video Title",
    "download_link": "https://media.server/download/link1"
  },
  {
    "filename": "Another Video Title",
    "download_link": "https://media.server/download/link2"
  }
]

Notes

    The script only processes videos and skips items in unsupported formats.
    The TIMEOUT setting in ms_client is extended to handle longer requests.

Troubleshooting

    Invalid path for configuration file: Ensure that the path provided in --conf exists and is accessible.
    Error retrieving links: This could be due to network issues, an incorrect channel_oid, or access restrictions. Check the error messages in the terminal for more details.

License

This project is licensed under the MIT License. See the LICENSE file for details.


### Explanation of Sections

- **Overview**: Brief description of the script.
- **Features**: List of features with emojis to enhance readability.
- **Prerequisites**: Required Python version, packages, and `ms_client` setup.
- **Installation**: Step-by-step setup instructions.
- **Usage**: Command structure, argument descriptions, and usage example.
- **Output**: JSON format for output, example included.
- **Notes**: Additional details on format handling and timeout.
- **Troubleshooting**: Common errors and solutions.
- **License**: License information with a link to `LICENSE` (if included).
