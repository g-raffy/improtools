# -*- coding: utf-8 -*-
"""
    installation des modules nécéssaires sur macos x :
    sudo port install opencv +python27
    sudo port install py-pyqt4
    sudo port install py-matplotlib

"""
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# import sys

import cv2
# from cv2 import cv
import numpy
import os
# from matplotlib import pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

from . import scene2d
from . import graphing


class Line2D(object):
    def __init__(self, point1, point2):
        self.m_point1 = point1
        self.m_point2 = point2


class IImageProcessListener(object):
    """
        an abstract base class that handle events that happen during an image processing. This provides a flexible way to debug image processing
    """
    def __init__(self):
        self.m_imageIndex = 0

    def onSignal(self, signal, signalName):
        """
            a new signal (1d array) has just been computed
        """
        assert(False)

    def onImage(self, image, imageName):
        """
            a new image has just been computed
        """
        assert(False)


class NullImageProcessListener(IImageProcessListener):

    def __init__(self):
        IImageProcessListener.__init__(self)

    def onSignal(self, signal, signalName):
        pass

    def onBaseImage(self, image, imageName=''):
        pass

    def onImage(self, image, imageName):
        pass

    def onPoint(self, point, layerPath, label=None):
        pass

    def onLine(self, line, layerPath, label=None):
        pass

    def onCircle(self, circle, layerPath, label=None):
        pass


class ImageProcessDebugger(IImageProcessListener):

    def __init__(self, outputFolder='./debug'):
        IImageProcessListener.__init__(self)
        self.m_scene = None
        self.m_baseImageName = None
        self.setOutputFolder(outputFolder)

    def __del__(self):
        # assert( self.m_scene is not None )
        if self.m_scene:
            self.m_scene.saveAsSvg('%s/%s.svg' % (self.m_outputFolder, self.m_baseImageName))
            self.m_scene = None

    def setOutputFolder(self, outputFolderPath):
        if self.m_scene:
            self.m_scene.saveAsSvg('%s/%s.svg' % (self.m_outputFolder, self.m_baseImageName))
            self.m_scene = None
        self.m_outputFolder = outputFolderPath
        pathParts = self.m_outputFolder.split('/')
        path = ''
        for i in range(len(pathParts)):
            if i != 0:
                path += '/'
            path += pathParts[i]
            try:
                os.mkdir(path)
            except (OSError):  # this exception is raised if the folder already exists
                pass

    def onSignal(self, signal, signalName):
        graphing.saveGraph(signal, '%s/%s.pdf' % (self.m_outputFolder, signalName))

    def onSignals(self, signals, signalName):
        graphing.saveMultiGraph(signals, '%s/%s.pdf' % (self.m_outputFolder, signalName))

    def onImage(self, image, imageName):
        # plt.subplot(1,1,1),plt.imshow(contourImage,cmap = 'gray')
        # plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
        # plt.show()
        filePath = '%s/%s.tif' % (self.m_outputFolder, imageName)
        saveImage(image, filePath)

    def onBaseImage(self, image, imageName=''):
        assert(imageName != '')
        self.m_baseImageName = imageName
        filePath = '%s/%s.png' % (self.m_outputFolder, imageName)
        saveImage(image, filePath)
        self.m_scene = scene2d.Scene()
        assert(self.m_scene is not None)
        if self.m_scene:
            self.m_scene.setBaseImage(scene2d.Image(filePath))

    def onPoint(self, point, layerPath, label=None):
        assert(self.m_scene)
        self.m_scene.getLayer(layerPath).addChild(scene2d.Point(point, label))

    def onLine(self, line, layerPath, label=None):
        assert(self.m_scene)
        self.m_scene.getLayer(layerPath).addChild(scene2d.Line(line, label))

    def onCircle(self, circle, layerPath, label=None):
        assert(self.m_scene)
        self.m_scene.getLayer(layerPath).addChild(scene2d.Circle(circle, label))


