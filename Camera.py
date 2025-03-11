import cv2
import cvzone
from cvzone.ColorModule import ColorFinder

# Bruk de kalibrerte HSV-verdiene fra kalibreringen
hsvVals = {'hmin': 0, 'smin': 164, 'vmin': 139, 'hmax': 179, 'smax': 255, 'vmax': 218}  

# Kamera port
CAMERA_PORT = 1  
RESOLUTION = (640, 480)

# Opprett ColorFinder (ikke i kalibreringsmodus)
myColorFinder = ColorFinder(False)

# Åpne kamera
camera = cv2.VideoCapture(CAMERA_PORT, cv2.CAP_DSHOW)
if not camera.isOpened():
    print(f"Feil: Kunne ikke åpne kamera på port {CAMERA_PORT}")
    exit()

camera.set(3, RESOLUTION[0])  # Bredde
camera.set(4, RESOLUTION[1])  # Høyde

# Senterpunkt for referanse (kan settes til 0,0,0 hvis du ikke har en kjent referanse)
center_point = (RESOLUTION[0]//2, RESOLUTION[1]//2, 1000)  

def getBallPosition(cap, hsvVals, center_point):
    """
    Finn ballens posisjon basert på HSV-verdier.
    :return: (x, y, z) posisjon eller (None, None, None) hvis ingen ball funnet.
    """
    ret, img = cap.read()
    if not ret:
        return None, None, None

    # Prosesser bildet
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)

    # Vis bilde med sporing
    cv2.imshow("Ballsporing", imgContour)
    cv2.waitKey(1)

    # Sjekk om det finnes konturer (ballen funnet)
    if contours:
        x = contours[0]['center'][0] - center_point[0]
        y = (RESOLUTION[1] - contours[0]['center'][1]) - center_point[1]
        z = (contours[0]['area'] - center_point[2]) / 1000  # Skalert areal

        return x, y, z

    return None, None, None


# Hovedløkke for sporing
while True:
    x, y, z = getBallPosition(camera, hsvVals, center_point)
    
    if x is not None and y is not None and z is not None:
        print(f"Ballposisjon: X={x}, Y={y}, Z={z}")
    else:
        print("Ingen ball funnet")

    # Trykk 'q' for å avslutte
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Frigjør ressurser
camera.release()
cv2.destroyAllWindows()
