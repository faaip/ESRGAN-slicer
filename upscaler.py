import os.path as osp
import os
import argparse
import sys
import glob
import cv2
import numpy as np
import torch
from tqdm import tqdm
import RRDBNet_arch as arch
import tkinter as tk
from tkinter import filedialog
from gdown import download

model_path = 'models/RRDB_ESRGAN_x4.pth'
if torch.cuda.is_available():
    print('Yay, CUDA is available!')
    device = torch.device('cuda')
else:
    print('No CUDA detected, running on CPU.')
    device = torch.device('cpu')

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
try:
    model.load_state_dict(torch.load(model_path), strict=True)
except FileNotFoundError as e:
    print('Model not found, downloading:')
    cmd = 'gdown https://drive.google.com/uc?id=1TPrz5QKd8DHHt1k8SRtm6tMiPjz_Qene -O ./models/RRDB_ESRGAN_x4.pth'
    os.system(cmd)
    print('Model downloaded')

model.eval()
model = model.to(device)


def upscale(img):
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(
        img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze(
        ).float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    return output


def slice(img, slice_size=600):
    out_img = np.zeros([img.shape[0]*4, img.shape[1]*4, img.shape[2]])
    print(range(0, img.shape[0], slice_size))
    for r in tqdm(range(0, img.shape[0], slice_size)):
        for c in range(0, img.shape[1], slice_size):
            upscaled_img = upscale(img[r:r+slice_size, c:c+slice_size, :])
            out_img[r*4:r*4+upscaled_img.shape[0], c*4:c *
                    4+upscaled_img.shape[1], :] = upscaled_img
    print('Upscaled sliced stitched together, done!')
    return out_img


def file_is_valid(file):
    if not os.path.exists(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return open(file, 'r')  # return an open file handle


def upscale_file(file_path, output_path):
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    out = slice(img)
    cv2.imwrite(output_path, out)


def isImage(file):
    return file.endswith(".png") or file.endswith(".jpeg")


def upscale_directory(input_dir, output_dir):
    print('Upscaling all files in directory')
    for file in tqdm(list(filter(lambda x: isImage, os.listdir(infile)))):
        filename = os.fsdecode(file)
        if filename.endswith(".png") or filename.endswith(".jpeg"):
            input_name = os.path.join(input_dir, filename)
            output_name = os.path.join(output_dir, filename)
            upscale_file(input_name,output_name)


parser = argparse.ArgumentParser(description='Upscale input file')

# add the argument
parser.add_argument('-i', '--input', dest='infile',   required=True,
                    metavar='INPUT_FILE', help='The image or directory of images to be upscaled')
parser.add_argument('-o', '--output', dest='outfile',  required=True,
                    metavar='OUTPUT_FILE', help='The upscaled image or output directory')

# parse and assign to the variable
args = parser.parse_args()
infile = args.infile
outfile = args.outfile

if os.path.isdir(infile):
    try:
        os.path.file(outfile)
    except AttributeError as e:
        print('ERROR: Output has to be a directory when input is a dir')
        # upscale_directory(infile, outfile)

    upscale_directory(infile, outfile)
elif os.path.isfile(infile):
    print("\nIt is a normal file")

# upscale_file(args.infile, args.outfile)
