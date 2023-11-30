import cv2
from snooker_table import find_snooker_table
from balls import find_balls
from holes import find_holes


# Videó feldolgozás
def process_video(input_path, output_path):
    # Open the video file
    video_capture = cv2.VideoCapture(input_path)

    # Get video properties
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Create VideoWriter object to save the processed video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Find snooker table boundaries
        _, snooker_table = find_snooker_table(frame.copy())

        # Find balls present on table
        # RESULT CONTAINS LOCATION OF BALLS
        result = {
            "red": []
        }

        balls = find_balls(snooker_table.copy(), result)

        # Find holes
        holes = find_holes(snooker_table.copy())

        # Final image
        final_image = cv2.addWeighted(balls, 0.5, holes, 0.5, 0)

        # Write the processed frame to the output video
        out.write(final_image)

        # Display the processed frame (optional)
        cv2.imshow('Processed Frame', final_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and writer
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()


# Ez az eddigi működés értékek állítgatására jó
def process_picture():
    # Read the image
    orig_image = cv2.imread("videos/teszt1.png")

    # Find snooker table boundaries
    img, snooker_table = find_snooker_table(orig_image.copy())

    # Find balls present on table
    balls = find_balls(snooker_table.copy())

    # Find holes
    holes = find_holes(snooker_table.copy())

    # Final image
    final_image = cv2.addWeighted(balls, 0.5, holes, 0.5, 0)

    # ======Results======
    # Original Image
    cv2.imshow('Original Image', orig_image)
    cv2.waitKey(0)

    # Snooker Table
    cv2.imshow('Snooker Table', snooker_table)
    cv2.waitKey(0)

    # Balls Highlighted
    cv2.imshow('Balls Highlighted', balls)
    cv2.waitKey(0)

    # Holes Highlighted
    cv2.imshow('Holes Highlighted', holes)
    cv2.waitKey(0)

    # Final image
    cv2.imshow('Final', final_image)
    cv2.waitKey(0)

    # Clean-up
    cv2.destroyAllWindows()
