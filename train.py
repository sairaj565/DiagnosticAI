import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

DATASET_PATH = "dataset"

# ======================
# DATA GENERATORS (ALIGNED MOBILE-NET PREPROCESSING)
# ======================
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.3,
    shear_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8,1.2]
)

val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

train = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=8,
    class_mode='binary',
    subset='training',
    seed=42
)

val = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=8,
    class_mode='binary',
    subset='validation',
    seed=42,
    shuffle=False
)

# ======================
# TRANSFER LEARNING ⭐⭐⭐
# ======================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ======================
# TRAIN
# ======================
history = model.fit(
    train,
    validation_data=val,
    epochs=15
)

model.save("lung_cancer_model.h5", include_optimizer=False)

print("[OK] Improved Model Saved")