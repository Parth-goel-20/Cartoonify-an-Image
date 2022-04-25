import cv2
import numpy as np

import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk


class Cartoonizer:
	"""Cartoonizer effect
		A class that applies a cartoon effect to an image.
		The class uses a bilateral filter and adaptive thresholding to create
		a cartoon effect.
	"""
	#variable
	def _init_(self):
		pass

	def render(self, img_rgb):
		img_rgb = cv2.imread(img_rgb)
		img_rgb = cv2.resize(img_rgb, (1366,668))
		numDownSamples = 2	 # number of downscaling steps
		numBilateralFilters = 50 # number of bilateral filtering steps

		# -- STEP 1 --

		# downsample image using Gaussian pyramid
		img_color = img_rgb
		for _ in range(numDownSamples):
			img_color = cv2.pyrDown(img_color)

		#cv2.imshow("downcolor",img_color)
		#cv2.waitKey(0)
		# repeatedly apply small bilateral filter instead of applying
		# one large filter
		for _ in range(numBilateralFilters):
			img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

		#cv2.imshow("bilateral filter",img_color)
		#cv2.waitKey(0)
		# upsample image to original size
		for _ in range(numDownSamples):
			img_color = cv2.pyrUp(img_color)
		#cv2.imshow("upscaling",img_color)
		#cv2.waitKey(0)

		# -- STEPS 2 and 3 --
		# convert to grayscale and apply median blur
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
		img_blur = cv2.medianBlur(img_gray, 3)
		#cv2.imshow("grayscale+median blur",img_color)
		#cv2.waitKey(0)

		# -- STEP 4 --
		# detect and enhance edges
		img_edge = cv2.adaptiveThreshold(img_blur, 255,
										cv2.ADAPTIVE_THRESH_MEAN_C,
										cv2.THRESH_BINARY, 9, 2)
		#cv2.imshow("edge",img_edge)
		#cv2.waitKey(0)

		# -- STEP 5 --
		# convert back to color so that it can be bit-ANDed with color image
		(x,y,z) = img_color.shape
		img_edge = cv2.resize(img_edge,(y,x))
		img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
		cv2.imwrite("edge.png",img_edge)
		#cv2.imshow("step 5", img_edge)
		#cv2.waitKey(0)
		#img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2]))
		#print img_edge.shape, img_color.shape
		return cv2.bitwise_and(img_color, img_edge)

tmp_canvas = Cartoonizer()

##
my_w = tk.Tk()
my_w.geometry("600x350")  # Size of the window
my_w.title('Pick an image now')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Now Pick a Photo',width=30,font=my_font1)
l1.grid(row=1,column=1)
b1 = tk.Button(my_w, text='Upload File', width=20,command = lambda:upload_file())
b1.grid(row=2,column=1)

def upload_file():
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    b2 =tk.Button(my_w,image=img) # using Button
    b2.grid(row=3,column=1)


my_w.mainloop()  # Keep the window open

##
file_name = r'b2'
res = tmp_canvas.render(file_name)
file_path_name = 'img'
file_name = file_path_name


cv2.imwrite("Cartoon version.jpg", res)
cv2.imshow("Cartoon version", res)
cv2.waitKey(0)
cv2.destroyAllWindows()