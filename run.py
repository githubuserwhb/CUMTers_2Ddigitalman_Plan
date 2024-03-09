import cv2
from source.cartoonize import Cartoonizer
import os
import numpy as np
import gradio as gr


def get_model_list(model_dir):
    list_models = []
    m_dirs = os.listdir(model_dir)
    for dir in m_dirs:
        path_model = os.path.join(model_dir,dir)
        list_models.append(path_model)
    return list_models


def style(operation):
    if operation == "画风":
        return 1
    elif operation == "动画":
        return 2
    elif operation == "素描":
        return 3
    elif operation == "漫画":
        return 4
    elif operation == "3d":
        return 0
def process_image1(choice,model):
    model_index=style(model)
    list_models = get_model_list("models")
    algo = Cartoonizer(list_models[model_index])
    if choice=="image1":
        img = cv2.imread("image1.jpg")[..., ::-1]    #imread()读的需要是图像的路径
    elif choice == "image2":
        img = cv2.imread("image2.jpg")[..., ::-1]  # imread()读的需要是图像的路径
    result = algo.cartoonize(img)
    result_mid = np.array(result, dtype=np.uint8)
    #file_img_out = os.path.split(list_models[model_index])[-1]+"_out_"+"input.jpg"   #输出一个新的文件名
    #cv2.imwrite(file_img_out,result_mid)    #文件处理路径和图像保存
    result_out = cv2.cvtColor(result_mid, cv2.COLOR_BGR2RGB)  # 将结果转换回RGB格式
    return result_out

def process_image2(image,model):
    model_index=style(model)
    list_models = get_model_list("models")
    algo = Cartoonizer(list_models[model_index])
    img = cv2.imread(image)[..., ::-1]  # imread()读的需要是图像的路径
    result = algo.cartoonize(img)
    result_mid = np.array(result, dtype=np.uint8)
    result_out = cv2.cvtColor(result_mid, cv2.COLOR_BGR2RGB)  # 将结果转换回RGB格式
    return result_out

with gr.Blocks() as demo:
    with gr.Tab("Passive"):
        gr.Interface(fn=process_image1,
            inputs=[
                gr.Radio(["image1", "image2"]),
                gr.Radio(["3d","画风", "动画", "素描", "漫画"])
                ],
            outputs=gr.Image(label="Cartoonized Image")
                           )
    with gr.Tab("active"):
        gr.Interface(fn=process_image2,
            inputs=[
                gr.Image(label="Image",type="filepath"),
                gr.Radio(["3d","画风", "动画", "素描", "漫画"])
                ],
            outputs=gr.Image(label="Cartoonized Image")
                           )

demo.launch()
#demo.launch(share=True)

