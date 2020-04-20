import os.path as osp
import os
from argparse import ArgumentParser
import sys
import glob
import cv2
import numpy as np
import torch
from tqdm import tqdm
import RRDBNet_arch as arch
import tkinter as tk
from tkinter import filedialog

model_path = 'models/RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)

def upscale(img):
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    return output


def slice(img, slice_size=600):
    print('Slicing image...')
    out_img = np.zeros([img.shape[0]*4, img.shape[1]*4, img.shape[2]])
    print(range(0,img.shape[0],slice_size))
    for r in tqdm(range(0, img.shape[0], slice_size)):
        for c in range(0, img.shape[1], slice_size):
            upscaled_img = upscale(img[r:r+slice_size, c:c+slice_size, :])
            out_img[r*4:r*4+upscaled_img.shape[0], c*4:c*4+upscaled_img.shape[1], :] = upscaled_img
    print('Upscaled sliced stitched together, done!')
    return out_img

def file_is_valid(file):
    if not os.path.exists(file):
        parser.error("The file %s does not exist!" % file)
    else:
        return open(file, 'r')  # return an open file handle

def upscale_file(file_path):
    img = cv2.imread(file_path, cv2.IMREAD_COLOR)
    out = slice(img)
    cv2.imwrite('out.png', out)