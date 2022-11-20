# Image Viewer

This python application is an image viewer which support visualization of EXIF data.
It is build with pyqt framework and it relies on qml language to structure the view.

The application features:
- Single image viewer
- Folder selection for multiple image view
- Image rotation by 90 degrees steps
- Image EXIF data view
- Google Maps position display
- Hotkeys
- Responsive window

## Dependencies

Major dependencies:
- pyqt
- exifread

Using Anaconda as environment manager, you can install these dependencies as:

```
conda install -c anaconda pyqt
conda install -c conda-forge exifread
```

## Usage

Once the environment has been set up, the application can be launched with:

```
python ImageViewer.py
```

### How to use:

Once the application has been started, you can select an image to be viewed by clicking
on the button 'Choose an image' or you can select a folder to view all the images
in that folder by clicking on the button 'Select a folder'.
Once an image has been loaded you can rotate it left/right by 90 degrees steps by using
the controls located in the bottom of the image.
The image can be resized by resizing the application window.
If you have opened a folder and more than one image is stored on the folder, 
you can switch between images using the controls located in the bottom of the image.
If an image has some exif data stored, you can view them by clicking on the button 'View EXIF data'.
If an image contains geolocalization tags, by clicking on Latitude or Longitude entry a
browser will be opened and position will be displayed in a Google Maps page.

## Hotkeys

- Ctrl+f: open folder selection
- Ctrl+i: open single image selection
- Ctrl+e: open exif visualization (if exif data are available)
- Ctrl+r: right rotate the image
- Ctrl+l: left rotate the image
- Left arrow: display the previous image (if the selected folder contains more than one image)
- Right arrow: display the next image (if the selected folder contains more than one image)

Supported image formats:

This application supports the following image formats: jpeg, png, tiff.

## Documentation:

This application support Doxygen doc generation.
In order to automatically generate documentation, if you have installed Doxygen, run the following command:

```
doxygenn doxy
```

If you don't have installed Doxygen, you can follow the instructions at this link; http://www.doxygen.nl/download.html

## Testing

This application has been tested on Ubuntu 18.04 and Windows 10.