class IMovieProcessListener(object):
    """
        an abstract base class that handle events that happen durin a movie image processing. This provides a flexible way to debug imageprocessing
    """

    def __init__(self, imageProcessListener):
        self.m_imageIndex = 0
        self.m_imageProcessListener = imageProcessListener

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
        self.m_imageProcessListener.onSignal(signal, signalName)

    def onImage(self, image, imageName):
        """
            a new image has just been computed
        """
        self.m_imageProcessListener.onImage(image, imageName)


class NullMovieProcessListener(IMovieProcessListener):

    def __init__(self):
        IMovieProcessListener.__init__(self, NullImageProcessListener())

    def onSignal(self, signal, signalName):
        pass

    def onImage(self, image, imageName):
        pass


def saveImage(image, filePath):
    print('%s original image type : %s range=(%f:%f)' % (filePath, str(image.dtype), image.min(), image.max()))
    if image.dtype == numpy.bool:
        cv2.imwrite(filePath, image.astype(numpy.uint8) * 255)
    elif image.dtype == numpy.uint16:
        fileExt = filePath.split('.')[-1]
        if fileExt == 'tif':
            # tif file format supports 16 bits per pixel
            cv2.imwrite(filePath, image)
        else:
            u8Image = cv2.normalize(image, alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imwrite(filePath, u8Image)
    elif image.dtype == numpy.float32 or image.dtype == numpy.float64:
        print('image range : %d-%d' % (image.min(), image.max()))
        u8Image = cv2.normalize(image, numpy.array(image.shape, dtype=numpy.uint8), alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        print('u8Image range : %d-%d' % (u8Image.min(), u8Image.max()))
        cv2.imwrite(filePath, u8Image)
    elif image.dtype == numpy.int32:
        print('image range : %d-%d' % (image.min(), image.max()))
        u8Image = cv2.normalize(image, numpy.array(image.shape, dtype=numpy.uint8), alpha=0.0, beta=255.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        print('u8Image range : %d-%d' % (u8Image.min(), u8Image.max()))
        cv2.imwrite(filePath, u8Image)
    else:
        # assert( False )
        cv2.imwrite(filePath, image)


class MovieProcessDebugger(IMovieProcessListener):

    def __init__(self):
        IMovieProcessListener.__init__(self, ImageProcessDebugger())
        self.m_outputFolder = './debug'
        self.m_scene = None
        try:
            os.mkdir(self.m_outputFolder)
        except (OSError):  # this exception is raised if the folder already exists
            pass

    def onImageProcessingStart(self):
        """
            the processing of a new image starts
        """
        IMovieProcessListener.onImageProcessingStart(self)
        self.m_imageProcessListener.setOutputFolder('%s/image%d' % (self.m_outputFolder, self.m_imageIndex))

    def onImageProcessingEnd(self):
        IMovieProcessListener.onImageProcessingEnd(self)
        self.m_imageProcessListener.setOutputFolder(None)

    def onSignal(self, signal, signalName):
        self.m_imageProcessListener.onSignal(signal, signalName)

    def onSignals(self, signals, signalName):
        self.m_imageProcessListener.onSignal(signals, signalName)

    def onImage(self, image, imageName):
        self.m_imageProcessListener.onImage(image, imageName)

    def onBaseImage(self, image, imageName):
        self.m_imageProcessListener.onBaseImage(image, imageName)

    def onPoint(self, point, layerPath, label=None):
        self.m_imageProcessListener.onPoint(image, point, layerPath, label)

    def onCircle(self, circle, layerPath, label=None):
        self.m_imageProcessListener.onPoint(image, circle, layerPath, label)


class IImageProcessor(object):

    def __init__(self, movieProcessListener=NullMovieProcessListener()):
        self.m_movieProcessListener = movieProcessListener

    def processImage(self, image):
        assert(False)  # this method is not supposed to be called

    def get_image_process_listener(self):
        return self.m_movieProcessListener


def findEdges(image):
    sx = cv2.Sobel(image, cv2.CV_32F, dx=1, dy=0, ksize=3)
    sy = cv2.Sobel(image, cv2.CV_32F, dx=0, dy=1, ksize=3)
    return numpy.sqrt(sx * sx + sy * sy)
