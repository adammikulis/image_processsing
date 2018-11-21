# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 09:24:47 2018

@author: adam mikulis

Bi-linear interpolation for 1D list of pixels
"""

import pygame, sys, random
from pygame.locals import *
from time import sleep
import numpy as np


#random.seed(17)
pygame.init()

tilesize = 5
color_min = 23
color_max = 37

# testing list
#ir = [1, 2, 3, 4,
#      2, 3, 4, 5,
 #    3, 4, 5, 6]


class Interpolation():
    def __init__(self, image, width, height, color_min, color_max, tilesize):
        self.image = image
        self.image_grayscale = []
        # 4:3 aspect ratio
        self.width = width
        self.height = height
        self.color_min = color_min
        self.color_max = color_max
        self.scale_factor = 3
        self.tilesize = tilesize

    def convert_1D(self):
        temp_list = []
        temp_list2 = []
        for i in range(self.height):
            for j in range(self.width - 1):
                temp_list.append(self.image[i][j])
        for i in range(self.height):
            for j in range(self.width - 1):
                temp_list.append(self.image[i][j])
        self.image = temp_list
        self.image_grayscale = temp_list2

    def convert_1D_gray(self):
        temp_list = []
        for i in range(self.height):
            for j in range(self.width - 1):
                temp_list.append(self.image[i][j])
        for i in range(self.height):
            for j in range(self.width - 1):
                temp_list.append(self.image[i][j])
        self.image_grayscale = temp_list

    # Convert 1D list into 2D list
    def convert_2D(self):
        self.image = [self.image[i:i+self.width] for i in range(0, len(self.image), self.width)]
    # Same but for grayscale image
    def convert_2D_gray(self):
        self.image_grayscale = [self.image_grayscale[i:i+self.width] for i in range(0, len(self.image_grayscale), self.width)]

    # Take average of pixels to form new one across rows (one direction)
    def linear(self):
        new_pixel_list = []
        for i in range(self.height):
            for j in range(self.width-1):
                p1 = self.image[i][j]
                p2 = self.image[i][j+1]
                p_new = (p1 + p2) / 2
                new_pixel_list.append(p1)
                new_pixel_list.append(p_new)
            new_pixel_list.append(p2)
        self.width = self.width * 2 - 1
        self.image = new_pixel_list

    # Switchs rows/columns
    def transpose(self):
        self.width, self.height = self.height, self.width
        self.image = [list(i) for i in zip(*self.image)]

    ''' not functional at this time
    def min_max(self):
        for i in range(len(self.image)):
            if self.image[i] < self.minimum:
                self.minimum = self.image[i]
            if self.image[i] > self.maximum:
                self.maximum = self.image[i]
        return self.minimum, self.maximum
    '''

    def convert_to_grayscale(self):
        for i in range(len(self.image)):
            self.image_grayscale.append(self.image[i] * self.scale_factor)

    # Main conversion loop for linear interpolation
    def lin_main(self):
        self.convert_2D()
        self.transpose()
        self.linear()
        self.convert_2D()
        self.transpose()
        self.linear()

def import_pixels(filename):
    frame_data = open(filename, 'r')
    lines = frame_data.readlines()
    return lines



frame_data = import_pixels('pixel_data.txt')

frame_array = np.empty([40, 768])
'''
for x in range(len(frame_data)-1):
    frame_buff = frame_data[x]
    frame_buff = frame_buff.replace(' ','').split(',')
    frame_buff = np.array(frame_buff)
    frame_buff = frame_buff.astype(np.float16)

    for i in range(len(frame_data)-1):
        for j in range(len(frame_buff)):
            frame_array[i][j] = frame_buff[j]'''



# Repeat image processing x times
while True:
    # Create array of random elements (total pixels) for testing
    #rand_ir = []
    #elements = 768
    #for i in range(elements):
    #    rand_ir.append(random.randint(color_min, color_max))

    for x in range(len(frame_data)):
        frame_buff = frame_data[x]
        frame_buff = frame_buff.replace(' ','').split(',')
        frame_buff = np.array(frame_buff)
        frame_buff = frame_buff.astype(np.float16)

        # Initialize 2 image objects with same dataset
        img1 = Interpolation(frame_buff, 32, 24, color_min, color_max, tilesize)
        img2 = Interpolation(frame_buff, 32, 24, color_min, color_max, tilesize)

        # Convert 1D pixel array to scaled 0-255 1D array, then convert to 2D
        img1.convert_to_grayscale()
        img1.convert_2D_gray()

        # Main loop processes on img2 with bilinear interpolation
        img2.lin_main()
        img2.convert_to_grayscale()
        img2.convert_2D_gray()

        # 3rd image
        img3 = Interpolation(img2.image, 63, 47, color_min, color_max, tilesize)
        img3.lin_main()
        img3.convert_to_grayscale()
        img3.convert_2D_gray()

        # Initialize display
        surf = pygame.display.set_mode((img3.width*tilesize+100,img1.height*tilesize+img2.height*tilesize+img3.height*tilesize+200))

        # Plot pixels of original image
        for i in range(img1.height):
           for j in range(img1.width):
               pygame.draw.rect(surf, (img1.image_grayscale[i][j], 0, 255 - img1.image_grayscale[i][j]), (j*19+25, i*19+25, 19, 19))

        # Plot pixels of interpolated image
        '''for i in range(img2.height):
           for j in range(img2.width):
               pygame.draw.rect(surf, (img2.image_grayscale[i][j], 0, 255 - img2.image_grayscale[i][j]), (j*tilesize+25, i*tilesize + tilesize*img1.height + 50, tilesize, tilesize))'''

        for i in range(img3.height):
            for j in range(img3.width):
                pygame.draw.rect(surf, (img3.image_grayscale[i][j], 0, 255 - img3.image_grayscale[i][j]), (j*tilesize+25, i*tilesize+tilesize*img1.height+tilesize*img2.height+150, tilesize, tilesize))

        # Update and pause before next frame
        pygame.display.update()
        sleep(.25)

    pygame.quit()
    sys.exit()