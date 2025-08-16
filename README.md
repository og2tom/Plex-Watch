# Plex-Watch 🎬

![Plex-Watch](https://img.shields.io/badge/Plex--Watch-v1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-yellow.svg)

## Introduction

Plex-Watch is a powerful tool designed to enhance your Plex media server experience. If you’ve ever faced issues with Plex not updating your library from network storage, this tool is for you. Plex-Watch actively monitors your media folders and ensures that Plex stays in sync with your content. With its automation capabilities, you can enjoy a seamless media experience without the hassle of manual updates.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Releases](#releases)

## Features

- **Automatic Library Updates**: Plex-Watch keeps your Plex library updated automatically.
- **File Monitoring**: Monitors your media folders for any changes in real-time.
- **Support for Multiple Protocols**: Works with NFS and SMB protocols for accessing network storage.
- **Lightweight and Fast**: Designed to run efficiently without consuming excessive resources.
- **Python-Based**: Built with Python, making it easy to modify and extend.
- **Cross-Platform**: Runs on various operating systems, including Windows, macOS, and Linux.

## Installation

To get started with Plex-Watch, follow these simple steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/og2tom/Plex-Watch.git
   ```

2. **Navigate to the Directory**:
   ```bash
   cd Plex-Watch
   ```

3. **Install Dependencies**:
   Ensure you have Python 3.7 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and Execute the Latest Release**:
   Visit the [Releases](https://github.com/og2tom/Plex-Watch/releases) section to download the latest version. Follow the instructions provided in the release notes for execution.

## Usage

After installation, you can start using Plex-Watch. Here’s how:

1. **Run the Script**:
   Execute the main script to start monitoring your media folders:
   ```bash
   python plex_watch.py
   ```

2. **Monitor Specific Folders**:
   You can specify which folders to monitor by editing the configuration file. This allows you to focus on specific media directories.

3. **Check Logs**:
   Plex-Watch generates logs to help you track its activity. Check the logs to ensure everything is functioning correctly.

## Configuration

To configure Plex-Watch, locate the `config.json` file in the root directory. Here’s a breakdown of the configuration options:

```json
{
    "media_folders": [
        "/path/to/media1",
        "/path/to/media2"
    ],
    "plex_server": {
        "host": "http://localhost:32400",
        "token": "YOUR_PLEX_TOKEN"
    },
    "check_interval": 60
}
```

- **media_folders**: List the paths to your media directories.
- **plex_server**: Provide the host and token for your Plex server.
- **check_interval**: Set the interval (in seconds) for checking the media folders.

## Contributing

We welcome contributions to Plex-Watch! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request. Here’s how to contribute:

1. **Fork the Repository**.
2. **Create a New Branch**:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make Your Changes**.
4. **Commit Your Changes**:
   ```bash
   git commit -m "Add Your Feature"
   ```
5. **Push to Your Fork**:
   ```bash
   git push origin feature/YourFeature
   ```
6. **Create a Pull Request**.

## License

Plex-Watch is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, feel free to reach out:

- **Email**: support@plex-watch.com
- **GitHub**: [og2tom](https://github.com/og2tom)

## Releases

For the latest updates and releases, visit the [Releases](https://github.com/og2tom/Plex-Watch/releases) section. Download the latest version and follow the provided instructions to keep your Plex library in sync.

## Conclusion

Plex-Watch simplifies the management of your Plex media server. By automating library updates and monitoring your media folders, it allows you to focus on enjoying your content. Whether you’re a casual user or a media enthusiast, Plex-Watch is a valuable tool for maintaining your media library. 

Explore the features, contribute to the project, and ensure your Plex server is always up-to-date. Happy watching!