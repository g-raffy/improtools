# -*- coding: utf-8 -*-
"""
	installation des modules nécéssaires sur macos x :
	sudo port install opencv +python27
	sudo port install py-pyqt4
	sudo port install py-matplotlib

"""
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages


class Signal:
	def __init__(self, signal, name=None):
		self.m_signalValues = signal
		self.m_name = name

class Point2D(object):
	def __init__(self, x, y):
		self.m_x = x
		self.m_y = y
	@property
	def x(self):
		return self.m_x
	@property
	def y(self):
		return self.m_y

class ScatterPlot(object):
	def __init__(self, xAxisDesc = None, yAxisDesc = None):
		self.m_points = []
		self.m_xAxisDesc = xAxisDesc
		self.m_yAxisDesc = yAxisDesc
	def append(self, point2d ):
		self.m_points.append(point2d)
	@property
	def xAxisDesc(self):
		return self.m_xAxisDesc
	@property
	def yAxisDesc(self):
		return self.m_yAxisDesc

	def setXAxisDesc(self, description):
		self.m_xAxisDesc = description
	def setYAxisDesc(self, description):
		self.m_yAxisDesc = description
	def __iter__(self):
		return iter(self.m_points)		

def saveScatterPlot( scatterPlot, pdfFileName):
	fig = pyplot.figure()
	pyplot.subplot(1,1,1)
	x = []
	y = []
	for point in scatterPlot:
		x.append( point.x )
		y.append( point.y )
	pyplot.scatter(x, y)
	if scatterPlot.xAxisDesc is not None:
		pyplot.xlabel(scatterPlot.xAxisDesc)
	if scatterPlot.yAxisDesc is not None:
		pyplot.ylabel(scatterPlot.yAxisDesc)
		
	#print('saving to '+pdfFileName)
	pp = PdfPages(pdfFileName)
	pp.savefig( fig )
	pp.close()
	pyplot.close(fig)
	
	
def saveGraph(signal, pdfFileName):
	fig = pyplot.figure()
	pyplot.subplot(1,1,1)
	pyplot.plot(signal)
	
	print('saving to '+pdfFileName)
	pp = PdfPages(pdfFileName)
	pp.savefig( fig )
	pp.close()
	pyplot.close(fig)

def saveMultiGraph(signals, pdfFileName):
	fig = pyplot.figure()
	pyplot.subplot(1,1,1)
	for signal in signals:
		print('plotting signal %s' % str(signal.m_signalValues.shape))
		pyplot.plot(signal.m_signalValues, label=signal.m_name)
	print('saving to '+pdfFileName)
	pyplot.legend()
	pp = PdfPages(pdfFileName)
	pp.savefig( fig )
	pp.close()
	pyplot.close(fig)




	
