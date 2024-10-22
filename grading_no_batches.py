import torch
from transformers import AutoModelForCausalLM
from PIL import Image
import os
from tqdm import tqdm
import pandas as pd
import argparse

model_path = f"{os.getcwd()}/model/models--q-future--one-align/snapshots/dcc603b95aa0ebd82afa696d4a1e20d11fc80ddb"
old_path= "q-future/one-align"
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, attn_implementation="eager", 
                                             torch_dtype=torch.float16, device_map="auto")
parser = argparse.ArgumentParser(description='Grade frames from a provided dir.')
parser.add_argument('--img_dataset', type=str, required=True, help='location of the images')
parser.add_argument('--particular_film', type=bool, required=False, default= False, help='one particular film or are there multiple direcrories')
parser.add_argument('--task_type', type=str, default='aesthetics', help='Task type for grading (aesthjetics or quality)')

args = parser.parse_args()

dir_name = args.img_dataset
if args.particular_film:
    look_through = [dir_name]
else:
    look_through = os.listdir(dir_name)

for subdir in look_through:
    subdir_path = os.path.join(dir_name, subdir)
    subdir_name = subdir.split("/")[-1]
    print(f"working on {subdir_name}")
    if os.path.isdir(subdir_path):
        
        image_paths = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith(".jpg")]
        images = [(f, Image.open(f)) for f in image_paths]
        images = [(filename, img.resize((256, int(256 * img.height / img.width))) if img.width > img.height else img.resize((int(256 * img.width / img.height), 256))) for filename, img in images]
        images = [(filename, img) for filename, img in images if img.mode == "RGB"]
        # Filtering out every second image to reduce load on the GPU
        images = images[::2]
        task = args.task_type
        print(f"grading {task}")
        scores = {}
        for filename, image in tqdm(images):
             scores[filename] = model.score([image], task_=task, input_="image")  
        scores = {k: v.item() for k, v in scores.items()}
        df = pd.DataFrame(scores, index=[0]).T
        os.makedirs(f'Data/grades/{subdir_name}', exist_ok=True)
        df.to_csv(f"Data/grades/{subdir_name}/{task}.csv")
