/**
 * SVLib
 * @version 0.1
 * @author Nick Chapman
 * email: nick@servervoodoo.com
 */


/**
 * Initiates the library object
 */

var SVLib = {};

/**
 * Loads different sized images based on screen width
 * 
 * Leave <img>'s src attribute as ""
 * 
 * Screen size descriptors:
 *  	small: 500< px
 *  	mid  : 501-1000 px
 *  	avg  : 1001-1500 px
 *  	big  : 1501 - 2000 px
 *  	huge : 2001> px
 * 
 * @param {object} img - An object that holds the links to the different image sizes
 * @param {int} developer - An option which will log messages to console when enabled (enabled = 1)
 * 
 * see http://github.com/ServerVoodoo/SVLib/wiki for usage notes and examples
 */
SVLib.scaleImg = function(img , developer){
	var width = window.innerWidth;
	var size = ""; //Image size that will be used
	var min  = 5; //Smallest available size
	var max = 0;  //Largest available size
	var sizes = ['small','mid','avg','big','huge'];
	//determine current screen size
	switch (true){
		case (width <= 500):
			size = "small";
			break;
		case (width <=1000):
			size = "mid";
			break;
		case (width <= 1500):
			size = "avg";
			break;
		case (width <= 2000):
			size = "big";
			break;
		case (width > 2000):
			size = "huge";
			break;
	}
	if(typeof developer !== 'undefined'){
		console.log("Window size: " + size);
	}
	//Finding smallest and largest images provided
	for(var propt in img){
    	var index = sizes.indexOf(propt);
    	if(index != -1){
        	if(index < min){
            	min = index;
        	}
        	if(index > max){
            	max = index;
    		}
		}
	};
	//Chceking to ensure best available image is used
	if(sizes.indexOf(size) < min){
		size = sizes[min];
	}
	if(sizes.indexOf(size) > max){
		size = sizes[max];
	}
	if(typeof developer !== 'undefined'){
		console.log("Minimum: " + sizes[min] + ". Maximum :" + sizes[max]);	
	}
	return img[size];
};

/**
 * Applies the SVLib.scaleImg() function to the <img> with the provided id
 * 
 * See SVLib.scaleImg for image params
 * 
 * @param {object} img
 * @param {int} developer - An option which will log messages to console when enabled (enabled = 1)
 *
 * see http://github.com/ServerVoodoo/SVLib/wiki for usage notes and examples
 */
SVLib.scaleBySelector = function(img, developer){
	var imageLink = SVLib.scaleImg(img,developer);
	if(img.id && document.getElementById(img.id).src != imageLink){
		document.getElementById(img.id).src = imageLink;
	}
	else if(img.class){
		var pictures = document.getElementsByClassName(img.class);
		if(pictures[0].src != imageLink){
			for(var zxc = 0; zxc < pictures.length; zxc++){
				pictures[zxc].src = imageLink;
			}
		}
	}
	else if(typeof developer !== 'undefined'){
		console.log('SVLib.scaleBySelector was unable to select an image');
	}
};


/**
 * Determines the width and height of the browser window once the page loads. 
 * 
 * Based on the StackOverflow post here:
 *     http://stackoverflow.com/questions/4976936/get-the-available-browser-window-size-clientheight-clientwidth-consistently-ac
 * 
 * NOTE: Cannot be used accurately until after the document has finished loading
 * 
 * Use as SVLib.getWindowSize().width;
 */
SVLib.getWindowSize = function() {
	var docEl = document.documentElement,
    	IS_BODY_ACTING_ROOT = docEl && (docEl.clientHeight === 0);

	// Used to feature test Opera returning wrong values 
	// for documentElement.clientHeight. 
	function isDocumentElementHeightOff () { 
		var d = document, div = d.createElement('div');
		div.style.height = "2500px";
		d.body.insertBefore(div, d.body.firstChild);
		var r = d.documentElement.clientHeight > 2400;
		d.body.removeChild(div);
		return r;
	}

	if (typeof document.clientWidth == "number") {
		return { width: document.clientWidth, height: document.clientHeight };
	} else if (IS_BODY_ACTING_ROOT || isDocumentElementHeightOff()) {
		var b = document.body;
		return { width: b.clientWidth, height: b.clientHeight };
	} else {
		return { width: docEl.clientWidth, height: docEl.clientHeight };
	}
};