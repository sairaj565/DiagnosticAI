import tensorflow as tf
model = tf.keras.models.load_model("lung_cancer_model.h5", compile=False)
for layer in model.layers:
    if hasattr(layer, 'output_shape'):
        print(f"{layer.name:45s} {str(layer.output_shape)}")