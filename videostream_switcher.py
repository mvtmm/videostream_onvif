from onvif import ONVIFCamera
import cv2
import threading    
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

def capture_frame(cap, frame_container, run_flag):
    while run_flag[0]:
        ret, frame = cap.read()
        if ret:
            frame_container[0] = frame
        else:
            logging.warning("Frame capture failed.")

def calculate_brightness(frame):
    if frame is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        brightness = hsv[...,2].mean()
        return brightness
    return 0

def initialize_camera(ip, port, user, password):
    try:
        camera = ONVIFCamera(ip, port, user, password)
        media_service = camera.create_media_service()
        media_profile = media_service.GetProfiles()[0]
        request = media_service.create_type('GetStreamUri')
        request.ProfileToken = media_profile.token
        request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        stream_uri = media_service.GetStreamUri(request).Uri
        return cv2.VideoCapture(stream_uri)
    except Exception as e:
        logging.error(f"Error initializing camera at {ip}: {e}")
        raise

def switch_camera(current_camera, frame_brightness, threshold):
    if current_camera == 1 and frame_brightness > threshold:
        return 2
    elif current_camera == 2 and frame_brightness <= threshold:
        return 1
    else:
        return current_camera



def main():
    ip_1, ip_2 = '192.168.1.135', '192.168.1.67'
    port, user, password = 80, 'admin', '123456'
    brightness_threshold = 100
    screen_width, screen_height = 1920, 1080
    current_camera = 1
    run_flags = [[True], [True]]
    frames = [[None], [None]]

    try:
        caps = [initialize_camera(ip, port, user, password) for ip in [ip_1, ip_2]]
        threads = [threading.Thread(target=capture_frame, args=(cap, frame, run_flag)) 
                   for cap, frame, run_flag in zip(caps, frames, run_flags)]

        for thread in threads:
            thread.start()

        while True:
            if all(frame[0] is not None for frame in frames):
                frame_brightness = calculate_brightness(frames[0][0])
                current_camera = switch_camera(current_camera, frame_brightness, brightness_threshold)
                frame_display = cv2.resize(frames[current_camera - 1][0], (screen_width, screen_height))
                cv2.imshow(f'Camera {current_camera}', frame_display)
                logging.info(f"Displaying Camera {current_camera}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Quitting application.")
                break
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        for cap in caps:
            cap.release()
        for run_flag in run_flags:
            run_flag[0] = False
        for thread in threads:
            thread.join()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

