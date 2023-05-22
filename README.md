# License Plate Recognition System for Vehicle Tracking

This project aims to develop a License Plate Recognition (LPR) system that can detect and recognize license plates in vehicle images and videos. The system utilizes the YOLOv7 model for license plate detection and PaddleOCR for text extraction from the detected plates. It provides functionalities for video-based tracking of vehicles and searching a database for stolen cars based on their license plate information.

## Methodology

1. Dataset Collection and Annotation

   - Gathered a dataset of vehicles with Egyptian license plate images.
   - Used the annotation tool, labelimg, to manually label the license plates by drawing bounding boxes around them.
   - Saved the annotations in XML format with the coordinates of the bounding boxes.
   - Converted the XML files to YOLO annotations for training.

2. Model Training

   - Fed the prepared dataset and configuration files into the YOLOv7 model.
   - Trained the model to detect license plates by adjusting its parameters through backpropagation and gradient descent optimization.
   - Experimented with different hyperparameter settings and settled for 300 Epochs and 32 Batch size.

3. Model Evaluation

   - Evaluated the trained YOLOv7 model on a separate validation or test dataset.
   - Measured metrics like precision, recall, and F1-score to assess the model's accuracy and effectiveness in license plate detection.

4. Video Testing and License Plate Recognition

   - Loaded the trained model and applied it to video frames for license plate detection.
   - Extracted the license plate regions as regions of interest (ROI).
   - Utilized PaddleOCR to extract the text from the license plates.
   - Parsed the recognized text to obtain the alphanumeric characters.
   - Performed post-processing steps to refine and validate the extracted text, including filtering, language verification (Arabic), length validation based on Egyptian plates, noise removal, and error correction.
   - Saved the license plate data along with the last seen location in a JSON file.

5. Detection Website

   - Set up a Flask server hosting a detection function based on the YOLO algorithm.
   - Received car images from a website and sent them to the server for license plate detection.
   - Extracted and validated the text from the detected license plates.
   - Searched the data file, containing information about stolen cars, using the validated text to check for matches.
   - Identified potentially stolen cars based on matches in the data file, providing information about the corresponding stolen locations.

6. Results

   The project achieved the following results:

   - Implemented a system that stores information about stolen cars, including license plate numbers, corresponding locations, and video evidence, in a centralized database.
   - Attained the following accuracy metrics:
     - Fitness value accuracy: 76.81%
     - Precision accuracy: 99.997%
     - Recall accuracy: 98.07%
   - Demonstrated the system's effectiveness in identifying stolen cars and accurately determining their locations.
   - The high precision score indicates minimal false alarms, while the high recall score suggests successful detection of a large portion of actual stolen cars.
   - Overall, the system serves as a valuable resource for recovering stolen vehicles and supporting law enforcement efforts.

## Usage

To use the License Plate Recognition system:

1. Set up the required dependencies and libraries mentioned in the project documentation.
2. Collect and annotate a dataset of vehicle images with labeled license plates.
3. Train the YOLOv7 model using the prepared dataset and configuration files.
4. Evaluate the trained model's performance using appropriate metrics.
5. Apply the trained model to video frames for license plate detection and recognition.
6. Perform post-processing steps to refine and validate the extracted license plate text.

``
