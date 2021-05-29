from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model


model = load_model('mixed_model.h5')
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])


def prediction_result():
    valid_datagen = ImageDataGenerator(rescale=1./255)
    valid_set = valid_datagen.flow_from_directory("./test",
                                                  target_size=(224, 224),
                                                  batch_size=128,
                                                  class_mode='categorical'
                                                  )
    prediction = model.predict(valid_set)
    list_of_all_categories = ['Apple___Apple_scab',
                              'Apple___Black_rot',
                              'Apple___Cedar_apple_rust',
                              'Apple___healthy',
                              'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                              'Corn_(maize)___Common_rust_',
                              'Corn_(maize)___Northern_Leaf_Blight',
                              'Corn_(maize)___healthy']
    prediction_array = []
    for i in prediction:
        max_prob = max(i)
        for j in range(8):
            if i[j] == max_prob:
                prediction_array.append(list_of_all_categories[j])
    return prediction_array
