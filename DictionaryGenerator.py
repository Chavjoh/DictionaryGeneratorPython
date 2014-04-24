#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------#
# Security - Dictionary Generator                                              #
# ============================================================================ #
# Developer:    Chavaillaz Johan                                               #
# Filename:     DictionaryGenerator.py                                         #
# Version:      1.0                                                            #
#                                                                              #
# Licensed to the Apache Software Foundation (ASF) under one                   #
# or more contributor license agreements. See the NOTICE file                  #
# distributed with this work for additional information                        #
# regarding copyright ownership. The ASF licenses this file                    #
# to you under the Apache License, Version 2.0 (the                            #
# "License"); you may not use this file except in compliance                   #
# with the License. You may obtain a copy of the License at                    #
#                                                                              #
# http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                              #
# Unless required by applicable law or agreed to in writing,                   #
# software distributed under the License is distributed on an                  #
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY                       #
# KIND, either express or implied. See the License for the                     #
# specific language governing permissions and limitations                      #
# under the License.                                                           #
#                                                                              #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                                                              #
#                               LIBRARIES IMPORT                               #
#                                                                              #
#------------------------------------------------------------------------------#

import sys
import argparse
import math

#------------------------------------------------------------------------------#
#                                                                              #
#                             UTILITIES FUNCTIONS                              #
#                                                                              #
#------------------------------------------------------------------------------#

def updateProgress(percent, barLength = 20):
	"""Update progress bar in command line"""
	hashes = '#' * int(round(percent * barLength / 100 ))
	spaces = ' ' * (barLength - len(hashes))
	
	sys.stdout.write("\rGenerating ... [{0}] {1}%".format(hashes + spaces, int(round(percent))))
	sys.stdout.flush()
	
def sizeDictionary(alphabetSize, minSize, maxSize):
	"""Calculate dictionary total size with indicated parameters"""
	sum = 0
	
	for currentSize in range(minSize, maxSize+1):
		sum += pow(alphabetSize, currentSize)
	
	return sum

def generateDictionary(alphabet, minSize, maxSize):
	"""Generate dictionary with indicated parameters"""
	alphabetSize = len(alphabet);
	currentAlphabetIndex = {}
	
	# Needed to update progress bar
	totalGeneration = sizeDictionary(alphabetSize, minSize, maxSize)
	currentGeneration = 0

	# Open or create database file
	with open('dictionary.txt', 'w+') as file:

		# Foreach size needed
		for currentSize in range(minSize, maxSize+1):

			# Current possibility
			currentIndex = 0

			# Calculate the number of possibilities
			currentIndexMax = pow(alphabetSize, currentSize)

			# While until the number of possibilities is reached
			while (currentIndex < currentIndexMax):

				word = ""

				# Current position in current size to be generated
				for currentPosition in range(0, currentSize):

					# Initialization of alphabet index for each position
					currentAlphabetIndex[currentPosition] = 0

					# Calculate reverse position to calculate indexValue
					# Reverse because we begin to change on the right of the word
					reversePosition = currentSize - 1 - currentPosition

					# Calculate the index of the current character to use in alphabet
					indexValue = math.floor((currentIndex / pow(alphabetSize, reversePosition)))  % alphabetSize

					# Add the character of the alphabet to the word
					word += alphabet[indexValue]

				file.write(word + '\n')
				
				currentGeneration += 1
				updateProgress((currentGeneration / totalGeneration) * 100)
				
				currentIndex += 1


#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
#                                                                              #
#                               "MAIN" FUNCTION                                #
#                                                                              #
#------------------------------------------------------------------------------#

# If this is the main module, run this
if __name__ == '__main__':
	argsCount = len(sys.argv)

	# Create argument parser to help user
	parser = argparse.ArgumentParser(
		description='Dictionary generator.'
	)
	parser.add_argument(
		'alphabet',
		type=str,
		help='Alphabet to use to generate all dictionary words.'
	)
	parser.add_argument(
		'minSize', 
		type=int,
		help='Minimum size of the generated words.'
	)
	parser.add_argument(
		'maxSize', 
		type=int,
		help='Maximum size of the generator words.'
	)

	# Show help if one of the arguments is missing
	if argsCount != 4:
		parser.print_help()
		sys.exit()
	
	# Get configuration
	alphabet = sys.argv[1]
	minSize = int(sys.argv[2])
	maxSize = int(sys.argv[3])

	if minSize > maxSize:
		print("Minimum size can't be superior to maxSize")

	generateDictionary(alphabet, minSize, maxSize)
