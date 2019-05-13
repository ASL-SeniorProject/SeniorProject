'''
Original author: Joe Lipinski
Date written:    05/12/19
Last modified:   05/12/19
Intent:          Take a image and rgb thresholds and apply them to an image
'''

class ImageProcessing():
    def cropImage(self, img):
        top = len(img)
        bottom = 0
        left = len(img[0])
        right = 0
        i_limit = len(img)
        for i in range(0, i_limit):
            j_limit = len(img[0])
            for j in range(0, j_limit):
                if i < top:
                    top = i
                if i > bottom:
                    bottom = i
                if j < left :
                    l = j
                if j > right:
                    right = j
        return img[top:bottom][left:right]
    '''
    Take the threshold arguement and convert it into a proper list of integer values
    '''
    def processThresholds(self, thresholds):
        newTresholds = []
        for thresh in thresholds:
            newTresholds.append(int(thresh))
        return newTresholds

'''
Main method
Args: 
    imageName : the name of the image
    thresholds: '[red_low, red_high, green_low, green_high, blue_low, blue_high]'
'''
if __name__ == "__main__":
    import sys
    import cv2
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg

    # Process arguements #
    imageName = sys.argv[1]
    image_processing = ImageProcessing()
    thresholds = image_processing.processThresholds(sys.argv[2].split(','))
    
    # Obtain rgb thresholds #
    red_low  = thresholds[0]
    red_hgh = thresholds[1]
    green_low  = thresholds[2]
    green_high = thresholds[3]
    blue_low  = thresholds[4]
    blue_high = thresholds[5]

    # Read in the image #
    img = mpimg.imread(imageName)
    # Convert the image to a list for processing
    img = img.tolist()
    # Apply thresholds #
    for row in range(0, len(img)):
        for col in range(0, len(img[row])):
            if red_low > img[row][col][0] or red_hgh < img[row][col][0]:
                img[row][col] = [255,255,255]
            if green_low > img[row][col][1] or green_high < img[row][col][1]:
                img[row][col] = [255,255,255]
            if blue_low > img[row][col][2] or blue_high < img[row][col][2]:
                img[row][col] = [255,255,255]
            
    # Convert img into a numpy array #
    img = np.array(img)
    # "Show" the image, causes plt to have knowledge of it #
    plt.imshow(img)
    # Turn off the axis so it can be saved nicely #
    plt.axis('off')
    # Save the figure #
    plt.savefig(imageName + '_isolated.jpg')