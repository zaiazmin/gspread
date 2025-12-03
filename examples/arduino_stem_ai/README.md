# Smart Light Sensor with Artificial Intelligence (AI)

This project is a STEM education example demonstrating how to collect data and use a simple Artificial Intelligence (AI) concept on an ESP32 microcontroller.

## Project Overview

The goal is to create a "Smart Light Sensor" that can learn to distinguish between "Dark" and "Bright" environments. Instead of hardcoding a threshold value (e.g., `if value < 500`), the system will **learn** the characteristics of "Dark" and "Bright" from the user.

This demonstrates the concept of **Supervised Learning** using a **Nearest Centroid Classifier**.

## Hardware Requirements

*   **ESP32 Board** (e.g., ESP32 DevKit V1)
*   **Light Dependent Resistor (LDR)** or a Potentiometer (to simulate sensor data)
*   **Resistor (10kΩ)** (if using LDR, for voltage divider)
*   Breadboard and Jumper wires

### Wiring (LDR)

1.  Connect one leg of the LDR to 3.3V.
2.  Connect the other leg of the LDR to a GPIO pin (e.g., GPIO 34) and also to one leg of the 10kΩ resistor.
3.  Connect the other leg of the resistor to GND.

*Note: If you don't have a sensor, you can use the built-in Touch sensors or just leave the pin floating to see random values (though less educational).*

## How it Works

The code has two modes: **Training** and **Inference**.

1.  **Data Collection & Training:**
    *   You tell the ESP32: "I am covering the sensor now, this is what 'Dark' looks like."
    *   The ESP32 records the sensor readings and calculates the average (mean) for 'Dark'.
    *   You tell the ESP32: "I am shining a light now, this is what 'Bright' looks like."
    *   The ESP32 records the sensor readings and calculates the average (mean) for 'Bright'.

2.  **Inference (AI Analysis):**
    *   The ESP32 constantly reads the sensor.
    *   It compares the current reading to the learned 'Dark' average and the learned 'Bright' average.
    *   It classifies the current state based on which average is closer (Nearest Neighbor).

## Usage

1.  Upload the code to your ESP32.
2.  Open the **Serial Monitor** (Baud rate: 115200).
3.  Type commands to control the AI:
    *   `train_dark`: Starts recording data for the "Dark" class (for 5 seconds). Cover the sensor!
    *   `train_bright`: Starts recording data for the "Bright" class (for 5 seconds). Shine light on the sensor!
    *   `run`: Starts the continuous inference mode.

## The "AI" Logic

This example uses a simplified **Nearest Centroid Classifier**:

1.  **Training Phase:**
    *   $Centroid_{dark} = \frac{1}{N} \sum_{i=1}^{N} x_i$ (where $x$ are sensor readings during dark phase)
    *   $Centroid_{bright} = \frac{1}{N} \sum_{i=1}^{N} x_i$ (where $x$ are sensor readings during bright phase)

2.  **Inference Phase:**
    *   Read new value $x_{new}$.
    *   Calculate distance to Dark: $D_{dark} = |x_{new} - Centroid_{dark}|$
    *   Calculate distance to Bright: $D_{bright} = |x_{new} - Centroid_{bright}|$
    *   If $D_{dark} < D_{bright}$, then Result = "Dark". Else, Result = "Bright".
