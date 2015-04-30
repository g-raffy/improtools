# -*- coding: utf-8 -*-
import cv2

class ISceneNodeVisitor(object):
	def __init__(self):
		pass
	
	def visitPoint(self, point):
		assert( False )

	def visitImage(self, image):
		assert( False )
		
	def visitLayer(self, layer):
		assert( False )
	
	def visitScene(self, scene):
		assert( False )
		
	def visitLine(self, line):
		assert( False )



class ISceneNode(object):
	def __init__(self):
		pass
	
	def onVisit(self, visitor ):
		assert( False )

class Point(ISceneNode):
	def __init__(self, coords, label = None):
		self.m_coords = coords
		self.m_label = label

	def onVisit( self, visitor ):
		visitor.visitPoint( self )

class Line(ISceneNode):
	def __init__(self, line, label = None):
		self.m_from = line[0]
		self.m_to = line[1]
		self.m_label = label

	def onVisit( self, visitor ):
		visitor.visitLine( self )

class Circle(ISceneNode):
	def __init__(self, circle, label = None):
		self.m_center = (circle[0], circle[1])
		self.m_radius = circle[2]
		self.m_label = label

	def onVisit( self, visitor ):
		visitor.visitCircle( self )

class Image(ISceneNode):
	def __init__(self, imageFilePath):
		self.m_imageFilePath = imageFilePath

	def onVisit(self, visitor ):
		visitor.visitImage( self )

	def getFilePath(self):
		return self.m_imageFilePath

	def getSize(self):
		cv_img = cv2.imread(self.m_imageFilePath, cv2.IMREAD_ANYDEPTH)
		return cv_img.shape
		
class Layer(ISceneNode):
	def __init__(self, layerName):
		self.m_name = layerName
		self.m_children = []
		self.m_layers = {}

	def getName(self):
		return self.m_name

	def addChild(self, childNode):
		self.m_children.append( childNode )
		
	def onVisit(self, visitor ):
		visitor.visitLayer( self )

	def addLayer(self, layer):
		print('adding layer %s' % layer.getName())
		self.m_layers[ layer.getName() ] = layer
	


class Scene(ISceneNode):
	def __init__(self):
		self.m_image = None
		self.m_rootLayer = Layer('root')

	def onVisit(self, visitor ):
		visitor.visitScene( self )
	
	def setBaseImage( self, image ):
		self.m_image = image
	
	def getLayer(self, layerPath):
		pathParts = layerPath.split('/')
		parentLayer = self.m_rootLayer
		for layerName in pathParts:
			if layerName not in parentLayer.m_layers:
				parentLayer.addLayer( Layer(layerName) )
			parentLayer = parentLayer.m_layers[layerName]
		return parentLayer
	
	def saveAsSvg(self, filePath):
		visitor = SvgExporter( filePath )
		self.onVisit(visitor)
		
class SvgExporter(ISceneNodeVisitor):
	def __init__(self, svgFilePath):
		self.m_svgFilePath = svgFilePath

	def visitPoint(self, point):
		radius = 1.0
		self.m_f.write('<circle cx="%.3f" cy="%.3f" r="%.3f"/>\n' % (point.m_coords[0], point.m_coords[1], radius) )
		if point.m_label is not None :
			self.m_f.write('<text x="%.3f" y="%.3f">%s</text>\n' % (point.m_coords[0], point.m_coords[1], point.m_label) )

	def visitLine(self, line):
		radius = 1.0
		self.m_f.write('<line x1="%.3f" x2="%.3f" y1="%.3f" y2="%.3f"/>\n' % (line.m_from[0], line.m_to[0], line.m_from[1], line.m_to[1]) )
		if line.m_label is not None :
			self.m_f.write('<text x="%.3f" y="%.3f">%s</text>\n' % (line.m_from[0], line.m_from[1], point.m_label) )

	def visitCircle(self, circle):
		radius = 1.0
		self.m_f.write('<circle cx="%.3f" cy="%.3f" r="%.3f"/>\n' % (circle.m_center[0], circle.m_center[1], circle.m_radius) )
		if circle.m_label is not None :
			self.m_f.write('<text x="%.3f" y="%.3f">%s</text>\n' % (circle.m_center[0], circle.m_center[1], point.m_label) )
				  
	def visitImage(self, image):
		imageSize = image.getSize()
		self.m_f.write('<image xlink:href="%s" x="0" y="0" width="%d" height="%d"/>\n' % (image.getFilePath().split('/')[-1], imageSize[1], imageSize[0]) )
		
	def visitLayer(self, layer):
		self.m_f.write('<g id="%s" style="fill:red;stroke:cyan">\n' % layer.getName())
		for child in layer.m_children:
			child.onVisit( self )
		for layer in layer.m_layers.itervalues():
			layer.onVisit( self )
		self.m_f.write('</g>\n')
	
	def visitScene(self, scene):
		with open(self.m_svgFilePath, 'wt') as self.m_f:
			print('exporting scene2d as %s' % self.m_svgFilePath)
			self.m_f.write('<?xml version="1.0"?>')
			self.m_f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="3008" height="2280" onload="init()">')
			self.m_f.write('<defs>')
			self.m_f.write('<script type="text/ecmascript" xlink:href="MeniscusUI.js"/>')
			self.m_f.write('</defs>')
			if scene.m_image is not None:
				scene.m_image.onVisit(self)
			
			scene.m_rootLayer.onVisit(self)
			#f.write('<image xlink:href="FullImage0235.png" x="0" y="0" width="3008" height="2280"/>')	
			self.m_f.write('</svg>')
		

