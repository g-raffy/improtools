var gXmlns = 'http://www.w3.org/2000/svg';
var svgDoc = document;
var evCounter = 0;
var gRootLayersControlNode;

function getImageSize()
{
	var anImageNode = svgDoc.getElementsByTagName('image')[0];
	var width = anImageNode.getAttribute('width');
	var height = anImageNode.getAttribute('height');
	var size = new Object;
	size.width = parseInt(width);
	size.height = parseInt(height);
	return size;
}

function ImageArea_onMouseMove(evt)
{
	var oObj = evt.target;
	var sObjID = oObj.getAttributeNS(null,'id');
	//nAgeBand = parseInt(sObjID.substring(1,3));
	if (evt.type=='mousemove')
	{
		//var cursor_coords = svgDoc.getElementById('cursor_coords.x');
		//cursor_coords.setAttributeNS(null,'style','fill:none;stroke:#80ffff');// evt.clientX
		//cursor_coords.firstChild.data=evt.clientX;
		svgDoc.getElementById('cursor_coords.x').firstChild.data='x :' + evt.clientX;
		svgDoc.getElementById('cursor_coords.y').firstChild.data='y :' + evt.clientY;
		svgDoc.getElementById('popup').setAttributeNS(null,'transform','translate('+evt.clientX+','+evt.clientY+')');
		svgDoc.getElementById('popup').setAttribute('display','inline');
	}//end mouseover
	evCounter++;	
}

function ImageArea_onMouseOut(evt)
{
	//alert( 'out' );
	var oObj = evt.target;
	var sObjID = oObj.getAttributeNS(null,'id');
	//nAgeBand = parseInt(sObjID.substring(1,3));
	if (evt.type=='mouseout')
	{
		svgDoc.getElementById('popup').setAttribute('display','none');
	}//end mouseover
	evCounter++;	
}

function getNodeDesc( xmlNode )
{
	return xmlNode.nodeName + '(id=' + xmlNode.getAttribute('id') + ')';
}

function SwitchButton_new( buttonName )
{
	var buttonNode = svgDoc.createElementNS(gXmlns,'circle');
	buttonNode.setAttribute('id', buttonName);
	buttonNode.setAttribute('cx', '0');
	buttonNode.setAttribute('cy', '0');
	buttonNode.setAttribute('r', '4');
	//buttonNode.setAttribute('onclick', 'LayerControlNode_onExpandClick(evt);');
	buttonNode.setAttribute('isEnabled', 'true');
	return buttonNode;
}

function SwitchButton_isEnabled( buttonNode )
{
	if( buttonNode.getAttribute('isEnabled') == 'true' )
	{
		return true;
	}
	else
	{
		return false;
	}
}

function SwitchButton_enable( buttonNode, bEnable )
{
	if( bEnable )
	{
		buttonNode.setAttribute('isEnabled', 'true');
		var callback = buttonNode.getAttribute('onButtonPress');
		if( callback )
		{
			buttonNode.setAttribute('onclick', callback);
		}
		buttonNode.removeAttribute('opacity');
	}
	else
	{
		buttonNode.setAttribute('isEnabled', 'false');
		var callback = buttonNode.getAttribute('onclick');
		if( callback )
		{
			buttonNode.removeAttribute('onclick');
		}
		buttonNode.setAttribute('opacity', '0.5');
	}
}

function SwitchButton_setPosition( buttonNode, x, y )
{
	buttonNode.setAttribute('cx', x);
	buttonNode.setAttribute('cy', y);
	return buttonNode;
}

function SwitchButton_setState( buttonNode, state )
{
	if( state == 'on' )
	{
		buttonNode.setAttribute('fill','cyan');
	}
	else if( state == 'off')
	{
		buttonNode.setAttribute('fill','grey');
	}
	else
	{
		assert(false);
	}
}

function SwitchButton_setVisible( buttonNode, bVisibility )
{
	if( bVisibility )
	{
		buttonNode.setAttribute('display','inline');
	}
	else
	{
		buttonNode.setAttribute('display','none');
	}
}

function SwitchButton_setOnButtonPressCallback( buttonNode, callback )
{
	buttonNode.setAttribute('onButtonPress', callback);
	SwitchButton_enable(buttonNode, SwitchButton_isEnabled( buttonNode )); // refresh
}

