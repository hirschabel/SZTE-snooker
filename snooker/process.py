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

    frame_count = 0
    previous_result = {}
    balls_expected_location = {}
    disappeared_balls = {}
    balls_in_pocket = {
        "top_left": [],
        "top_middle": [],
        "top_right": [],
        "bottom_left": [],
        "bottom_middle": [],
        "bottom_right": []
    }

    while video_capture.isOpened():
        frame_count += 1
        ret, frame = video_capture.read()

        if not ret:
            break

        # Find snooker table boundaries
        snooker_table, x, y, w, h = find_snooker_table(frame.copy())

        # Find balls present on table
        # RESULT CONTAINS LOCATION OF BALLS
        result = {
            "red": []
        }

        balls = find_balls(snooker_table.copy(), result)

        # Itt nézzük, hogy előző frame-ben volt, most nincs golyó
        for prev_key in previous_result:
            if prev_key != 'white' and prev_key not in result:
                disappeared_balls[prev_key] = frame_count
            if prev_key == 'red' and len(previous_result[prev_key]) != len(result[prev_key]):
                pass  # TODO: szükséges a red-ek cimkezese, jelenleg nem tudjuk megkülönböztetni őket

        # Itt nézzük, hogy tényleg eltűnt-e
        for disappeared_ball in list(disappeared_balls.keys()):
            if disappeared_ball in result.keys():
                del disappeared_balls[disappeared_ball]
            else:
                if disappeared_balls[disappeared_ball] > 10:  # Eltűnés frame határérték
                    del disappeared_balls[disappeared_ball]
                    balls_in_pocket[balls_expected_location[disappeared_ball]].append(disappeared_ball)

        previous_result = result


        # Find holes
        holes = find_holes(snooker_table.copy(), balls_in_pocket)

        # Final image
        final_image = cv2.addWeighted(balls, 0.5, holes, 0.5, 0)

        # Lehetséges leütések számítása
        for ball in result:
            white = result.get("white")
            other = result.get(ball)

            golyok = []
            if ball == "red":
                golyok = other
            else:
                golyok.append(other)

            for golyo in golyok:
                if (white and golyo) and (white != golyo):
                    white_ball_position = (white.get("x"), white.get("y"))  # Example coordinates of the white ball (x, y)
                    other_ball_position = (golyo.get("x"), golyo.get("y"))  # Example coordinates of the other ball (x, y)

                    # Calculate the line between the two points
                    line_thickness = 2
                    cv2.line(final_image, white_ball_position, other_ball_position, (255, 0, 0), line_thickness)

                    # Calculate the extended line beyond the other ball's position
                    delta_x = other_ball_position[0] - white_ball_position[0]
                    delta_y = other_ball_position[1] - white_ball_position[1]

                    temp_x, temp_y = other_ball_position
                    while 0 < temp_x < final_image.shape[1] and 0 <= temp_y < final_image.shape[0]:
                        temp_x += delta_x
                        temp_y += delta_y

                    extended_position = (int(temp_x), int(temp_y))

                    # Draw the extended line
                    cv2.line(final_image, other_ball_position, extended_position, (0, 255, 0), line_thickness)

                    ########################################################################################################
                    # Hova mehet be a golyó, ha most leütjük?

                    # Initial position of the line starting from the other ball
                    current_x, current_y = other_ball_position

                    # Iterate and extend the line until reaching the edge of the image
                    while 0 <= current_x < final_image.shape[1] and 0 <= current_y < final_image.shape[0]:
                        current_x += delta_x
                        current_y += delta_y

                    if current_x > final_image.shape[1]:
                        current_x = final_image.shape[1]

                    if current_y < final_image.shape[0]:
                        current_y = final_image.shape[0]

                    # Mark the final point where the line reaches the edge
                    final_position = (int(current_x), int(current_y))

                    # Find the intersection point with the image boundary
                    max_x, max_y = final_image.shape[1], final_image.shape[0]

                    if delta_x == 0:  # Vertical line
                        final_position = (other_ball_position[0], 0 if delta_y < 0 else max_y - 1)
                    else:
                        slope = delta_y / delta_x
                        if abs(slope) <= max_y / max_x:  # Intersects with left or right boundary
                            final_position = (
                            0 if delta_x < 0 else max_x - 1, int(other_ball_position[1] - slope * other_ball_position[0]))
                        else:  # Intersects with top or bottom boundary
                            final_position = (int(other_ball_position[0] - (1 / slope) * (
                                        other_ball_position[1] - (0 if delta_y < 0 else max_y - 1))),
                                              0 if delta_y < 0 else max_y - 1)

                    cv2.circle(final_image, final_position, 5, (0, 0, 255), -1)

                    ########################################################################################################
                    # Melyik lyukhoz lenne a golyó legközelebb?

                    top_boundary = int(final_image.shape[0] * 0.2)  # 20% of the image height
                    bottom_boundary = int(final_image.shape[0] * 0.8)  # 80% of the image height
                    left_boundary = int(final_image.shape[1] * 0.333)  # 33.3% of the image width
                    right_boundary = int(final_image.shape[1] * 0.666)  # 66.6% of the image width

                    # Check the position of the marked point relative to the defined boundaries
                    if final_position[1] < top_boundary:
                        if final_position[0] < left_boundary:
                            balls_expected_location[ball] = "top_left"
                        elif left_boundary <= final_position[0] <= right_boundary:
                            balls_expected_location[ball] = "top_middle"
                        else:
                            balls_expected_location[ball] = "top_right"
                    elif final_position[1] > bottom_boundary:
                        if final_position[0] < left_boundary:
                            balls_expected_location[ball] = "bottom_left"
                        elif left_boundary <= final_position[0] <= right_boundary:
                            balls_expected_location[ball] = "bottom_middle"
                        else:
                            balls_expected_location[ball] = "bottom_right"

        # Write the processed frame to the output video
        frame[y:y + h, x:x + w] = final_image
        out.write(frame)

        # Display the processed frame (optional)
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and writer
    video_capture.release()
    out.release()
    cv2.destroyAllWindows()
