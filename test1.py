import tensorflow as tf
import mobile_linknet as ml
from matplotlib import pyplot as plt

dataset = ml.load_dataset("images/train/",["images/cells/","images/nuclei/"], ["msc_1.jpg","fib1_1.jpg"],(96*4,96*3))

augmented = dataset.repeat(4).map(ml.augment).shuffle(8).batch(2)

model = ml.Mobile_LinkNet_SAM()

train_callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="loss", patience=15,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="loss", factor=0.75,
        patience=7, verbose=1
    )
]

model.compile(optimizer="adam",loss=ml.metrics.IoU_focal,metrics=[ml.metrics.accuracy, ml.metrics.precision, ml.metrics.recall])
model.fit(augmented, epochs=5)

model.save("saved_model.h5")