function RefreshLayersControlsBranch( layerControlsBranch )
{
	var myHeight = 15;
	var numChildren = layerControlsBranch.childNodes.length;
	var iChild;
	var expandButtonNode = null;
	var numChildrenLayers = 0;
	for( iChild = 0 ; iChild < numChildren ; iChild++)
	{
		var childNode = layerControlsBranch.childNodes.item(iChild);
		if( childNode.nodeName == 'g' )
		{
			if( layerControlsBranch.getAttribute('expanded') == 'true' )
			{
				childNode.setAttribute('display', 'inline');
				childNode.setAttribute('transform', 'translate(10,'+myHeight+')')
				myHeight += RefreshLayersControlsBranch( childNode );
			}
			else
			{
				childNode.setAttribute('display', 'none');
			}
			numChildrenLayers++;
		}
		else if( childNode.getAttribute('id') == 'expandButton' )
		{
			expandButtonNode = childNode;
			if( layerControlsBranch.getAttribute('expanded') == 'true' )
			{
				SwitchButton_setState(childNode, 'on');
			}
			else
			{
				SwitchButton_setState(childNode, 'off');
			}
		}
		else if( childNode.getAttribute('id') == 'toggleVisibilityButton' )
		{
			var layerName = layerControlsBranch.getAttribute( 'controlledLayerName' );
			if( layerName != '<noname>' )
			{
				var layerNode = svgDoc.getElementById(layerName);
				//alert('layerNode : '+getNodeDesc(layerNode));
				if( layerNode.getAttribute('display') == 'inline' )
				{
					SwitchButton_setState(childNode, 'on');
					
				}
				else
				{
					SwitchButton_setState(childNode, 'off');
				}
			}
			else
			{
				SwitchButton_setState(childNode, 'on');
			}
		}
	}
	// disable the expand button if there are no children layers
	if( numChildrenLayers == 0 )
	{
		SwitchButton_enable( expandButtonNode, false );
	}
	else
	{
		SwitchButton_enable( expandButtonNode, true );
	}
	return myHeight;
}

function RefreshLayersControls( )
{
	RefreshLayersControlsBranch( svgDoc.getElementById('layers'), 0 );
}

function LayerControlNode_onExpandClick( evt )
{
	//alert('clic');
	var buttonNode = evt.target;
	var controlNode = buttonNode.parentNode;
	//alert('controlNode : '+getNodeDesc(controlNode));
	//var sObjID = oObj.getAttributeNS(null,'id');
	if( controlNode.getAttribute('expanded') == 'true' )
	{
		//alert('folding : '+getNodeDesc(controlNode));
		controlNode.setAttribute('expanded','false');
		//buttonNode.setAttribute('fill','black');
	}
	else
	{
		//alert('expanding : '+getNodeDesc(controlNode));
		controlNode.setAttribute('expanded','true');
		//buttonNode.setAttribute('fill','red');
	}
	RefreshLayersControlsBranch(gRootLayersControlNode);
}

function LayerControlNode_onToggleVisibilityClick( evt )
{
	var buttonNode = evt.target;
	var controlNode = buttonNode.parentNode;
	var layerName = controlNode.getAttribute('controlledLayerName');
	if( layerName != '<noname>' )
	{
		var layerNode = svgDoc.getElementById(layerName);
		//alert('layerNode : '+getNodeDesc(layerNode));
		if( layerNode.getAttribute('display') == 'inline' )
		{
			layerNode.setAttribute('display','none');
		}
		else
		{
			layerNode.setAttribute('display','inline');
		}
	}
	RefreshLayersControlsBranch(gRootLayersControlNode);
}

function CreateLayerControlNode( controlledGroupNode )
{
	

	var layerName = controlledGroupNode.getAttribute('id');
	if( ! layerName )
	{
		layerName = '<noname>';
	}
	//alert( 'CreateLayerControlNode : layer : ' + layerName );
	
	var controlNode = svgDoc.createElementNS(gXmlns,'g');
	controlNode.setAttribute('id', layerName + '_controller');
	controlNode.setAttribute('expanded', 'false');
	controlNode.setAttribute('controlledLayerName', layerName);

	var textNode = svgDoc.createElementNS(gXmlns,'text');
	textNode.setAttribute('x', '20');
	textNode.setAttribute('y', '5');
	textNode.setAttribute('fill', 'grey');
	textNode.appendChild( svgDoc.createTextNode( layerName ) );

	//alert( 'parentLayerControl : ' + getNodeDesc(parentLayerControl) );
	controlNode.appendChild( textNode );

	var expandButton = SwitchButton_new( 'expandButton' );
	SwitchButton_setPosition( expandButton, 0, 0 );
	SwitchButton_setOnButtonPressCallback( expandButton, 'LayerControlNode_onExpandClick(evt);' );
	controlNode.appendChild( expandButton );
	
	var toggleVisibilityButton = SwitchButton_new( 'toggleVisibilityButton' );
	SwitchButton_setPosition( toggleVisibilityButton, 10, 0 );
	SwitchButton_setOnButtonPressCallback( toggleVisibilityButton, 'LayerControlNode_onToggleVisibilityClick(evt);' );
	controlNode.appendChild( toggleVisibilityButton );
	
	return controlNode;
}


