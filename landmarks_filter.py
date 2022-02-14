#Import libraries.
import cv2
import dlib
import base64
from imutils import resize, face_utils
from urllib.parse import quote

#Define dlib paths
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_face_landmarks_gtx.dat")

#Introduce CLAHE("Contrast Limited AHE(adapative-histogram-equalization)")
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))


#Define a new function to transform the uploaded image.
def get_image_with_landmarks(file_path: str):
    #convert image to grayscale
    rects = None
    gray = None
    clone = None
#Try capturing the image and process it to gray scale.
    try:
        image = cv2.imread(file_path, 1)
        image = resize(image, height=400)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clone = image.copy()
        rects = detector(gray, 1)
#If it doesn't work, return an error.
    except Exception:
        return {'error': 'Error:Unable to read image successfully. Please try again.'}
#If a face is found, enumerate the shape of the face using enumerate function and face utils library.  
    any_face_was_found = len(rects) > 0
    if any_face_was_found:
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            for point in range(1, 68):
                coords = shape.tolist()[point]
                cv2.circle(clone, (coords[0], coords[1]), 1, (0, 0, 255), thickness=2)
#If unable to enumerate the face, return an error.                 
    else:
        return {'error': 'Unable to detect a face present in the image provided.'}
#Capture the numerical value using Open CV2 with the imencode function.
    retval, buffer = cv2.imencode('.jpg', clone)

#Store the numerical value of the face in a clone using base64    
    image_as_text = base64.b64encode(buffer)
#Return the image with landmarks.
    return {'image_with_landmarks': 'data:image/png;base64,{}'.format(quote(image_as_text))}