# -*- coding: utf-8 -*-
"""
	installation des modules nécéssaires sur macos x :
	sudo port install opencv +python27
	sudo port install py-pyqt4
	sudo port install py-matplotlib

"""
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
#import sys

import cv2
from cv2 import cv
import numpy
import os
import sys
#from matplotlib import pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages

sys.path.append('../Libraries/python')
import scene2d
import graphing

class Line2D(object):
	def __init__( self, point1, point2 ):
		self.m_point1 = point1
		self.m_point2 = point2
	


class IMovieProcessListener(object):
	"""
		an abstract base class that handle events that happen durin a movie image processing. This provides a flexible way to debug imageprocessing
	"""
	def __init__(self):
		self.m_imageIndex = 0
	def onImageProcessingStart(self):
		"""
			the processing of a new image starts
		"""
		self.m_imageIndex += 1		
	def onImageProcessingEnd(self):
		"""
			the processing of a new image ends
		"""
		pass
	def onSignal(self, signal, signalName):
		"""
			a new signal (1d array) has just been computed
		"""
		assert( False )
	def onImage(self, image, imageName):
		"""
			a new image has just been computed
		"""
		assert( False )

class NullMovieProcessListener(IMovieProcessListener):
	def __init__(self):
		IMovieProcessListener.__init__( self )
	def onSignal(self, signal, signalName):
		pass
	def onImage(self, image, imageName):
		pass

def saveImage(image, filePath):
	print('%s original image type : %s range=(%f:%f)' % (filePath, str(image.dtype), image.min(), image.max()))
	if image.dtype == numpy.bool:
		cv2.imwrite(filePath, image.astype(numpy.uint8)*255)
	elif image.dtype == numpy.uint16:
		fileExt = filePath.split('.')[-1]
		if fileExt == 'tif':
			# tif file format supports 16 bits per pixel 
			cv2.imwrite(filePath, image)
		else:
			u8Image = cv2.normalize(image, alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)		
			cv2.imwrite(filePath, u8Image)
	elif image.dtype == numpy.float32:
		cv2.imwrite(filePath, cv2.normalize(image, alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U))
	elif image.dtype == numpy.int32:
		print('image range : %d-%d' % (image.min(), image.max()))
		u8Image = cv2.normalize(image, alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)	
		print('u8Image range : %d-%d' % (u8Image.min(), u8Image.max()))
		cv2.imwrite(filePath, u8Image)
	else:
		#assert( False )
		cv2.imwrite(filePath, image)
	

class MovieProcessDebugger(IMovieProcessListener):
	def __init__(self):
		IMovieProcessListener.__init__( self )
		self.m_outputFolder='./debug'
		self.m_scene = None
		try:
			os.mkdir(self.m_outputFolder)
		except (OSError): # this exception is raised if the folder already exists
			pass
	def onImageProcessingStart(self):
		"""
			the processing of a new image starts
		"""
		IMovieProcessListener.onImageProcessingStart(self)
		assert( self.m_scene is None )
		self.m_scene = scene2d.Scene()
	def onImageProcessingEnd(self):
		IMovieProcessListener.onImageProcessingEnd(self)
		# save the svgImage for the previous image
		assert( self.m_scene is not None )
		if self.m_scene:
			self.m_scene.saveAsSvg('%s/result_%03d.svg' % (self.m_outputFolder, self.m_imageIndex))
			self.m_scene = None
	def onSignal(self, signal, signalName):
		graphing.saveGraph(signal, '%s/%s_%03d.pdf' % (self.m_outputFolder, signalName, self.m_imageIndex))
	def onSignals(self, signals, signalName):
		graphing.saveMultiGraph(signals, '%s/%s_%03d.pdf' % (self.m_outputFolder, signalName, self.m_imageIndex))
	def onImage(self, image, imageName):
		#plt.subplot(1,1,1),plt.imshow(contourImage,cmap = 'gray')
		#plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
		#plt.show()
		filePath = '%s/%s_%03d.tif' % (self.m_outputFolder, imageName, self.m_imageIndex)
		saveImage( image, filePath )
	def onBaseImage(self, image, imageName):
		filePath = '%s/%s_%03d.png' % (self.m_outputFolder, imageName, self.m_imageIndex)
		saveImage( image, filePath )
		assert( self.m_scene is not None )
		if self.m_scene:
			self.m_scene.setBaseImage(scene2d.Image(filePath))
				
	def onPoint(self, point, layerPath, label=None ):
		assert( self.m_scene )
		self.m_scene.getLayer(layerPath).addChild(scene2d.Point(point, label))
	def onCircle(self, circle, layerPath, label=None ):
		assert( self.m_scene )
		self.m_scene.getLayer(layerPath).addChild(scene2d.Circle(circle, label))


class IImageProcessor(object):
	
	def __init__(self, m_movieProcessListener = NullMovieProcessListener()):
		self.m_movieProcessListener = m_movieProcessListener

	def processImage(self, image):
		assert( False ) # this method is not supposed to be called



def findEdges(image):
	sx = cv2.Sobel(image, cv2.CV_32F, dx=1, dy=0, ksize=3)
	sy = cv2.Sobel(image, cv2.CV_32F, dx=0, dy=1, ksize=3)
	return numpy.sqrt(sx*sx + sy*sy)
	




	
