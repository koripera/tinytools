import cv2
import numpy as np
import sys
import math
import random
import win32gui
import keyboard
import itertools

import numpy as np	
import Dijkstra as D
from mycv import Img
#--------------------
window_name = "frame"
window_size = (1000,1000)

#--------------------

np.set_printoptions(linewidth=1000)
np.set_printoptions(threshold=np.inf)

def main():
	a = np.array([[1, 2, 3],
				  [4, 5, 6],
				  [7, 8, 9]])

	z = cut(a,(-10,4),10)
	print(z)

def cut(array,pos,long):
#np.arrayのスライスの拡張
#スライスできない場所を0で埋める
	array = array.copy()
	baseh ,basew = array.shape
	x,y = pos[0]-1,pos[1]-1

	if y-long < 0:
		for i in range(abs(y-long)):
			array = np.insert(array, 0, 0, axis=0)
			baseh+=1
			y+=1

	if x-long < 0:
		for i in range(abs(x-long)):
			array = np.insert(array, 0, 0, axis=1)
			basew+=1
			x+=1
	
	if baseh < y+long+1 :
		for i in range(abs((y+long+1)-baseh)):
			array = np.append(array, np.zeros((1,basew)) , axis=0)
			baseh+=1

	if basew < x+long+1 :
		for i in range(abs((x+long+1)-basew)):
			array = np.append(array, np.zeros((baseh,1)) , axis=1)
			basew+=1

	#print(array)
		
	return array[y-long:y+long+1 , x-long:x+long+1]

if __name__ == "__main__":
	main() 
	val=input("")
