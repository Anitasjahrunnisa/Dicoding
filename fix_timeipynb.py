# -*- coding: utf-8 -*-
"""FIX-timeipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C2FsmnJ9q-yDkfEQz0mS0QYgUBOy-gyA
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Bidirectional,Dropout
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import LSTM,Dense,Embedding,Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/My Drive/Colab Notebooks/PJME_hourly.csv")
data.index+=1
data.head()

display(data.tail())

data.isnull().sum()

plot = data
plot[plot.columns.to_list()].plot(subplots=True, figsize=(15, 10))
plt.show()

from sklearn.preprocessing import MinMaxScaler
tuj= ['PJME_MW']
scale = MinMaxScaler()
data[tuj] = scale.fit_transform(data[tuj])

date = data['Datetime'].values
label = data['PJME_MW'].values

plot = data
plot[plot.columns.to_list()].plot(subplots=True, figsize=(15, 10))
plt.show()

#plt.figure(figsize=(15,5))
#plt.plot(date,label)
#plt.title('Hourly Energy Consumption', fontsize = 20)
#plt.ylabel('PJME_MW')
#plt.xlabel('Datetime')

x_train, x_test, y_train, y_test = train_test_split(label, date, train_size=0.8, test_size = 0.2)
print('Jumlah Data Train : ',len(x_train))
print('Jumlah Data Validation : ',len(x_test))

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
  series = tf.expand_dims(series, axis=-1)
  ds = tf.data.Dataset.from_tensor_slices(series)
  ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
  ds = ds.flat_map(lambda w: w.batch(window_size + 1))
  ds = ds.shuffle(shuffle_buffer)
  ds = ds.map(lambda w: (w[:-1], w[-1:]))
  return ds.batch(batch_size).prefetch(1)

train_set = windowed_dataset(x_train, window_size=60, batch_size=100, shuffle_buffer=1000)
model = tf.keras.models.Sequential([
  tf.keras.layers.LSTM(60, return_sequences=True),
  tf.keras.layers.LSTM(60),
  tf.keras.layers.Dense(30, activation="relu"),
  tf.keras.layers.Dense(10, activation="relu"),
  tf.keras.layers.Dense(1),
  ])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('mae')< 0.1):
      print("\nMAE dari model < 10% ")
      self.model.stop_training = True
callbacks = myCallback()

optimizer = tf.keras.optimizers.SGD(learning_rate=1.0000e-04, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])
history = model.fit(train_set,epochs=30,callbacks=[callbacks])

# MAE
plt.plot(history.history['mae'])
plt.title('MAE')
plt.ylabel('mae')
plt.xlabel('epoch')
plt.show()

# Plot Loss
plt.plot(history.history['loss'])
plt.title('Loss ')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()
