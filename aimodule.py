from mtcnn.mtcnn import MTCNN
from PIL import Image
from numpy import asarray
from os import listdir
from os.path import isdir
from re import split
from PIL import Image
from matplotlib import pyplot
from numpy import savez_compressed
#from numpy import load
from numpy import expand_dims
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from sklearn.externals import joblib
import cv2
import numpy as np
import menagetimes as tzd
import pickle

#facenet_model1 = load_model('facenet_keras.h5')
#out_encoder = LabelEncoder()
#out_encoder.classes_ = np.load('classes.npy')
#detector = MTCNN(min_face_size=15, steps_threshold=[0.6, 0.7, 0.7])


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


class AI:
    detector = MTCNN(min_face_size=30, steps_threshold=[0.8, 0.8, 0.5], scale_factor=0.6)
    facenet_model1 = load_model('models/model.h5')
    out_encoder = LabelEncoder()
    out_encoder.classes_ = np.load('models/classes.npy')


    def extract_mtcnn_result_from_photo(self, filename):
        pixels = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        results = self.detector.detect_faces(pixels)
        return results


    def extract_face_file_to_save(self, filename, results, required_size=(160, 160)):
        pixels = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
        #results to wynik metody detect_faces dla zdjęcia filename
        x1, y1, width, height = results[0]['box']
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        return image


    def extract_file_photo(self, filename):
        return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)


    def load_faces(self, directory):
        faces = list()
        file_names = list()
        for filename in sorted_aphanumeric(listdir(directory)):
            path = directory + filename
            face = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
            faces.append(face)
            file_names.append(filename)
        return faces, file_names


    def load_dataset(self, directory):
        X, y, file_names = list(), list(), list()
        for subdir in sorted_aphanumeric(listdir(directory)):
            path = directory + subdir + '/'
            if not isdir(path):
                continue
            faces, file_id = self.load_faces(path)
            labels = [subdir for _ in range(len(faces))]
            X.extend(faces)
            y.extend(labels)
            file_names.extend(file_id)
        X = asarray(X)
        y = asarray(y)
        z = asarray(file_names)
        return X, y, z


    def get_embedding(self, face_pixels):
        face_pixels = face_pixels.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        sample = expand_dims(face_pixels, axis=0)
        emb = self.facenet_model1.predict(sample)
        return emb[0]


    def get_db_emb(self):
        facesPhotos, labelsPhotos, photosNames = self.load_dataset('photos/')
        facesPhotosVectors = list()
        for face_pixels in facesPhotos:
            embedding = self.get_embedding(face_pixels)
            facesPhotosVectors.append(embedding)
        facesPhotosVectors = asarray(facesPhotosVectors)
        savez_compressed("gen_data/"+'photos_faces_emb.npz',
                         facesPhotosVectors, labelsPhotos, photosNames)
        tzd.save_time_tofile('vectors_time.txt')
        return facesPhotosVectors, labelsPhotos


    def train_svm(self):
        if tzd.read_time_from_file('gen_time/vectors_time.txt') == str(0):
            print("You cannot train a model without generating embeds")
            return
        data = np.load("gen_data/"+'photos_faces_emb.npz')
        facesPhotosVectors = data['arr_0']
        labels = data['arr_1']
        in_encoder = Normalizer(norm='l2')
        facesPhotosVectors = in_encoder.transform(facesPhotosVectors)
        self.out_encoder.fit(labels)
        np.save('models/classes.npy', self.out_encoder.classes_)
        labels = self.out_encoder.transform(labels)
        model = SVC(kernel='rbf', gamma=0.015, C=100, probability=True)
        model.fit(facesPhotosVectors, labels)
        with open('models/model_classifier.pkl', 'wb') as f:
            pickle.dump(model, f)
        tzd.save_time_tofile('svm_time.txt')


    def return_probability_from_distance(self, x):
        if x<0.03464:
            return 100
        elif x>1.7:
            return 0
        else:
            x = round(x, 5)
            data = np.load("gen_data/"+'kde_prob_file1.npz')
            indexy = data["arr_0"]
            proc_tak = data["arr_1"]
            index = np.where(indexy == x)[0][0]
            prob_in_proc = round(proc_tak[index], 2)
            return prob_in_proc


    def find_person_from_video(self, frame, mtcnn_results, required_size=(160, 160), position=0):
        model_deeplearning = self.facenet_model1
        import pickle
        with open('models/model_classifier.pkl', 'rb') as f:
            model_classifier = pickle.load(f)
        pixels = frame
        x1, y1, width, height = mtcnn_results[position]['box']
        if x1<0:
            x1=0
        if y1<0:
            y1=0
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        face_pixels = face_array.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        sample = expand_dims(face_pixels, axis=0)
        yhat = model_deeplearning.predict(sample)
        sample = expand_dims(yhat[0], axis=0)
        class_index = model_classifier.predict(sample)
        class_proba = model_classifier.predict_proba(sample)
        return int(class_index[0]), int(class_proba[0, class_index] * 100), class_proba


    def find_person_from_photo_and_extract_face2(self, file_path, mtcnn_results, required_size=(160, 160), position=0):
        model_deeplearning = self.facenet_model1
        import pickle
        with open('models/model_classifier.pkl', 'rb') as f:
            model_classifier = pickle.load(f)
        image = Image.open(file_path)
        image = image.convert('RGB')
        pixels = asarray(image)
        x1, y1, width, height = mtcnn_results[position]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        face_pixels = face_array.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        sample = expand_dims(face_pixels, axis=0)
        yhat = model_deeplearning.predict(sample)
        sample = expand_dims(yhat[0], axis=0)
        class_index = model_classifier.predict(sample)
        class_proba = model_classifier.predict_proba(sample)
        return int(class_index[0]), int(class_proba[0, class_index] * 100), face, class_proba


    def find_person_from_face_image_to_video_search\
                    (self, face_photo, required_size=(160, 160)):
        with open('models/model_classifier.pkl', 'rb') as f:
            model_svm = pickle.load(f)
        face_array_a = cv2.resize(face_photo, required_size)
        face_array = cv2.cvtColor(face_array_a, cv2.COLOR_BGR2RGB)
        sample = expand_dims(self.get_embedding(face_array), axis=0)
        class_proba = model_svm.predict_proba(sample)
        return class_proba


    def get_id_from_svm(self, index):
        return self.out_encoder.inverse_transform([index])

