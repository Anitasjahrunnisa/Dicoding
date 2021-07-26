# -*- coding: utf-8 -*-
"""Last

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GMmkxnnb369Rl86SFJO3N2LndNySTBWy
"""

import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os, shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

!wget --no-check-certificate \
https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip\
  -O rockpaperscissors.zip

import zipfile,os
zip = 'rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(zip, 'r')
zip_ref.extractall('rps')
zip_ref.close()

!pip install split_folders

import splitfolders
splitfolders.ratio('rps/rockpaperscissors/rps-cv-images', 'rps/rockpaperscissors/data', seed=1337, ratio=(.8, .2))

db = 'rps/rockpaperscissors/data'
db_train = os.path.join(db, 'train')
db_test = os.path.join(db, 'val')
os.listdir('rps/rockpaperscissors/data/train')
os.listdir('rps/rockpaperscissors/data/val')

tbatu = os.path.join(db_train, 'rock')
tgunting = os.path.join(db_train, 'scissors')
tkertas = os.path.join(db_train, 'paper')
vbatu = os.path.join(db_test, 'rock')
vgunting = os.path.join(db_test, 'scissors')
vkertas = os.path.join(db_test, 'paper')

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
  rescale=1./255, 
  shear_range=0.2, 
  zoom_range=0.2, 
  horizontal_flip=True) 

test_datagen = ImageDataGenerator(
  rescale=1./255, 
  shear_range=0.2, 
  zoom_range=0.2, 
  horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    db_train, 
    target_size=(224, 224),
    batch_size=32, 
    color_mode='rgb', 
    class_mode='categorical',  
    shuffle = True, 
    seed=42) 
validation_generator = test_datagen.flow_from_directory(
    db_test,
    target_size=(224, 224),
    batch_size=32,
    color_mode='rgb',
    class_mode='categorical',
    shuffle = True,
    seed=42)

sample_train_images, _ = next(train_generator)
sample_val_images, _ = next(test_generator)

fbatu = os.listdir(tbatu)
fgunting = os.listdir(tgunting)
fkertas = os.listdir(tkertas)

pic_index = 2

batu2 = [os.path.join(tbatu, fname) 
                for fname in fbatu[pic_index-2:pic_index]]
gunting2 = [os.path.join(tgunting, fname) 
                for fname in fgunting[pic_index-2:pic_index]]
kertas2 = [os.path.join(tkertas, fname) 
                for fname in fkertas[pic_index-2:pic_index]]

for i, img_path in enumerate(batu2+gunting2+kertas2):
    fig, axes = plt.subplots(figsize=(3,3))
    img = mpimg.imread(img_path)
    plt.imshow(img)
    plt.axis('Off')
    plt.show()

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

# Callback stop pas akurasi lebih dr 85%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.85):
      print("\nAkurasi diatas 85 Maka Training Berhenti")
      self.model.stop_training = True

callbacks = myCallback()

history = model.fit(
    train_generator,
    steps_per_epoch = 20,
    epochs = 30,
    validation_data = validation_generator,
    validation_steps = 5,
    verbose =2,
    callbacks=[callbacks]
)

import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']
#AKURASI
plt.plot(acc, color='blue')
plt.plot(val_acc, color='red')
plt.title('AKURASI')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
#LOSS
plt.plot(loss, color='blue')
plt.plot(val_loss, color='red')
plt.title('LOSS')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for ab in uploaded.keys():
 
  # predicting images
  path = ab
  img = image.load_img(path, target_size=(224,224))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=32)

  if classes[0,0]!=0:
    print('PAPER')
  elif classes[0,1]!=0:
    print('ROCK')
  else:
    print('SCISSORS')

model22 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model22.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

# Callback stop pas akurasi lebih dr 85%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.85):
      print("\nAkurasi ke 2 diatas 85 Maka Training Berhenti")
      self.model.stop_training = True

callbacks = myCallback()

history = model22.fit(
    train_generator,
    steps_per_epoch = 20,
    epochs = 30,
    validation_data = validation_generator,
    validation_steps = 5,
    verbose =2,
    callbacks=[callbacks]
)

import warnings
warnings.filterwarnings('ignore')
converts = tf.lite.TFLiteConverter.from_keras_model(model)
tflite = converts.convert()

# Save the model.
with open('Suit.tflite', 'wb') as f:
  f.write(tflite)

!ls -la | grep 'Suit'

"""
Nama: Anita Sjahrunnisa , Username: arisa98 , Email: arisanita98@gmail.com """