import numpy


class Histogram:

    def __init__(self, min, max, numBins):
        self.m_min = min
        self.m_max = max
        self.m_numBins = numBins

        self.m_data = numpy.zeros(self.m_numBins)
        binSize = (self.m_max - self.m_min) / self.m_numBins
        self.m_oneOneBinWidth = 1.0 / binSize

    def addValue(self, value):
        iBinIndex = (value - self.m_min) * self.m_oneOneBinWidth
        if iBinIndex < 0:
            return
        if iBinIndex >= self.m_numBins:
            return
        self.m_data[iBinIndex] += 1

    def get_bin_range(self, bin_index):
        bin_size = (self.m_max - self.m_min) / self.m_numBins
        bin_min = self.m_min + bin_size * bin_index
        return (bin_min, bin_min + bin_size)

    def getArray(self):
        return self.m_data
