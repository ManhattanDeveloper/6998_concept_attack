from PIL import Image
import numpy as np
import sys
import os
print("###Starting###")

directory = sys.argv[1]
out_dir = sys.argv[2]

def main():
	for filename in os.listdir(directory):
		if filename.endswith('.jpg'):
			print()
			num = 154

			obj = Image.open(directory+'/'+filename[:-4]+'_object.png')
			img = Image.open(directory+'/'+filename)
			#obj = Image.open(directory+'/ADE_train_00018094_object.png')
			#img = Image.open(directory+'/ADE_train_00018094.jpg')
			obj_arr = np.array(obj)[:,:,0]

			if num in obj_arr:
				print filename
				obj_arr[obj_arr != num] = 0
				obj_arr[obj_arr == num] = 1
				
				#print obj_arr.shape
				obj_arr = obj_arr.repeat(2, axis=0).repeat(2, axis=1)
				obj_arr = np.repeat(obj_arr[:, :, np.newaxis], 3, axis=2)
				#print obj_arr.shape

				

				# print np.unique(obj_arr.flatten())

				# mod_img = Image.fromarray(obj_arr)

				# mod_img.show()

				img_arr = np.array(img)
				# masked_img = np.ma.masked_array(img_arr, mask=obj_arr)
				

				#img_arr[obj_arr!=1] = 0

				img_arr = np.add(img_arr, obj_arr * 50)
				img_arr[img_arr>255] = 255


				# Insert Attack Here

				#print img_arr.shape
				mod_img = Image.fromarray(img_arr)
				# mod_img.show()
				mod_img.save(out_dir+"/"+filename, "JPEG")
				# mod_img = Image.composite()


if __name__ == "__main__":
	main()