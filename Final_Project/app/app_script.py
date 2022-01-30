import sys
import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import glob
import os
import torch
from IPython.display import Image, clear_output  # to display images
clear_output()
from PIL import Image

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def mpage(model,Htxt,yolo_model,CSVF='yolov5s_1500_results.csv'):
    """
    To choose the display options.
    """
    st.title(model)
    name=['Model information','Model training results']
    page=st.radio('', name)
    if page=='Model training results':
        st.header("Metrics of the training runs")
        st.subheader("Table")
        st.write('A sample of the metrics logging of the training runs')
        df = pd.read_csv('csv_files/'+CSVF)#'yolov5s_1500_results.csv')
        df.columns = [c.replace(' ', '') for c in df.columns]   # This removes the spaces in the column names.
        df_sample = df.sample(5)
        st.dataframe(df_sample)
        #st.download_button('Download the Full CSV file', text_contents, 'vsc_files/yolov5s_1500_results.cvs')

        st.write('---')
        st.subheader("Plots")
        fig, axes = plt.subplots(2,2, sharex=True,figsize=(10,8))
        sns.scatterplot(ax=axes[0,0],data=df,x='epoch',y='metrics/precision', color='red')
        axes[0,0].set_ylabel('Precision')
        sns.scatterplot(ax=axes[0,1],data=df,x='epoch',y='metrics/recall')
        axes[0,1].set_ylabel('Recall')
        sns.scatterplot(ax=axes[1,0],data=df,x='epoch',y='metrics/mAP_0.5', color='green')
        axes[1,0].set_ylabel('mAP_0.5')
        sns.scatterplot(ax=axes[1,1],data=df,x='epoch',y='metrics/mAP_0.5:0.95', color='orange')
        axes[1,1].set_ylabel('mAP_0.5:0.95')        
        st.pyplot(fig)


    if page=='Model information':
        st.write(Htxt)
        st.image(yolo_model)


#=======================
st.header("Space Craters Detector")
st.write('---')
STYLE = """
<style>

img { 
    max-width: 100%;
}
</style>
"""
#=======================
options = st.sidebar.selectbox('Show me some option',("Moon","Mars"))
model_options=st.sidebar.selectbox('Models to choose',("Model 1","Model 2", "Model 3"))

if options == 'Moon':
    st.title(options)
    st.write("Here you will make detection of craters with lunar surface images using **Yolov5** ")
    st.markdown("""[`Link to Yolov5 repository`](https://github.com/ultralytics/yolov5)""")

    st.image('moon.jpg', width=400)

    if model_options == "Model 1":
       Htxt="The pretrained model **Yolov5s** is used to start training. The model uses **5 images** and **1500 epochs** train."
       yolo_model='yolov5s.jpg'
       mpage(model_options,Htxt,yolo_model,'yolov5s_1500_results.csv') # The mage for model 1

    elif model_options == "Model 2":
       Htxt="The pretrained model **Yolov5s** is used to start training. The model uses **39 images** and **1000 epochs** to train."
       yolo_model='yolov5s.jpg'
       mpage(model_options,Htxt,yolo_model,'yolov5s_1000_results.csv') # The mage for model 2
    elif model_options == "Model 3":
       Htxt="The pretrained model **Yolov5m** is used to start training. The model uses **39 images** and **200 epochs** to train."
       yolo_model='yolov5m.jpg'
       mpage(model_options,Htxt,yolo_model,'yolov5m_200_results.csv')  # The mage for model 1
    else:
        st.write('The Moon has a large number of craters ...')
        
#======================
# To see the load image
    def load_image(image_file):
        img=Image.open(image_file)
        return img

    def main():
        st.markdown (STYLE, unsafe_allow_html=True)
        image_file=st.file_uploader("Upload your file here", type=["png","jpg","mp4"])
        
        if image_file is not None:
           st.write(image_file)
           filename=image_file.name
           with open(filename, 'wb') as f:    # to save the load image
               f.write(image_file.getbuffer())
           if image_file.type!="video/mp4":    
             st.image(load_image(image_file))
             st.write(filename)   
           elif image_file.type=="video/mp4":
             video1=open(image_file.name,'rb').read()
             st.video(video1)
             st.write(image_file.name)
           
#===================================================================================================
           st.write('---')
           st.subheader("The detections")

           # to predict using the model
           if model_options == 'Model 1':
               os.system(f"python detect.py --weights weights/best_v5s_1500.pt --img 640 --conf 0.25 --source {filename} --name m1exp") 
               name='m1exp'   

           elif model_options == 'Model 2':
               os.system(f"python detect.py --weights weights/best_v5s_1000.pt --img 640 --conf 0.25 --source {filename} --name m2exp") 
               name='m2exp'

           elif model_options == 'Model 3':
               os.system(f"python detect.py --weights weights/best_v5m_200.pt --img 640 --conf 0.25 --source {filename} --name m3exp") 
               name='m3exp'

           # the path where results are save
           from pathlib import Path
           FILE = Path(__file__).resolve()
           ROOT = FILE.parents[0]                          # the root directory
           if str(ROOT) not in sys.path:
               sys.path.append(str(ROOT))                  # add ROOT to PATH
           ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
           project=ROOT / 'runs/detect'  # same path as the model save the results
                    
           path=Path(project) / name
           path = Path(path)
           save_dir =sorted(glob.glob(f"{path}*"), key=os.path.getmtime)[-1] # increment with each run
           st.write(save_dir) 

           # show prediction
           if image_file.type!="video/mp4":    
             st.image(f'{save_dir}/{filename}')  
           elif image_file.type=="video/mp4":
             os.system(f"ffmpeg -i {save_dir}/{filename} -vcodec libx264 {save_dir}/reformat.mp4")
             video2=open(f'{save_dir}/reformat.mp4','rb').read()
             st.video(video2)
           st.warning('If you prediction is not good, try the other models')
               
    main()

elif options == "Mars":

    st.title(options)
