Image Viewer
Author: Francesco Areoluci

This python application is an image viewer which support visualization of EXIF data.
It is build with pyqt framework and it relies on qml language to structure the view.

Functionalities:
- Single image viewer
- Folder selection for multiple image view
- Image rotation by 90 degrees steps
- Image EXIF data view
- Responsive window

Dependencies:
- exifread

In order to install this dependency:
- Using Anaconda as an environment manager:
> conda install -c conda-forge exifread

To launch this application:
> python ImageViewer.py

How to use:
Once the application has been started, you can select an image to be viewed by clicking
on the button 'Choose an image' or you can select a folder to view all the images
in that folder by clicking on the button 'Select a folder'.
Once an image has been loaded you can rotate it left/right by 90 degrees steps by using
the controls located in the bottom of the image. If you have opened a folder and more than
one image is stored on the folder, you can switch between images using the controls located 
in the bottom of the image.
If an image has some exif data stored, you can view them by clicking on the button 'View EXIF data'.

Doxygen documentation:
This application support Doxygen doc generation.
In order to automatically generate documentation, if you have installed Doxygen, run the following command:
> doxygenn doxy
If you don't have installed Doxygen, you can check out this how to: http://www.doxygen.nl/download.html