from PIL import Image
import numpy as np
import sys
import os
from scipy import ndimage
print("###Starting###")

directory = sys.argv[1]
out_dir = sys.argv[2]
attack_type = sys.argv[3]
param = int(sys.argv[4])

def main():
	for filename in os.listdir(directory):
		if filename.endswith('.jpg'):
			img = Image.open(directory+'/'+filename)
			print filename
			img_arr = np.array(np.array(img), dtype= np.uint32)
			mask = np.ones(img_arr.shape)
			# INSERT ATTACKS HERE
			if attack_type == "brightening":
				img_arr = np.add(img_arr, mask * param)
			elif attack_type == "gaussian":
				noise_old = np.random.normal(0.0, param, img_arr.shape)
				# noise_old[mask == 0] = 0
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