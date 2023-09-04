from onvif import ONVIFCamera
import cv2
import threading    

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

def capture_frame(cap, frame_container,run_flag):
    while run_flag[0]:
        ret, frame = cap.read()
        if ret:
            frame_container[0] = frame

def connect_to_camera(ip, port, user, password):
    mycam = ONVIFCamera(ip, port, user, password)
    media_service = mycam.create_media_service()
    media_profile = media_service.GetProfiles()[0]

    # Create PTZ service object
    ptz = mycam.create_ptz_service()

    
    return media_service, media_profile, ptz

def get_stream_uri(media_service, media_profile):
    # Get stream URI
    request = media_service.create_type('GetStreamUri')
    request.ProfileToken = media_profile.token
    request.StreamSetup = {
        'Stream': 'RTP-Unicast',
        'Transport': {'Protocol': 'RTSP'}
    }
    resp = media_service.GetStreamUri(request)
    return resp.Uri

def main():

    # Data Camera 1 -> K1
    ip_1 = '192.168.1.135'  
    port = 80 
    user = 'admin' 
    password = '123456'  

    # Data Camera 2 -> K2
    ip_2 = '192.168.1.67'  # Replace with your camera's IP
    port = 80  # Replace with your camera's port
    user = 'admin'  # Replace with your camera's username
    password = '123456'  # Replace with your camera's password


    run_flag = [True]  # Shared flag to control the threads
    # Connect to the camera
    media_service_c1, media_profile_c1, ptz = connect_to_camera(ip_1, port, user, password)
    # media_service_c2, media_profile_c2, ptz = connect_to_camera(ip_2, port, user, password)


    
# Get Stream URI
    stream_uri_c1 = get_stream_uri(media_service_c1, media_profile_c1)
    # stream_uri_c2 = get_stream_uri(media_service_c2, media_profile_c2)
    
    # Display video stream
    cap_1 = cv2.VideoCapture(stream_uri_c1)
    # cap_2 = cv2.VideoCapture(stream_uri_c2)

    frame_1 = [None]
    # frame_2 = [None]

    # Start threads to capture frames
    thread_1 = threading.Thread(target=capture_frame, args=(cap_1, frame_1, run_flag))
    # thread_2 = threading.Thread(target=capture_frame, args=(cap_2, frame_2))
    thread_1.start()
    # thread_2.start()

    screen_width = 1920
    screen_height = 1080

    while True:
        if frame_1[0] is not None: # and frame_2[0] is not None:
            # Process and display frames
                    # Resize frames to fit the window size
            frame_1_resized = cv2.resize(frame_1[0], (screen_width, screen_height))
            # frame_2_resized = cv2.resize(frame_2[0], (screen_width, screen_height))
            cv2.imshow('Camera 1', frame_1_resized)
            # cv2.imshow('Camera 2', frame_2_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_1.release()
    # cap_2.release()
    thread_1.join()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()