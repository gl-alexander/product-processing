import numpy as np
from rembg import remove
import cv2
import os

input_path = 'IMG_1808.JPG'

border_path = 'output/transparentBG.png'
border_path2 = 'output/whiteBG.png'

directory_path = 'C:\\Users\\user\\Desktop\\Products\\Bottles'

output_path = 'C:\\Users\\user\\Desktop\\output_folder'

#dimnesions of output images
DEST_WIDTH = 1536
DEST_HEIGHT = 1536
SIZE_OF_CONTENT = 1400

#alpha value threshold
TRANSPARENCY_FILTER = 95


def crop(img):
    x, y, w, h = cv2.boundingRect(img[..., 3])
    im2 = img[y:y+h, x:x+w, :]
    im2 = cv2.rotate(im2, cv2.ROTATE_90_CLOCKWISE)

    return im2


def scale(img):
    height = img.shape[0]
    width = img.shape[1] 
    orientation = max(height, width)
    scale_factor = SIZE_OF_CONTENT / orientation
    
    scaled_f_down = cv2.resize(img, None, fx= scale_factor, fy= scale_factor, interpolation= cv2.INTER_LINEAR)
    return scaled_f_down
    


def pasteOnCanvas(img):
    height = img.shape[0]
    width = img.shape[1]
    
    canvas = np.zeros((DEST_HEIGHT, DEST_WIDTH, 4), dtype=np.uint8)
    
    y_offset = int((DEST_HEIGHT - height) / 2)
    x_offset = int((DEST_WIDTH - width) / 2)
    canvas[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
    return canvas


def whiteBackground(img):
    trans_mask = img[:,:,3] <= TRANSPARENCY_FILTER
    img[trans_mask] = [255, 255, 255, 255]
    return img


def process_image(img_path, white_bg_path, clear_bg_path):
    target_folder_t = '/'.join(clear_bg_path.split("\\")[:-1])
    target_folder_w = '/'.join(white_bg_path.split("\\")[:-1])
    
    original = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    im = remove(original, alpha_matting=False)
    
    cropped = crop(im)
    scaled = scale(cropped)
    clear_bg = pasteOnCanvas(scaled)
    #creates the directory through the os library
    if(not os.path.exists(target_folder_t)):
        os.makedirs(target_folder_t)
    cv2.imwrite(clear_bg_path, clear_bg)
    white_bg = whiteBackground(clear_bg)
    if(not os.path.exists(target_folder_w)):
        os.makedirs(target_folder_w)
    cv2.imwrite(white_bg_path, white_bg)
    



for subdir, dirs, files in os.walk(directory_path):
    item_id = subdir.split("\\")[-1]
    print("Processing folder " + item_id)
    for i in range(0, len(files)):
        img_path = os.path.join(subdir, files[i])
        clear_path = os.path.join(str(output_path), item_id, item_id+'-transparent', str(i+1) + '.PNG')
        white_path = os.path.join(str(output_path), item_id, item_id+'-white', str(i+1) + '.PNG')
        
        
        process_image(img_path, white_path, clear_path)
        
        #print(img_path)
        
        



#img.save(output_path)
