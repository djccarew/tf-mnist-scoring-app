/** 
 * Copyright 2017 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
**/
 
/*
 * This function processes the  input canvas created by the user 
 * It normalizes the input digit by scaling it to 20x20 and then centering it within a 
 * 28x28 canvas. 
 * It also convert the RGB values used by the HTML5 canvas object to raw pixel values  to match the MNIST  * training data (0 represents  the background color)
 *
 */
function processImage(srcCanvas, destCanvas) {
    var minx = srcCanvas.width, miny = srcCanvas.height, maxx = 0, maxy = 0;
    var mincol = srcCanvas.width, minrow = srcCanvas.height, maxrow = 0, maxcol = 0;
	var red, green, blue;
	var boundingHeight, boundingWidth, boundingX, boundingY;
	var redraw = false;
	var srcCtx = srcCanvas.getContext("2d");
	var destCtx = destCanvas.getContext("2d");
	var srcImageData = srcCtx.getImageData(0, 0, srcCanvas.width, srcCanvas.height);
	var imageWidth  = srcImageData.width;
	var destImageData;
	var featureIndex = 0;
    // Feature array is a flattened row oriented representation of a 28x28 image
    // We initialize it to 0's  to be consistent with the MNIST training data 
	var features = new Array(784);
    for (i = 0; i < features.length; i++) {
        features[i] = 0;
    }

	
	// Find a minimal bounding rectangle around the digit entered by looking for nonwhite pixels
	// Top left of bounding rectangle will be at (minx, miny) and bottom right will be (maxx, maxy)
    for (var y = 0; y < srcCanvas.height; y++) {
       for (var x = 0; x < srcCanvas.width; x++) {    
	      var idx = ((imageWidth * y) + x) * 4;		 
	      var red = srcImageData.data[idx];
	      var green = srcImageData.data[idx + 1];
          var blue = srcImageData.data[idx + 2];
		
          if (red != 255 || green != 255 || blue != 255) {
		     if (x < minx) {			  
				//console.log("Updating minx x,y = " + x + "," + y +  " old minx = " + minx);
			    minx = x ;
			 }	
			if (x > maxx)	
			    maxx = x;
		    if (y < miny) {
				//console.log("Updating miny x,y = " + x + "," + y +  " old miny = " + miny);
			    miny = y;
			}	
		    if (y > maxy)	
			    maxy =y;
				
		  }
		}
    } 	
	

	console.log("min x, min y, maxx, maxy " + minx + " " + miny + " " + maxx + " " + maxy + " ");
    boundingHeight = maxy - miny;
	boundingWidth = maxx - minx;
	// Convert bounding rectangle to bounding square
	// If there is not enough room on the canvas we have to center the bounding box and redraw
	if (boundingHeight < boundingWidth) { // Need to expand height to make it a square
	   if (((miny - ((boundingWidth - boundingHeight)/2)) < 0) || ((maxy + ((boundingWidth - boundingHeight)/2)) > srcCanvas.height)) {
		  console.log("Not enough vertical room to form bounding square repositioning and redrawing ..."); 
	
	      redraw = true;
	   } 
	   else {
		  console.log("Expanding height to make it a square");
		  var halfDiff = (boundingWidth - boundingHeight)/2;
          boundingY = 	miny -  halfDiff;
		  boundingX = minx;
          boundingHeight = boundingWidth;
	      //console.log("boundingX " + boundingX + " minx " + minx +  " boundingY " + boundingY + " half diff " + halfDiff + " height " + boundingHeight + " width " + boundingWidth);
       }		  
	}
	else if (boundingWidth < boundingHeight) { // Need to expand width to make it a square 
	   if (((minx - ((boundingHeight - boundingWidth)/2)) < 0) || ((maxx + ((boundingHeight - boundingWidth)/2)) > srcCanvas.width)) {
		  console.log("Not enough horizontal room to form bounding square repositioning and redrawing ...");  
		
	      redraw = true;
	   }	
       else {
		  console.log("Expanding width to make it a square");
		  var halfDiff = (boundingHeight - boundingWidth)/2;
	      boundingX = minx - ((boundingHeight - boundingWidth)/2);
		  boundingY = miny;
		  boundingWidth = boundingHeight;		  
	     // console.log("boundingX " + boundingX + " minx " + minx + " boundingY " + boundingY + " half diff " +  halfDiff+ " height " + boundingHeight + " width "+ boundingWidth);
		 
	   }	   
	}
	else {
	   boundingX = minx;
	   boundingY = miny;
	} 
	console.log("boundingX, boundingY, boundingWidth, boundingHeight " + boundingX + " " + boundingY + " " + boundingWidth + " " + boundingHeight);
	
	if (redraw) { // if we have to redraw center bounding rectangle in center of canvas
	   var middleX = minx + (boundingWidth/2);
	   var middleY = miny  + (boundingHeight/2);
	   var redrawX = minx, redrawY = miny;
	   var imageData;
	   
	   // calculate distance from center of bounding rectangle  to center of canvas  ie  (83, 83)
	   // to determine how far to move the bounding rect in the canvas
	   if (middleX > 70) 
		  redrawX = minx - (middleX - 70);
	   else if (middleX < 70)	 
		  redrawX = minx + (70 - middleX);
	   if (middleY > 70)
			redrawY = miny - (middleY - 70);	
	   else if (middleY < 70)	 
		  redrawY = miny + (70 - middleY); 	
		  
	   // Save canvas, clear it and then redraw to new coordinates	  
	   imageData = srcCtx.getImageData(minx, miny, boundingWidth, boundingHeight);
	   srcCtx.clearRect(0, 0, srcCanvas.width, srcCanvas.height);
	   srcCtx.fillStyle="#FFFFFF";
	   srcCtx.fillRect(0,0, srcCanvas.width,  srcCanvas.height);
	   srcCtx.putImageData(imageData, redrawX, redrawY);	
	  // With bounding rectangle centered in canvas we can expand it to make a bounding square
	   if (boundingHeight < boundingWidth) {
		  boundingY = 	redrawY -  ((boundingWidth - boundingHeight)/2);
		  boundingHeight = boundingWidth;
		  boundingX = redrawX;
	   }
	   else {
		  boundingX = redrawX - ((boundingHeight - boundingWidth)/2);
		  boundingWidth = boundingHeight;
		  boundingY = redrawY;
	   }
	   
	   console.log("Redrawing to " + redrawX + "," + redrawY );
		 
	
	}
	else 
		console.log("Bounding square fits in canvas skipping redraw");
	
	// Scale image to fit in 20x20 square centred in the destination canvas to be compatible with MNIST data
	// MNIST  data is white foreground  on a black background  so we have to invert the pixels from the on screen canvas
	// (which is a black foreground on a white background)
	
	// Fill dest canvas with white background
	destCtx.fillStyle="#FFFFFF";
	destCtx.fillRect(0,0, destCanvas.width,  destCanvas.height);
	// Scale bounding box around our digit and fit it in the 20x20 middle of the 28x28 destination canvas
	
	destCtx.drawImage(srcCanvas, boundingX, boundingY, boundingWidth, boundingHeight, 4, 4, destCanvas.width - 8, destCanvas.height - 8);
 
	destImageData = destCtx.getImageData(0, 0, destCanvas.width, destCanvas.height);
	
	for (var y = 0; y < destCanvas.height; y++) {
       for (var x = 0; x < destCanvas.width; x++) {    
	      var idx = ((destCanvas.width * y) + x) * 4;
         
		//  Convert RGB values to pixel values in  the MNIST data format
        //  RGB(255,255,255) or white  is converted to 0 
        //  RGB(0,0,0) or black is converted to 255 
        // 
		  var pixelFromRGB = 255 -  Math.round((destImageData.data[idx] * 0.299) + (destImageData.data[idx+1] * 0.587) + (destImageData.data[idx+2] * 0.114));
	      if (pixelFromRGB > 0) {			
			   featureIndex = (y*28) + x; 
			   features[featureIndex] = pixelFromRGB;
		  }
        
		}
    } 	
		 
	destCtx.putImageData(destImageData, 0, 0);
	console.log('features ' + JSON.stringify(features));
	

	return features;

}

// Used to format response received from scoring service
// Ignores predictions if confidence level is below 85%
function formatResponse(response, isError) {
    //console.log("formatResponse " + JSON.stringify(response))
	if (!isError) {
        var confidence = (response.probability * 100).toFixed(2);
        if (confidence  >= 85.00)
		   return "Value predicted: " + response.digit + " Confidence: " + confidence + "%" ;
        else
           return "Value predicted: n/a (confidence is too low)  Confidence: " + confidence + "%"  ;
	}
	else 
		return "Error from server: " + response;
}