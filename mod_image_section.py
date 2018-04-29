from PIL import Image
import numpy as np
import sys
import os
print("###Starting###")

directory = sys.argv[1]
out_dir = sys.argv[2]
attack_type = sys.argv[3]
param = int(sys.argv[4])
category = int(sys.argv[5])


def main():
	for filename in os.listdir(directory):
		if filename.endswith('.jpg'):
			print()
			num = category

			obj = Image.open(directory+'/'+filename[:-4]+'_object.png')
			img = Image.open(directory+'/'+filename)
			#obj = Image.open(directory+'/ADE_train_00018094_object.png')
			#img = Image.open(directory+'/ADE_train_00018094.jpg')
			obj_arr = np.array(obj)[:,:,0]

			if num in obj_arr:
				print filename
				mask = np.zeros(obj_arr.shape)
				# obj_arr[obj_arr != num] = 0
				mask[obj_arr == num] = 1
				
				#print obj_arr.shape
				mask = mask.repeat(2, axis=0).repeat(2, axis=1)
				mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
				#print obj_arr.shape

				img_arr = np.array(np.array(img), dtype= np.uint32)
				print img_arr.dtype
				if attack_type == "brightening":
					# print np.unique(obj_arr.flatten())

					# mod_img = Image.fromarray(obj_arr)

					# mod_img.show()

					# masked_img = np.ma.masked_array(img_arr, mask=obj_arr)
					

					#img_arr[obj_arr!=1] = 0

					img_arr = np.add(img_arr, mask * param)
				elif attack_type == "gaussian":
					noise_old = np.random.normal(0.0, param, img_arr.shape)
					noise_old[mask == 0] = 0
					noise = np.array(noise_old, dtype = np.float32)
					print noise.dtype
					img_arr = np.add(img_arr, noise)
				img_arr[img_arr>255] = 255
				img_arr[img_arr<0] = 0
				img_arr = np.array(img_arr, dtype = np.uint8)


				# Insert new Attack Here

				#print img_arr.shape
				mod_img = Image.fromarray(img_arr)
				# mod_img.show()
				mod_img.save(out_dir+"/"+filename, "JPEG")
				# mod_img = Image.composite()


if __name__ == "__main__":
	main()