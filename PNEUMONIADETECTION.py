# Convolutional Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
"""here we are filtering an input image using 32 (3*3) feature detector. Here we are using 
input images which are colored images so we are using 3 in input shape arguments and dimension
 of images as 64*64 because we are working on CPU and don't want to waste more time on our code
 to execute"""
#You can use dimensions of input images accordingly like 128*128 or 256*256 if you have higher system configurations but I recommend you to use 64*64 dimension if you are working on CPU
classifier.add(Convolution2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer, we can also add third cnn layer with 64 filters instead of 32 for more accuracy
classifier.add(Convolution2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator
#Image Augmentation Part
train_datagen = ImageDataGenerator(rescale = 1./255,           #rescaling pixel value between 0 & 1
                                   shear_range = 0.2,   
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255) #rescaling the pixel value of test set between  0 & 1 

training_set = train_datagen.flow_from_directory('chest_xray/train',    #training of CNN
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('chest_xray/test',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

classifier.fit_generator(training_set,                  
                         steps_per_epoch = (5216/32),
                         epochs = 25,
                         validation_data = test_set,
                         validation_steps = (624/32))   #images in our test set


# Part 3 - Making new predictions
import numpy as np
from keras.preprocessing import image
test_image = image.load_img('chest_xray/val/PNEUMONIA/person1946_bacteria_4874.jpeg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices
if result[0][0] == 1:
    prediction = 'Pneumonia'
else:
    prediction = 'Normal'
