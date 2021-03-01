import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

ConvModelPath = "./models/model_conv.tflite"
DanseModelPath = "./models/model_danse.tflite"

map_characters =["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def resolve(filename):
    interpreter = tf.lite.Interpreter(model_path=ConvModelPath)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = image.load_img(filename, target_size=(28, 28, 1), color_mode = "grayscale")

    x = image.img_to_array(img)
    # Меняем форму массива в плоский вектор
    x = x.reshape(1, 28, 28, 1)
    # Инвертируем изображение, нам надо белое на чёрном фоне
    x = 255 - x
    # Нормализуем изображение
    x /= 255

    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    y_pred_ids = output_data[0].argsort()[-1:][::-1]
    result = ""
    for i in range(len(y_pred_ids)):
        result = result + "\n\t" + map_characters[y_pred_ids[i]] + " (" + str(round(output_data[0][y_pred_ids[i]]*100, 5)) +"%" + ")"
    print("")
    print(result)
    return result
