import sys
import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import glob
#----------------------
import subprocess

import os

import torch
from IPython.display import Image, clear_output  # to display images

clear_output()
print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

#-----------------------


#===========
st.header("Crater recognition")
st.write('---')

STYLE = """
<style>

img { 
    max-width: 100%;
}
</style>
"""


from PIL import Image
#@st.cache
def load_image(image_file):
     img=Image.open(image_file)
     return img

def main():
    st.markdown (STYLE, unsafe_allow_html=True)
    image_file=st.file_uploader("Upload your File", type=["png","jpg"])

    if image_file is not None:
       #st.write(type(file))
       #st.write(dir(file))
       st.image(load_image(image_file))
       filename=image_file.name
       st.write(filename)       


       with open(filename, 'wb') as f:
           f.write(image_file.getbuffer())
       st.success("File saved")

       st.write('---')
       st.subheader("The prediction")
       os.system(f"python detect.py --weights best.pt --img 640 --conf 0.25 --source {filename}")
       st.success("Prediction is done")
   
       
       from pathlib import Path
       FILE = Path(__file__).resolve()
       ROOT = FILE.parents[0]                          # the root directory
       if str(ROOT) not in sys.path:
           sys.path.append(str(ROOT))                  # add ROOT to PATH
       ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

       project=ROOT / 'runs/detect'  # save results to project/name
       name='exp'                    # save results to project/name
       path=Path(project) / name
       path = Path(path)
       save_dir =sorted(glob.glob(f"{path}*"))[-1] # increment with eachrun
       st.write(save_dir) 



       # show prediction
       st.image(f'{save_dir}/{filename}')

main()

