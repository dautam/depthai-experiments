from depthai_sdk import OakCamera, AspectRatioResizeMode

with OakCamera() as oak:
    color = oak.create_camera('color')
    nn = oak.create_nn('mobilenet-ssd', color)
    nn.config_nn(aspect_ratio_resize_mode=AspectRatioResizeMode.LETTERBOX)
    oak.create_visualizer([color, nn], fps=True)
    oak.start(blocking=True)