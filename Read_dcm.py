import pydicom
import SimpleITK as sitk

import sys
import os
import argparse
from tqdm import tqdm
import datetime

import numpy as np
import cv2
from skimage import io
import warnings
warnings.filterwarnings("ignore")

def get_array(path):
    array_jpg, array_3ch = read_dicom(path)
    return array_jpg, array_3ch

def read_dicom(path):
    try:
        B = pydicom.dcmread(path)
        A = B.pixel_array
    except:
        reader = sitk.ReadImage(path)
        A = sitk.GetArrayViewFromImage(reader)[0]

    try:
        h, w = A.shape
    except:
        h, w, ch = A.shape

    if A.max() > 255:
        arreglo = np.copy(A)
        img_gry = (((A - A.min())/(A.max() - A.min() + sys.float_info.epsilon))*255).astype('uint8')
    else:
        arreglo = A
        img_gry = A

    return arreglo, img_gry.astype('uint8')

def reshape(image):
    h,w = image.shape
    if args.wh:
        new_image = cv2.resize(image, (args.wh, args.wh))
    else:
        new_width = args.width if args.width is not None else w
        new_height = args.height if args.height is not None else h
        new_image = cv2.resize(image, (new_width, new_height))
    return new_image

def main():
    Files = []
    for root, dirs, files in os.walk(args.data):
        for file in files:
            path = os.path.join(root, file)
            if path[-4::] == '.dcm' or path[-4::] == '.DCM':
                Files.append(path)
    print("Found", len(Files), "files")

    path_images = "Images"
    try:
        os.makedirs(path_images)
        print("Saving images on", path_images + "/")
    except:
        print("Saving images on", path_images + "/")

    for name in tqdm(Files[0:15]):
        _, I = read_dicom(name)
        path_save = name.split('\\')[-1]
        seg_name = ""
        for sub_name in path_save.split(".")[0:-1]:
            seg_name += sub_name + "."

        if args.width or args.height or args.wh:
            I = reshape(I)

        io.imsave(os.path.join(path_images, seg_name + 'tif'), I, check_contrast=False)

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='.', help='Path to dcm files')
parser.add_argument('--width', type=int, default=None, help='Reshape to new width')
parser.add_argument('--height', type=int, default=None, help='Reshape to new height')
parser.add_argument('--wh', type=int, default=None, help='Reshape to new image with height and width equal to wh')

args = parser.parse_args()

if args.wh:
    args.width, args.height = None, None

main()
print('TERMINADO')
