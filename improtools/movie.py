# -*- coding: utf-8 -*-
"""
    installation des modules nécéssaires sur macos x :
    sudo port install opencv +python27
    sudo port install py-pyqt4
    sudo port install py-matplotlib

"""

import cv2
import numpy


def u16tou8image(u16Image, focusRange=None):

    if focusRange is None:
        focusRange = (u16Image.min(), u16Image.max())

    def display(image, display_min, display_max):  # copied from Bi Rico
        # Here I set copy=True in order to ensure the original image is not
        # modified. If you don't mind modifying the original image, you can
        # set copy=False or skip this step.
        image = numpy.array(image, copy=True)
        image.clip(display_min, display_max, out=image)
        image -= display_min
        image //= (display_max - display_min + 1) / 256.
        return image.astype(numpy.uint8)

    def lut_display(image, display_min, display_max):
        lut = numpy.arange(2**16, dtype='uint16')
        lut = display(lut, display_min, display_max)
        return numpy.take(lut, image)
    return lut_display(u16Image, focusRange[0], focusRange[1])


class IImageFeeder(object):

    def __init__(self, name):
        self.m_name = name

    def getName(self):
        return self.m_name

    def getMinIndex(self):
        assert(False)

    def getMaxIndex(self):
        assert(False)

    def getImage(self, index):
        assert(False)

    def getImageSize(self):
        assert(False)


class FolderImageFeeder(IImageFeeder):

    def __init__(self, folderPath):
        IImageFeeder.__init__(self, folderPath)
        self.m_folderPath = folderPath
        from os import walk
        self.m_sequenceFileNames = []
        for (dirpath, dirnames, filenames) in walk(folderPath):
            for filename in filenames:
                if filename.split('.')[-1] in ('tif'):
                    self.m_sequenceFileNames.append(folderPath + '/' + filename)
            # sequenceFileNames.extend(filenames)
            break
        print(self.m_sequenceFileNames)
        image = self.getImage(0)
        self.m_imageSize = image.shape

    def getMinIndex(self):
        return 0

    def getMaxIndex(self):
        return len(self.m_sequenceFileNames) - 1

    def getImage(self, imageIndex):
        cv_img = cv2.imread(self.m_sequenceFileNames[imageIndex], cv2.IMREAD_ANYDEPTH)  # read image with opencv
        print(cv_img.min())
        print(cv_img.max())
        # print(cv_img.depth())
        print(cv_img.shape)
        print(cv_img.dtype)

        # cv_img = u16tou8image(cv_img)

        return cv_img

    def getImageSize(self):
        return self.m_imageSize


class MovieSampler(IImageFeeder):
    """
        a movie that is a smpling of another movie (only keeps one frame out of n frames)
    """

    def __init__(self, imageFeeder, imageStep):
        """
            imageFeeder    the source movie
            imageStep use 1 image every imageStep images
        """
        IImageFeeder.__init__(self, imageFeeder.getName())
        self.m_imageFeeder = imageFeeder
        self.m_step = imageStep

    def getMinIndex(self):
        return 0

    def getMaxIndex(self):
        orgMin = self.m_imageFeeder.getMinIndex()
        orgMax = self.m_imageFeeder.getMaxIndex()
        orgNumImages = (orgMax + 1 - orgMin)
        return orgNumImages // self.m_step

    def getImage(self, imageIndex):
        orgImageIndex = (imageIndex * self.m_step) + self.m_imageFeeder.getMinIndex()
        return self.m_imageFeeder.getImage(orgImageIndex)

    def getImageSize(self):
        return self.m_imageFeeder.getImageSize()


class ImageSelector(IImageFeeder):
    """
        a movie that is a sampling of another movie (only keeps one frame)
    """

    def __init__(self, imageFeeder, imageIndex):
        """
            imageFeeder    the source movie
            imageIndex the index of the selected inmage in the movie
        """
        IImageFeeder.__init__(self, imageFeeder.getName())
        self.m_imageFeeder = imageFeeder
        self.m_imageIndex = imageIndex

    def getMinIndex(self):
        return 0

    def getMaxIndex(self):
        return 0

    def getImage(self, imageIndex):
        assert(imageIndex <= self.getMaxIndex())
        return self.m_imageFeeder.getImage(self.m_imageIndex)

    def getImageSize(self):
        return self.m_imageFeeder.getImageSize()

# pyqtTest()
