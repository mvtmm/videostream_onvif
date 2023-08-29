from onvif import ONVIFCamera
import cv2

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

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
    ip = '192.168.1.67'  # Replace with your camera's IP
    port = 80  # Replace with your camera's port
    user = 'admin'  # Replace with your camera's username
    password = '123456'  # Replace with your camera's password
    
    # Connect to the camera
    media_service, media_profile, ptz = connect_to_camera(ip, port, user, password)
    
    # Get Stream URI
    stream_uri = get_stream_uri(media_service, media_profile)
    
    # Display video stream
    cap = cv2.VideoCapture(stream_uri)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to get frame")
            break

        cv2.imshow('ONVIF Camera Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
