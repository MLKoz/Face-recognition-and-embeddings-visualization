# Face-recognition-and-embeddings-visualization

The project allows you to create a database of photos of people with their personal data, and then detect these people in photos, videos and camera images.\ 
There are built-in methods for determining the similarity of faces in photos outside the database.\ 
It is possible to visualize in 2D and 3D face embedding in the database using the t-SNE, PCA and UMAP algorithms.

#Technologies:  \
PyQt5 - the interface. \
SQLite - the database\
Pillow - working with image (loading, reshaping, etc.)\
OpenCV - working with camera and videos\
Keras and Tensorflow - working with deep learning models\
Numpy - to flow the data between pillow-opencv-keras-sklearn-matplotlib etc.\
MTCNN - the library used to detect faces working with images and videos (its frames)\
UMAP-Learn - used to visualizations 2D and 3D \
KDEpy - to use kernel density estimation in order to compare face embeddings without using the SVM model built on the database\
Scikit-Learn - making SVM model on face embeddings and using PCA and t-SNE to 2D and 3D visualizations, and metrices like accuracy etc.\
SciPy - to calculate the Euclidean distance between face embeddings\
Matplotlib - used to visualizations\

In order to generate the face embeddings I used the FaceNet model:\
https://arxiv.org/abs/1503.03832