function CreateLayerControlsBranch( groupNode )
{
	//alert('CreateLayerControls : buidling controls for group tree ' + getNodeDesc(groupNode) );
	var controlNode = CreateLayerControlNode( groupNode );
	//alert('created controller : '+getNodeDesc( controlNode ));
	var numChildren = groupNode.childNodes.length;
	if( numChildren < 50 ) // the contour_points layer has a subgroup per pillar
	{
		//alert( 'num Children : ' + numChildren );
		var iChild;
		for( iChild = 0 ; iChild < numChildren ; iChild++)
		{
			var childNode = groupNode.childNodes.item(iChild);
			//alert( 'childNode.nodeName = ' + childNode.nodeName );
			//var childId = childNode.getAttribute('id');
			if( (childNode.nodeName == 'g') && ( childNode.getAttribute('id') != 'layers' ) )
			{
				//alert( 'id : ' + childNode.getAttribute('id') );
				
				var childControlNode = CreateLayerControlsBranch( childNode );
				/*
				alert( 'created controls branch for id : ' + childNode.getAttribute('id') );
				alert( 'controlNode = '+getNodeDesc( controlNode ));
				alert( 'childControlNode = '+getNodeDesc(childControlNode));
				*/
				controlNode.appendChild( childControlNode );
				//alert( 'after adding child control to parent' );
			}
		}
	}
	return controlNode;
}

function Test()
{
	var g1 = svgDoc.createElementNS(gXmlns,'g');
	var g2 = svgDoc.createElementNS(gXmlns,'g');
	var g3 = svgDoc.createElementNS(gXmlns,'g');
	g2.appendChild(g3);
	g1.appendChild(g2);
}

function init()
{
	console.log('init');
	var cursor_coords = svgDoc.getElementById('cursor_coords');
	
	var svgNode = svgDoc.childNodes[0];
	
	var imageSize = getImageSize();
	
	// expand the size of the svg to allow for the panel on the right han side
	var panelWidth = 300;
	svgNode.setAttribute( 'width', imageSize.width + panelWidth )
	
	// create the layers node as the child of svg node. This node will contain the control buttons for layers
	{
		var layersNode = svgDoc.createElementNS(gXmlns,'g');
		layersNode.setAttribute('id', 'layers');
		layersNode.setAttribute('transform', 'translate('+(imageSize.width+10)+',32)');

		var backgroundNode = svgDoc.createElementNS(gXmlns,'rect');
		backgroundNode.setAttribute('x', '-10');
		backgroundNode.setAttribute('y', '-32');
		backgroundNode.setAttribute('width', panelWidth);
		backgroundNode.setAttribute('height', imageSize.height);
		backgroundNode.setAttribute('fill', 'black');
		layersNode.appendChild( backgroundNode );
		
		svgNode.appendChild( layersNode );
	}
	
	// create the hovering window that will display pixel position
	{
		var popupNode = svgDoc.createElementNS(gXmlns,'g');
		popupNode.setAttribute('id', 'popup');
		popupNode.setAttribute('transform', 'translate(100,16)');
		popupNode.setAttribute('display', 'none');

		var backgroundNode = svgDoc.createElementNS(gXmlns,'rect');
		backgroundNode.setAttribute('x', '10');
		backgroundNode.setAttribute('y', '10');
		backgroundNode.setAttribute('width', '50');
		backgroundNode.setAttribute('height', '40');
		backgroundNode.setAttribute('rx', '5');
		backgroundNode.setAttribute('ry', '5');
		backgroundNode.setAttribute('fill', '#80ffff');
		backgroundNode.setAttribute('opacity', '0.5');
		//backgroundNode.setAttribute('onmousemove', 'TellMe(evt)');
		popupNode.appendChild( backgroundNode );

		var textNode = svgDoc.createElementNS(gXmlns,'text');
		textNode.setAttribute('id', 'cursor_coords.x');
		textNode.setAttribute('x', '15');
		textNode.setAttribute('y', '25');
		textNode.appendChild( svgDoc.createTextNode( 'undefined' ) );
		popupNode.appendChild( textNode );
		
		var textNode = svgDoc.createElementNS(gXmlns,'text');
		textNode.setAttribute('id', 'cursor_coords.y');
		textNode.setAttribute('x', '15');
		textNode.setAttribute('y', '45');
		textNode.appendChild( svgDoc.createTextNode( 'undefined' ) );
		popupNode.appendChild( textNode );
		
		svgNode.appendChild( popupNode );
	}
	// create a rect that will capture mousemove
	
	{
		var mouseMoveCaptureNode = svgDoc.createElementNS(gXmlns,'rect');
		mouseMoveCaptureNode.setAttribute('x', '0');
		mouseMoveCaptureNode.setAttribute('y', '0');
		mouseMoveCaptureNode.setAttribute('width', imageSize.width);
		mouseMoveCaptureNode.setAttribute('height', imageSize.height);
		mouseMoveCaptureNode.setAttribute('fill', 'grey');
		mouseMoveCaptureNode.setAttribute('opacity', '0.0');
		mouseMoveCaptureNode.setAttribute('onmousemove', 'ImageArea_onMouseMove(evt)');
		mouseMoveCaptureNode.setAttribute('onmouseout', 'ImageArea_onMouseOut(evt)');
		svgNode.appendChild( mouseMoveCaptureNode );
	}
	
	var controlNode = CreateLayerControlsBranch( svgDoc.childNodes[0] );
	svgDoc.getElementById('layers').appendChild( controlNode );
	gRootLayersControlNode = controlNode;
	RefreshLayersControlsBranch(controlNode);
	
}
