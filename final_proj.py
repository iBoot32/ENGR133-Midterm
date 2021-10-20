"""
===============================================================================
ENGR 13300 Fall 2021

Program Description: Purdue ENGR133 Midterm Project: image encryption/decryption using a XOR Cipher, and using gaussian blur + sobel edge detection to locate Earth in an image
    

Assignment Information
    Assignment:     Python Group Project Fall 2021
    Author:         Tom O'Donnell, tkodonne@purdue.edu
    Team ID:        LC3 - 03

Contributor:    nathan summers, nasummer@purdue.edu
                jack kleck, jkleck@purdue.edu
                pierce johnson, pyjohnso@purdue.edu
                arturo lopez caullieres alopezca@purdue.edu
                
    My contributor(s) helped me:
    [x] understand the assignment expectations without
        telling me how they will approach it.
    [x] understand different ways to think about a solution
        without helping me plan my solution.
    [x] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

import matplotlib.pyplot as plt
import math
import numpy as np
from numpy import random
import scipy as sc
from scipy import ndimage
from scipy import misc

input_image_name = ""

#main function asking user the mode they want to use
def main():
    im = get_image()
    #plt.imshow(im)

    mode = input("Options: encrypt/decrypt/detect: ")
    if mode == "encrypt":
        #plot before image
        plt.hist(im[:,:,0].reshape(im.shape[0]*im.shape[1]),bins=np.arange(2**8+1))
        plt.hist(im[:,:,1].reshape(im.shape[0]*im.shape[1]),bins=np.arange(2**8+1))
        plt.hist(im[:,:,2].reshape(im.shape[0]*im.shape[1]),bins=np.arange(2**8+1))
        plt.show()
        
        xor_cipher(im, xor_key_array(im))
    if mode == "decrypt":
        mode = input("Are you decrypting the PBD image using stock key? yes/no: ")
        if mode == "yes":
            dec_cipher(im, gen_key_array(im, input("Enter your key: ")))
        if mode == "no":
            xor_cipher(im, xor_key_array(im))
            
    if mode == "detect":
        detect_earth(im)


def get_image():
    global input_image_name
    
    #import and plot image
    input_image_name = input("Enter the name of the image file: ")
    image = plt.imread(input_image_name)[:,:,:3]
    
    #begin by checking data type of inage, making sure == uint8
    #uint8 is in range(0, 255)
    if image.dtype != "uint8":
        print("Data type is not uint8. Exiting.")
        return
    else:
        return image
    
def xor_key_array(im):
    inputseed = int(input("Enter your key as int: "))
    np.random.seed(inputseed)
    #using seed, generate array of random ints between 0 and 255
    keyy = random.randint(0, 255, size = im.shape)
    return keyy


def gen_key_array(image, user_key): 
    
    #calculate number of chars in key by splitting to words
    key_len = 0
    split = user_key.split(' ')
    for word in split:
        key_len += len(word)
    
    #get number of rows, columns, and depth of image
    r, c, d = image.shape
    
    #create array full of zeroes of shape (r, c)
    #(r, c) is a tuple with r=rows and c=columns
    #doesn't need depth since key is independent of 
    key_array = np.zeros((r, c))
    
    
    #iterate through rows
    for row_index in range(len(image)):
        #iterate through columns
        for column_index in range(len(image[0])):
            #calculate A value, and use it to calculate key for given pixel
            A = ((row_index)*(column_index)) % key_len
            key = A*(2**8 // (key_len))
            
            #add key value to key array
            key_array[row_index][column_index] = key
    return key_array


def dec_cipher(image, key_arr):
    #get image dimensions
    r = image.shape[0]
    c = image.shape[1]
    d = image.shape[2]
    
    #create new image with sizes of encrypted image
    new_im = np.zeros((r, c, d))
    
    #iterate through rows and columns
    for row_index in range(len(image)):
        for column_index in range(len(image[0])):
            
            #take each pixel in R, G, and B depth, and apply XOR operator. no need to convert to binary since ^ operator supports integers.
            new_im[row_index][column_index][0] = int(key_arr[row_index][column_index]) ^ int(image[row_index][column_index][0])
            new_im[row_index][column_index][1] = int(key_arr[row_index][column_index]) ^ int(image[row_index][column_index][1])
            new_im[row_index][column_index][2] = int(key_arr[row_index][column_index]) ^ int(image[row_index][column_index][2])
            
      #display and save image      
    plt.imshow(new_im.astype('uint8'))
    plt.imsave("yea.tiff", new_im.astype('uint8'))

def xor_cipher(image, key_arr):
    #get image dimensions
    r = image.shape[0]
    c = image.shape[1]
    d = image.shape[2]
    
    #create new image with sizes of encrypted image
    new_im = np.zeros((r, c, d))
    
    #iterate through rows and columns
    for row_index in range(len(image)):
        for column_index in range(len(image[0])):
            #print(key_arr[row_index][column_index])
            
            #take each pixel in R, G, and B depth, and apply XOR operator. no need to convert to binary since ^ operator supports integers.
            new_im[row_index][column_index][0] = int(key_arr[row_index][column_index][0]) ^ int(image[row_index][column_index][0])
            new_im[row_index][column_index][1] = int(key_arr[row_index][column_index][1]) ^ int(image[row_index][column_index][1])
            new_im[row_index][column_index][2] = int(key_arr[row_index][column_index][2]) ^ int(image[row_index][column_index][2])
            
            
            
      #display and save image      
    plt.imshow(new_im.astype('uint8'))
    plt.show()
    
    plt.hist(new_im[:,:,0].reshape(new_im.shape[0]*new_im.shape[1]),bins=np.arange(2**8+1))
    plt.hist(new_im[:,:,1].reshape(new_im.shape[0]*new_im.shape[1]),bins=np.arange(2**8+1))
    plt.hist(new_im[:,:,2].reshape(new_im.shape[0]*new_im.shape[1]),bins=np.arange(2**8+1))
    plt.show()
    
    plt.imsave("yea.tiff", new_im.astype('uint8'))
            
        
def detect_earth(im):
    r, c, d = im.shape
    
    #create array full of zeroes of shape (r, c)
    #(r, c) is a tuple with r=rows and c=columns
    #doesn't need depth since key is independent of pixel value
    gs_im = np.zeros((r, c))
    
    
    #grayscale image by iterating through pixels and using recommended formula
    #iterate through rows
    for row_index in range(len(im)):
        #iterate through columns
        for column_index in range(len(im[0])):
            r = im[row_index][column_index][0]
            g = im[row_index][column_index][1]
            b = im[row_index][column_index][2]
            
            gs_im[row_index][column_index] = (0.3*r) + (0.59*g) + (0.11*b)
            
    print("Outputting grayscaled image")
    plt.imshow(gs_im.astype('uint8'))
    plt.show()
            
    #gaussian filter using scipy
    s = 1.056 #sigma
    w = 5
    t = (((w-1)/2) - 0.5)/s #calc truncate value based on w and sigma
    g_gs_im = sc.ndimage.filters.gaussian_filter(gs_im, sigma=s, truncate=t)
    
    print("Outputting gaussian blurred image")
    plt.imshow(g_gs_im.astype('uint8'))
    plt.show()
            
    
    #partial derivatives using scipy's sobel edge detection algorithm
    dx = ndimage.sobel(g_gs_im, 0)  # horizontal derivative
    dy = ndimage.sobel(g_gs_im, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  #create image of magnitude of vert+horiz derivatives of image
    
    #iterate through pixels to find maximum value in image, which is Earth's location
    max_val = 0
    for row_index in range(300, len(mag)): #start at 300 just to save loop iterations
        #iterate through columns
        for column_index in range(300, len(mag[0])):
            if mag[row_index][column_index] > max_val:
                max_val = mag[row_index][column_index]
                row = row_index
                col = column_index
   
    print("Showing image with sobel edge detection applied")
    plt.imshow(mag.astype('uint8'))
    plt.show()
    print(f'Eath detected at location ({row}, {col}) with brightness of {max_val}.')
    
#create empty array for zoomed imahe    
    #get pixels within a 50 pixel horiz/vert radius around the Earth to act as a window to zoom into
    zoomed = np.zeros((101, 101))
    for row_index in range(0, 101):
        for column_index in range(0, 101):
            zoomed[row_index][column_index] = mag[-50 + row + row_index][-50 + col + column_index]
    
    
    plt.figure()
    plt.imshow(zoomed.astype('uint8'), cmap="gray")

        
if __name__ == "__main__":
    main()