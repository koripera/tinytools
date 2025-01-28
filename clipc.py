"""
"""
import pyperclip

import os
import re


def change(txt):
	txt = TEX(txt)


	return txt.txt


def change1(txt):

	
	pyperclip.copy(txt)
	print(repr(txt))

def tr(strobject,want,wordlist):
	return re.sub("|".join(wordlist), want, strobject)

def main():
	while True:
		change1(pyperclip.waitForNewPaste())

class TEX:
	def __init__(self,txt):
		self.txt = txt.strip()

	def tr(self,new,old):
		self.txt = re.sub("|".join(old), new, self.txt)

if __name__=="__main__":
	main()


