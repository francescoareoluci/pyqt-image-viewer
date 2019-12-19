# Image Viewer

Author: Francesco Areoluci

This python application is an image viewer which support visualization of EXIF data.
It is build with pyqt framework and it relies on qml language to structure the view.

Features:
- Single image viewer
- Folder selection for multiple image view
- Image rotation by 90 degrees steps
- Image EXIF data view
- Google Maps position display
- Hotkeys
- Responsive window

Dependencies:
- exifread

In order to install this dependency:
- Using Anaconda as an environment manager:

```
conda install -c conda-forge exifread
```

How to launch this application:
```
python ImageViewer.py
```

How to use:

Once the application has been started, you can select an image to be viewed by clicking
on the button 'Choose an image' or you can select a folder to view all the images
in that folder by clicking on the button 'Select a folder'.
Once an image has been loaded you can rotate it left/right by 90 degrees steps by using
the controls located in the bottom of the image. 
If you have opened a folder and more than one image is stored on the folder, 
you can switch between images using the controls located in the bottom of the image.
If an image has some exif data stored, you can view them by clicking on the button 'View EXIF data'.
If an image contains geolocalization tags, by clicking on Latitude or Longitude entry a default
browser will be opened and position will be displayed in a Google Maps page. 

Hotkeys:

- Ctrl+f: open folder selection
- Ctrl+i: open single image selection
- Ctrl+e: open exif visualization (if exif data are available)
- Ctrl+r: right rotate the image
- Ctrl+l: left rotate the image
- Left arrow: display the previous image (if the selected folder contains more than one image)
- Right arrow: display the next image (if the selected folder contains more than one image)

Doxygen documentation:

This application support Doxygen doc generation.
In order to automatically generate documentation, if you have installed Doxygen, run the following command:

```
doxygenn doxy
```

If you don't have installed Doxygen, you can check out this how to: http://www.doxygen.nl/download.html