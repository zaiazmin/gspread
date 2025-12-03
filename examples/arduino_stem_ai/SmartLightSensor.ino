/*
 * Smart Light Sensor - STEM AI Example
 *
 * This code demonstrates a simple Machine Learning concept (Nearest Centroid Classifier)
 * running on an ESP32. It collects data from a sensor (LDR), trains a simple model
 * by calculating averages, and then classifies new data.
 *
 * Hardware:
 * - ESP32 Board
 * - Analog Sensor (LDR or Potentiometer) connected to ANALOG_PIN
 *
 * Usage:
 * Open Serial Monitor at 115200 baud.
 * Commands:
 * - "train_dark": Record data for Dark state.
 * - "train_bright": Record data for Bright state.
 * - "run": Start classifying sensor data.
 */

// --- Configuration ---
const int ANALOG_PIN = 34; // GPIO 34 (Analog ADC1_CH6)
const int SAMPLES_FOR_TRAINING = 100;
const int DELAY_BETWEEN_SAMPLES = 50; // ms

// --- Global Variables ---
// These hold the "learned" knowledge (the model)
float meanDark = 0;
float meanBright = 0;
bool isTrainedDark = false;
bool isTrainedBright = false;

// State machine for the application
enum AppState {
  IDLE,
  TRAINING_DARK,
  TRAINING_BRIGHT,
  RUNNING
};

AppState currentState = IDLE;

void setup() {
  Serial.begin(115200);

  // Configure the pin
  pinMode(ANALOG_PIN, INPUT);

  Serial.println("--- ESP32 STEM AI Example: Smart Light Sensor ---");
  Serial.println("Commands:");
  Serial.println("  'train_dark'   - Record 'Dark' samples");
  Serial.println("  'train_bright' - Record 'Bright' samples");
  Serial.println("  'run'          - Start AI classification");
  Serial.println("-------------------------------------------------");
}

void loop() {
  // 1. Handle Serial Input (User Commands)
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace

    if (command == "train_dark") {
      currentState = TRAINING_DARK;
      Serial.println("-> Starting Training for DARK...");
    } else if (command == "train_bright") {
      currentState = TRAINING_BRIGHT;
      Serial.println("-> Starting Training for BRIGHT...");
    } else if (command == "run") {
      if (isTrainedDark && isTrainedBright) {
        currentState = RUNNING;
        Serial.println("-> AI Model is Running...");
      } else {
        Serial.println("ERROR: You must train both Dark and Bright classes first!");
      }
    } else {
      Serial.println("Unknown command. Try 'train_dark', 'train_bright', or 'run'.");
    }
  }

  // 2. Main Logic based on State
  switch (currentState) {
    case IDLE:
      // Do nothing, wait for command
      break;

    case TRAINING_DARK:
      trainModel(0); // 0 = Dark
      currentState = IDLE;
      Serial.println("-> Training Complete for DARK. Mean value: " + String(meanDark));
      break;

    case TRAINING_BRIGHT:
      trainModel(1); // 1 = Bright
      currentState = IDLE;
      Serial.println("-> Training Complete for BRIGHT. Mean value: " + String(meanBright));
      break;

    case RUNNING:
      performInference();
      delay(500); // Slow down output for readability
      break;
  }
}

// --- Helper Functions ---

/**
 * Collects data and calculates the average (mean).
 * targetClass: 0 for Dark, 1 for Bright
 */
void trainModel(int targetClass) {
  long sum = 0;

  Serial.println("Collecting samples... Please hold the sensor condition steady.");

  for (int i = 0; i < SAMPLES_FOR_TRAINING; i++) {
    int val = analogRead(ANALOG_PIN);
    sum += val;
    // Simple progress bar
    if (i % 10 == 0) Serial.print(".");
    delay(DELAY_BETWEEN_SAMPLES);
  }
  Serial.println();

  float average = (float)sum / SAMPLES_FOR_TRAINING;

  if (targetClass == 0) {
    meanDark = average;
    isTrainedDark = true;
  } else {
    meanBright = average;
    isTrainedBright = true;
  }
}

/**
 * Reads sensor and classifies it based on the learned model.
 */
void performInference() {
  int currentVal = analogRead(ANALOG_PIN);

  // Calculate distance (absolute difference) to each class mean
  float distDark = abs(currentVal - meanDark);
  float distBright = abs(currentVal - meanBright);

  String prediction = "";
  float confidence = 0;

  // Nearest Neighbor Classification
  if (distDark < distBright) {
    prediction = "DARK";
    // Simple confidence metric (closer is better)
    confidence = 100 * (1 - (distDark / (distDark + distBright)));
  } else {
    prediction = "BRIGHT";
    confidence = 100 * (1 - (distBright / (distDark + distBright)));
  }

  Serial.print("Sensor: ");
  Serial.print(currentVal);
  Serial.print(" | Prediction: ");
  Serial.print(prediction);
  Serial.print(" (Confidence: ");
  Serial.print(confidence, 1);
  Serial.println("%)");
}
