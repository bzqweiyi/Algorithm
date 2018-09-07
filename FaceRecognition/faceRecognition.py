import os
import cv2
import numpy as np
from sklearn import preprocessing
# Class to handle tasks related to label encoding
class LabelEncoder(object):
    # Method to encode labels from words to numbers
    def encode_labels(self, label_words):
        self.le = preprocessing.LabelEncoder()
        self.le.fit(label_words)
    # Convert input label from word to number
    def word_to_num(self, label_word):
        print("[label_word]",[label_word])
        print("self.le.transform([label_word])[0]",self.le.transform([label_word])[0])
        print("int(self.le.transform([label_word])[0])",int(self.le.transform([label_word])[0]))
        return int(self.le.transform([label_word])[0])
    # Convert input label from number to word
    def num_to_word(self, label_num):
        return self.le.inverse_transform([label_num])[0]
# Extract images and labels from input path
def get_images_and_labels(faceCascade,input_path):
    label_words = []
    # Iterate through the input path and append files
    for root, dirs, files in os.walk(input_path):
        for filename in (x for x in files if x.endswith('.jpg')):
            filepath = os.path.join(root, filename)
            label_words.append(filepath.split('\\')[-2])
    print("label_words",label_words)
    print("filepath",filepath)
    # Initialize variables
    images = []
    le = LabelEncoder()
    le.encode_labels(label_words)
    print("le",le)
    labels = []
    # Parse the input directory
    for root, dirs, files in os.walk(input_path):
        for filename in (x for x in files if x.endswith('.jpg')):
            filepath = os.path.join(root, filename)
            # Read the image in grayscale format
            image = cv2.imread(filepath, 0)
            # Extract the label
            name = filepath.split('\\')[-2]
            # Perform face detection
            faces = faceCascade.detectMultiScale(image, 1.1, 2, minSize=(100,100))
            # Iterate through face rectangles
            # print(faces)
            for (x, y, w, h) in faces:
                images.append(image[y:y+h, x:x+w])
                labels.append(le.word_to_num(name))
                print("x,y,w,h",x,y,w,h,"filepath=",filepath)
            print("labels=",labels)
    return images, labels, le
class my_face_reconginizer:
    def __init__(self, cascade_path = r"cascade_files\haarcascade_frontalface_alt.xml",
                      path_train = r'faces_dataset\train', path_test = r'faces_dataset\test'):
        self.faceCascade = cv2.CascadeClassifier(cascade_path) #人脸级联文件。
        self.path_train=path_train
        self.path_test=path_test
    def Recongizer_train(self):
        self.images, self.labels, self.le = get_images_and_labels(self.faceCascade,self.path_train)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        print( "\nTraining...")
        self.recognizer.train(self.images, np.array(self.labels))
    def Recongizer_Predict(self):
        # Test the recognizer on unknown images
        print('\nPerforming prediction on test images...')
        stop_flag = False
        for root, dirs, files in os.walk(self.path_test):
            for filename in (x for x in files if x.endswith('.jpg')):
                filepath = os.path.join(root, filename)
                # Read the image
                predict_image = cv2.imread(filepath, 0)
                print("predict_image",predict_image)
                print("filepath",filepath)
                print("type(predict_image)",type(predict_image))
                print("shape(predict_image)",np.shape(predict_image))
                # Detect faces
                faces = self.faceCascade.detectMultiScale(predict_image, 1.1,
                        2, minSize=(100,100))
                print("faces",faces)
                # Iterate through face rectangles
                for (x, y, w, h) in faces:
                    # Predict the output
                    predicted_index, conf = self.recognizer.predict(
                            predict_image[y:y+h, x:x+w])
                    # Convert to word label
                    predicted_person = self.le.num_to_word(predicted_index)
                    # Overlay text on the output image and display it
                    cv2.putText(predict_image, 'Prediction: ' + predicted_person,
                            (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),3)
                    cv2.imshow("Recognizing face", predict_image)
                c = cv2.waitKey(0)
                if c == 27:
                    stop_flag = True
                    break
            return 0
            if stop_flag:
                break
test1=my_face_reconginizer()
test1.Recongizer_train()
test1.Recongizer_Predict()