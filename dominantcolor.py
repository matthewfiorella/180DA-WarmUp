import numpy as np
import cv2
from sklearn.cluster import KMeans

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)
    
    hist = hist.astype("float")
    hist /= hist.sum()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Establish rectangle to capture dominant color
    cv2.rectangle(frame, (500, 250), (600, 350), (0,255,0), 2)
    # Run K-Means on pixels within rectange
    sampleImg = rgb[500:600, 250:350]
    sampleImg = sampleImg.reshape((sampleImg.shape[0] * sampleImg.shape[1], 3)) #represent as row*column,channel number
    clt = KMeans(n_clusters = 1) # cluster number
    clt.fit(sampleImg)
    #Get dominantColor and creat image with that color
    dominantColor = clt.cluster_centers_
    blank_image = np.zeros((100, 100, 3), np.uint8)
    blank_image[:,:,:] = dominantColor
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('dominant color', blank_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()