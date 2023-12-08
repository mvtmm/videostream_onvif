# ONVIF Camera Stream Manager

## Overview
This Python script is designed to manage video streams from two ONVIF cameras. It automatically switches between the cameras based on the brightness level of the video feed from the first camera. When the brightness exceeds a defined threshold, the script switches to the second camera. This functionality is particularly useful in scenarios where varying light conditions affect the visibility of the camera feed.

## Features
- Connect to two ONVIF cameras.
- Continuously capture video streams from both cameras.
- Calculate the average brightness of the video feed from the first camera.
- Switch to the second camera if the brightness level exceeds a specified threshold.
- Logging of key events and errors for easier debugging and monitoring.

## Requirements
- Python 3.x
- ONVIFCamera library
- OpenCV (cv2)
- Threading module

## Installation
Before running the script, ensure that you have Python 3.x installed on your system along with the necessary libraries. You can install the required libraries using pip:

```bash
pip install onvif-zeep python-opencv

## Configuration 
Before running the script, configure the IP addresses, ports, usernames, and passwords for your ONVIF cameras in the main function:

ip_1, ip_2 = '<Camera1_IP>', '<Camera2_IP>'
port, user, password = <Camera_Port>, '<Username>', '<Password>'
brightness_threshold = <Brightness_Threshold>


## Usage
Run the script using Python: 

```bash
python3 camera_stream_manager.py

The script will start capturing video feeds from both cameras. The feed from Camera 1 will be displayed until the brightness exceeds the threshold, after which it will switch to Camera 2.

##Quitting the Application

To quit the application, press 'q' while the video feed window is active. The script will safely close all connections and threads before exiting.

##Logging

The script logs important events and errors, which can be found in the console output. This is helpful for debugging and understanding the script's behavior during execution.

