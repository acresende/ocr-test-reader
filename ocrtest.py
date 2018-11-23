# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import json
import pprint
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image to be OCR'd")

ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="type of preprocessing to be done")

args = vars(ap.parse_args())


yourpath = r'C:/Projects/ocrtest/images/'

#convert image to jpeg

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        print(os.path.join(root, name))
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                print ("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
            else:
                outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                try:
                    im = Image.open(os.path.join(root, name))
                    print ("Generating jpeg for %s" % name)
                    im.thumbnail(im.size)
                    im.save(outfile, "JPEG", quality=100)
                except Exception as e:
                    print (e)

image = Image.open(r'C:/Projects/ocrtest/images/test.jpg')




#load the example image and convert it to grayscale
image = cv2.imread(args["image"])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

 
# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)
 
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)


# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file



image = Image.open(r'C:/Projects/ocrtest/images/test.jpg')

# text = pytesseract.image_to_string(image, lang='por')
data = pytesseract.image_to_data(image, lang='por', output_type=dict)
#os.remove(filename)



print('\n')
# print('=============================================================')
print('\n')


# opens json containing keywords that define regions of test
with open('keywords_list.json') as keywords_file:
    keywords_list = json.load(keywords_file)

# split lines of data
data_lines = data.splitlines()
data_matrix = []
# loop throught each line and append lines that contains keywords
for lines in data_lines:
    for item in keywords_list["keywords"]:
        if len(lines.split('\t')) == 12:
            if lines.split('\t')[11] in item['name'] and len(lines.split('\t')[11]) > 3:
                data_matrix.append(lines.split('\t'))

widthOffset = 240
heightOffset = 570
jsonData = {}
regions_matrix = []
jsonData['region'] = []
image = cv2.imread("C:/Projects/ocrtest/images/test.jpg")
print('\n')
'''
x1--------x2
|          |  
|          |
|          |
x3--------x4
'''
for element in data_matrix:
    x1 = int(element[6]) #- widthOffset
    y1 = int(element[7])

    x2 = int(element[6]) + int(element[8]) #+ widthOffset
    y2 = int(element[7])

    x3 = int(element[6])
    y3 = int(element[7]) + int(element[9]) # + heightOffset

    x4 = int(element[6]) + int(element[8])
    y4 = int(element[7]) + int(element[9]) # + heightOffset

    jsonData['region'].append({
        'upperLeftBoundX': str(x1),
        'upperLeftBoundY': str(y1),
        'upperRightBoundX': str(x2),
        'upperRightBoundY': str(y2),
        'bottomLeftBoundX': str(x3),
        'bottomLeftBoundY': str(y3),
        'bottomRightBoundX': str(x4),
        'bottomRightBoundY': str(y4)
    })

    regions_matrix = [x1, y1, x2, ]



cv2.rectangle(image, (x1, y1), (x4, y4), (255, 0, 0), 2)


with open('outputBounds.json', 'w') as outfile:
    json.dump(jsonData, outfile)

cv2.imwrite("layoutOutput.png", image)



# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)