import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTK, Image

""" fileopenbox opens the box to choose file 
and help us store file path as string"""

top = tk.tk()
top.geometry('400x400')
top.title('cartoonify Your Image !')
top.configure(background='white')
label = Label(top, background = '#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    original_img = cv2.imread(ImagePath) #read the image
    original_img = cv2.cvtcolor(original_img, cv2.color_BGR2RGB)
    #image is stored in form of numbers
    #confirm that image is chosen
    if original_img is None:
        print("Can not find any Image")
        sys.exit()
    Resized1 = cv2.resize(original_img, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')
    #converting an image to grayscale
    grayScaleImage = cv2.cvtColor(original_img, cv2.Color_BGR2GRAY)
    Resized2 = cv2.resize(grayScaleImage, (960, 540))
   
    #applying median blur to smoothen an image
    smoothGrayScale = cv2.mediamBlur(grayScaleImage, 5)
    Resized3 = cv2.resize(smoothGrayScale, (960, 540))
  
    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    Resized4 = cv2.resize(getEdge, (960, 540))
  
    #applying bilateral filter to remove noise
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(original_img, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960, 540))
   
    #masking edged image with our "Beautify" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    Resized6 = cv2.resize(cartoonImage, (960, 540))
  
    #Plotting the whole transition
    image = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(image[i], cmap='gray')
    
    save1=Button(top, text="Save cartoon image", command=lambda: save(Resized6, ImagePath),padx=38,pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)
    #save button code
    plt.show()

def save(Resized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.Color_RGB2BGR))
    I = "Image saved by name" + newName + " at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)

top.mainloop()
    