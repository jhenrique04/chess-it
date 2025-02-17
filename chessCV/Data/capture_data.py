import cv2
import os

# Function to resize the frame


def rescale_frame(frame, percent=75):
    dim = (1000, 750)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


# Create the target directory if it doesn't exist
output_dir = "/test_data/"
os.makedirs(output_dir, exist_ok=True)

# Open the camera
cap = cv2.VideoCapture(2)  # Adjust the index as per your camera setup

capture_num = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize the frame for display
    small_frame = rescale_frame(frame)

    # Display the frame
    cv2.imshow('frame', small_frame)

    # Save the frame when 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        file_name = os.path.join(output_dir, f"frame{capture_num}.jpeg")
        cv2.imwrite(file_name, frame)
        print(f"Saved: {file_name}")
        capture_num += 1

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
