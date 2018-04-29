from PIL import Image
import numpy as np
import sys
import os
from scipy import ndimage
print("###Starting###")

directory = sys.argv[1]
out_dir = sys.argv[2]
category = int(sys.argv[3])
attack_type = sys.argv[4]
param = int(sys.argv[5])
param2 = None
if len(sys.argv) > 6:
	param2 = int(sys.argv[6])

def main():
	for filename in os.listdir(directory):
		if filename.endswith('.jpg'):
			num = category

			obj = Image.open(directory+'/'+filename[:-4]+'_object.png')
			img = Image.open(directory+'/'+filename)
			#obj = Image.open(directory+'/ADE_train_00018094_object.png')
			#img = Image.open(directory+'/ADE_train_00018094.jpg')
			obj_arr = np.array(obj)[:,:,0]

			if num in obj_arr:
				print filename
				mask = np.zeros(obj_arr.shape)
				mask[obj_arr == num] = 1
				
				mask = mask.repeat(2, axis=0).repeat(2, axis=1)
				mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
				if param2 != None:
					mask = ndimage.binary_dilation(mask, iterations=param2).astype(mask.dtype)
				img_arr = np.array(np.array(img), dtype= np.uint32)
				# INSERT ATTACKS HERE
				if attack_type == "brightening":
					img_arr = np.add(img_arr, mask * param)
				elif attack_type == "gaussian":
					noise_old = np.random.normal(0.0, param, img_arr.shape)
					noise_old[mask == 0] = 0
					noise = np.array(noise_old, dtype = np.float32)
					img_arr = np.add(img_arr, noise)

				
				img_arr[img_arr>255] = 255
				img_arr[img_arr<0] = 0
				img_arr = np.array(img_arr, dtype = np.uint8)

				mod_img = Image.fromarray(img_arr)
				# mod_img.show()
				mod_img.save(out_dir+"/"+filename, "JPEG")


if __name__ == "__main__":
	main()