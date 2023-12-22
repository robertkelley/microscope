
from picamera2 import Picamera2
from picamera2 import Preview
from signal import pause

from libcamera import Transform
from gpiozero import Button
# import time


# button_on = Button(2)
button_up = Button(3)
button_down = Button(4)

camera = Picamera2()
camera.start_preview(Preview.QTGL, x=300, y = 300, width=700, height=700, 
                    transform = Transform(hflip = 1, vflip = 1))

# camera.start_preview(Preview.DRM, x=100, y = 100, width=2000, height=2000, 
#                  transform = Transform(hflip = 1, vflip = 1))

preview_config = camera.create_preview_configuration({"size": (700,700)})    # below 700 seems to magnify the image   

camera.configure(preview_config)

# camera.start_preview(Preview.QTGL)
#camera.configure()
camera.start()

# print("pereview config ", Preview)


print( "Meta data  " ,camera.capture_metadata())


 

# How to do digital zoom using the "ScalerCrop" control.

def camera_up():


    size = camera.capture_metadata()['ScalerCrop'][2:]
    print(" Size after camera initialized   a  :-",  size)  

    full_res = camera.camera_properties['PixelArraySize']

    print("Before camera up  full res :-  ", full_res , "   Size   :-", size) 
    
    for _ in range(20):
        # This syncs us to the arrival of a new camera frame:
        camera.capture_metadata()

        size = [int(s * 0.95) for s in size]
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
        camera.set_controls({"ScalerCrop": offset + size})

    print(" After camera up     Offset':-  ", offset, "  full res  :- ",  full_res , "  Size  :- ", size)   
        
# def cameraTest_up():
#     size = camera.capture_metadata()['ScalerCrop'][2:0]


def camera_down():

    size = camera.capture_metadata()['ScalerCrop'][2:]

    full_res = camera.camera_properties['PixelArraySize']

    print("Before camera down  full res :-  ", full_res , "   Size   :-", size) 

    for _ in range(20):
        # This syncs us to the arrival of a new camera frame:
        camera.capture_metadata()

        size = [int(s * 1.05) for s in size]           #       0.95   =>   1.05
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]     
        camera.set_controls({"ScalerCrop": offset + size})      

    print(" After camera down     Offset':-  ", offset, "  full res  :- ",  full_res , "  Size  :- ", size)    



# button_on.when_pressed = camera_on
button_up.when_pressed = camera_up
button_down.when_pressed = camera_down

pause()
