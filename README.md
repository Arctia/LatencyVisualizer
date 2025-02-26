# Ping Overlay

A lightweight, draggable overlay that displays real-time ping times to a configurable host.

## Features

* Real-time ping monitoring with color-coded status
* Draggable, always-on-top overlay
* Configurable host, port, and display settings
* Clean, minimal interface
* Automatic color changes based on ping times

## Release
* download the release from github to get the compiled version
* customize host, port and whatever you want in the config.json file
* run the program
* click and drag the red dot (●) to move the overlay
* right-click the red dot to close the application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Arctia/LatencyVisualizer.git
```
2. Create a file with your desired settings in the same folder:
```json
{
    "mode": "compact",
    "host": "google.it",
    "port": 443,
    "interval": 1.0,
    "color_ranges": {
        "optimal": 50,
        "good": 150,
        "warn": 230
    },
    "colors": {
        "optimal": "#00ee33",
        "good": "#00cc55",
        "warn": "orange",
        "critical": "red"
    }
}
```

## Usage

1. Run the script:
```bash
python ping.py
```
2. The overlay will appear in the top-left corner
3. Click and drag the red dot (●) to move the overlay
4. Right-click the red dot to close the application


## Technical Details

* Uses TCP socket connections for accurate ping measurements
* Implements threading for non-blocking UI updates
* Features transparent background with customizable opacity
* Includes drag-and-drop functionality
* Built with Python 3.x and Tkinter

## Dependencies

* Python 3.x
* tkinter (included with Python)
* socket (included with Python)
* json (included with Python)
* time (included with Python)
* threading (included with Python)
