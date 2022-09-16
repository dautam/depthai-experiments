import os.path

import depthai as dai
import cv2
import serial
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QAbstractSpinBox
import os
import time

colorMode = QtGui.QImage.Format_RGB888
try:
    colorMode = QtGui.QImage.Format_BGR888
except:
    colorMode = QtGui.QImage.Format_RGB888

CSV_HEADER = "TimeStamp,MxID,RealDistance,DetectedDistance,planeFitMSE,gtPlaneMSE,planeFitRMSE," \
             "gtPlaneRMSE,fillRate,Result,Side"
mx_id = None
product = None
inter_conv = None


class Ui_DepthTest(object):
    def setupUi(self, DepthTest):
        DepthTest.setObjectName("DepthTest")
        DepthTest.resize(1074, 696)
        self.centralwidget = QtWidgets.QWidget(DepthTest)
        self.centralwidget.setObjectName("centralwidget")
        self.l_info = QtWidgets.QLabel(self.centralwidget)
        self.l_info.setGeometry(QtCore.QRect(30, 270, 221, 331))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_info.setFont(font)
        self.l_info.setStyleSheet("QLabel {\n"
"    .adjust-line-height {\n"
"        line-height: 1em;\n"
"    }\n"
"}")
        self.l_info.setObjectName("l_info")
        self.l_result = QtWidgets.QLabel(self.centralwidget)
        self.l_result.setGeometry(QtCore.QRect(110, 230, 101, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.l_result.setFont(font)
        self.l_result.setText("")
        self.l_result.setObjectName("l_result")
        self.b_start = QtWidgets.QPushButton(self.centralwidget)
        self.b_start.setGeometry(QtCore.QRect(640, 550, 151, 71))
        self.b_start.setObjectName("b_start")
        self.l_test = QtWidgets.QLabel(self.centralwidget)
        self.l_test.setGeometry(QtCore.QRect(20, 40, 231, 81))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.l_test.setFont(font)
        self.l_test.setObjectName("l_test")
        self.l_lidar = QtWidgets.QLabel(self.centralwidget)
        self.l_lidar.setGeometry(QtCore.QRect(270, 300, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_lidar.setFont(font)
        self.l_lidar.setObjectName("l_lidar")
        self.l_fill_rate = QtWidgets.QLabel(self.centralwidget)
        self.l_fill_rate.setGeometry(QtCore.QRect(270, 350, 71, 31))
        self.l_fill_rate.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(18)
        font.setUnderline(False)
        self.l_fill_rate.setFont(font)
        self.l_fill_rate.setObjectName("l_fill_rate")
        self.l_gt_plane_rmse = QtWidgets.QLabel(self.centralwidget)
        self.l_gt_plane_rmse.setGeometry(QtCore.QRect(270, 400, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_gt_plane_rmse.setFont(font)
        self.l_gt_plane_rmse.setObjectName("l_gt_plane_rmse")
        self.spin_manual = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_manual.setGeometry(QtCore.QRect(20, 140, 76, 36))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spin_manual.setFont(font)
        self.spin_manual.setObjectName("spin_manual")
        self.r_manual = QtWidgets.QRadioButton(self.centralwidget)
        self.r_manual.setGeometry(QtCore.QRect(110, 140, 201, 26))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.r_manual.setFont(font)
        self.r_manual.setObjectName("r_manual")
        self.r_sensor = QtWidgets.QRadioButton(self.centralwidget)
        self.r_sensor.setGeometry(QtCore.QRect(110, 190, 201, 26))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.r_sensor.setFont(font)
        self.r_sensor.setObjectName("r_sensor")
        self.l_sensor = QtWidgets.QLabel(self.centralwidget)
        self.l_sensor.setGeometry(QtCore.QRect(20, 190, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_sensor.setFont(font)
        self.l_sensor.setObjectName("l_sensor")
        self.preview_video = QtWidgets.QGraphicsView(self.centralwidget)
        self.preview_video.setGeometry(QtCore.QRect(410, 30, 640, 480))
        self.preview_video.setObjectName("preview_video")
        self.l_plane_fit_mse = QtWidgets.QLabel(self.centralwidget)
        self.l_plane_fit_mse.setGeometry(QtCore.QRect(270, 450, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_plane_fit_mse.setFont(font)
        self.l_plane_fit_mse.setObjectName("l_plane_fit_mse")
        self.l_gt_plane_mse = QtWidgets.QLabel(self.centralwidget)
        self.l_gt_plane_mse.setGeometry(QtCore.QRect(270, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_gt_plane_mse.setFont(font)
        self.l_gt_plane_mse.setObjectName("l_gt_plane_mse")
        self.l_gt_plane_mse_2 = QtWidgets.QLabel(self.centralwidget)
        self.l_gt_plane_mse_2.setGeometry(QtCore.QRect(270, 550, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.l_gt_plane_mse_2.setFont(font)
        self.l_gt_plane_mse_2.setObjectName("l_gt_plane_mse_2")
        self.board_group = QtWidgets.QGroupBox(self.centralwidget)
        self.board_group.setGeometry(QtCore.QRect(410, 520, 151, 131))
        self.board_group.setObjectName("board_group")
        self.r_left = QtWidgets.QRadioButton(self.board_group)
        self.r_left.setGeometry(QtCore.QRect(10, 30, 117, 26))
        self.r_left.setObjectName("r_left")
        self.r_right = QtWidgets.QRadioButton(self.board_group)
        self.r_right.setGeometry(QtCore.QRect(10, 90, 117, 26))
        self.r_right.setObjectName("r_right")
        self.r_center = QtWidgets.QRadioButton(self.board_group)
        self.r_center.setGeometry(QtCore.QRect(10, 60, 117, 26))
        self.r_center.setCheckable(True)
        self.r_center.setChecked(True)
        self.r_center.setObjectName("r_center")
        self.options_group = QtWidgets.QGroupBox(self.centralwidget)
        self.options_group.setGeometry(QtCore.QRect(900, 520, 151, 131))
        self.options_group.setObjectName("options_group")
        self.c_lrcheck = QtWidgets.QCheckBox(self.options_group)
        self.c_lrcheck.setGeometry(QtCore.QRect(10, 30, 97, 26))
        self.c_lrcheck.setChecked(True)
        self.c_lrcheck.setObjectName("c_lrcheck")
        self.c_extended = QtWidgets.QCheckBox(self.options_group)
        self.c_extended.setGeometry(QtCore.QRect(10, 90, 97, 26))
        self.c_extended.setObjectName("c_extended")
        self.c_subpixel = QtWidgets.QCheckBox(self.options_group)
        self.c_subpixel.setGeometry(QtCore.QRect(10, 60, 97, 26))
        self.c_subpixel.setChecked(True)
        self.c_subpixel.setObjectName("c_subpixel")
        DepthTest.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DepthTest)
        self.statusbar.setObjectName("statusbar")
        DepthTest.setStatusBar(self.statusbar)

        self.retranslateUi(DepthTest)
        QtCore.QMetaObject.connectSlotsByName(DepthTest)

    def retranslateUi(self, DepthTest):
        _translate = QtCore.QCoreApplication.translate
        DepthTest.setWindowTitle(_translate("DepthTest", "Depth Test"))
        self.l_info.setText(_translate("DepthTest", "<html>\n"
"<head/>\n"
"<body>\n"
"<div style=\"line-height:49px\">\n"
"<p align=\"right\">\n"
"LiDAR Depth:<br>\n"
"fillRate:<br>\n"
"gtPlaneRMSE:<br>\n"
"planeFitMSE:<br>\n"
"gtPlaneMSE:<br>\n"
"planeFitRMSE:</span></p>"))
        self.b_start.setText(_translate("DepthTest", "Start"))
        self.l_test.setText(_translate("DepthTest", "Depth Test"))
        self.l_lidar.setText(_translate("DepthTest", "-"))
        self.l_fill_rate.setText(_translate("DepthTest", "-"))
        self.l_gt_plane_rmse.setText(_translate("DepthTest", "-"))
        self.r_manual.setText(_translate("DepthTest", "Manual Distance"))
        self.r_sensor.setText(_translate("DepthTest", "Sensor Distance"))
        self.l_sensor.setText(_translate("DepthTest", "-"))
        self.l_plane_fit_mse.setText(_translate("DepthTest", "-"))
        self.l_gt_plane_mse.setText(_translate("DepthTest", "-"))
        self.l_gt_plane_mse_2.setText(_translate("DepthTest", "-"))
        self.board_group.setTitle(_translate("DepthTest", "board_side"))
        self.r_left.setText(_translate("DepthTest", "Left"))
        self.r_right.setText(_translate("DepthTest", "Right"))
        self.r_center.setText(_translate("DepthTest", "Center"))
        self.options_group.setTitle(_translate("DepthTest", "options"))
        self.c_lrcheck.setText(_translate("DepthTest", "lrcheck"))
        self.c_extended.setText(_translate("DepthTest", "extended"))
        self.c_subpixel.setText(_translate("DepthTest", "subpixel"))


class Camera:
    def __init__(self, lrcheck, subpixel, extended):
        # get mono resolution
        cam_res = {
            'OV7251': dai.MonoCameraProperties.SensorResolution.THE_480_P,
            'OV9*82': dai.MonoCameraProperties.SensorResolution.THE_800_P,
            'OV9282': dai.MonoCameraProperties.SensorResolution.THE_800_P
        }
        self.device = dai.Device()
        print(self.device.getDeviceInfo().getXLinkDeviceDesc())
        sensors = self.device.getCameraSensorNames()
        mono_resolution = cam_res[sensors[dai.CameraBoardSocket.LEFT]]
        if mono_resolution is dai.MonoCameraProperties.SensorResolution.THE_400_P:
            self.resolution = (640, 400)
        elif mono_resolution is dai.MonoCameraProperties.SensorResolution.THE_480_P:
            self.resolution = (640, 480)
        elif mono_resolution is dai.MonoCameraProperties.SensorResolution.THE_800_P:
            self.resolution = (1280, 800)
        elif mono_resolution is dai.MonoCameraProperties.SensorResolution.THE_720_P:
            self.resolution = (1280, 720)
        else:
            self.resolution = None
        # Create pipeline
        pipeline = dai.Pipeline()
        mono_left = pipeline.create(dai.node.MonoCamera)
        mono_right = pipeline.create(dai.node.MonoCamera)
        stereo = pipeline.create(dai.node.StereoDepth)

        xout_depth = pipeline.create(dai.node.XLinkOut)
        xin_spatial_calc_config = pipeline.create(dai.node.XLinkIn)

        xout_depth.setStreamName("depth")
        xin_spatial_calc_config.setStreamName("spatialCalcConfig")

        mono_left.setResolution(mono_resolution)
        mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        mono_right.setResolution(mono_resolution)
        mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

        stereo.initialConfig.setConfidenceThreshold(200)
        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        stereo.setRectifyEdgeFillColor(0)  # black, to better see the cutout
        stereo.initialConfig.setMedianFilter(dai.StereoDepthProperties.MedianFilter.MEDIAN_OFF)
        stereo.setLeftRightCheck(lrcheck)
        stereo.setSubpixel(subpixel)
        stereo.setExtendedDisparity(extended)

        # Linking
        mono_left.out.link(stereo.left)
        mono_right.out.link(stereo.right)

        stereo.depth.link(xout_depth.input)

        # self.device = dai.Device(pipeline)
        self.device.startPipeline(pipeline)
        global mx_id, product
        mx_id = self.device.getDeviceInfo().getMxId()
        calib_obj = self.device.readCalibration()
        try:
            product = calib_obj.eepromToJson()['productMame']
        except KeyError:
            product = calib_obj.eepromToJson()['boardName']
        M_right = np.array(calib_obj.getCameraIntrinsics(calib_obj.getStereoRightCameraId(), self.resolution[0], self.resolution[1]))
        R2 = np.array(calib_obj.getStereoRightRectificationRotation())
        H_right_inv = np.linalg.inv(np.matmul(np.matmul(M_right, R2), np.linalg.inv(M_right)))
        global inter_conv
        inter_conv = np.matmul(np.linalg.inv(M_right), H_right_inv)
        self.spatialCalcConfigInQueue = self.device.getInputQueue("spatialCalcConfig")
        self.depthQueue = self.device.getOutputQueue(name="depth", maxSize=4, blocking=False)
        # self.spatialCalcQueue = self.device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)

    def get_frame(self):
        in_depth = self.depthQueue.tryGet()
        if in_depth is None:
            return
        depth_frame = in_depth.getFrame()
        depth_frame_color = cv2.normalize(depth_frame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
        depth_frame_color = cv2.equalizeHist(depth_frame_color)
        depth_frame_color = cv2.applyColorMap(depth_frame_color, cv2.COLORMAP_HOT)

        if colorMode == QtGui.QImage.Format_RGB888:
            depth_frame_color = cv2.cvtColor(depth_frame_color, cv2.COLOR_BGR2RGB)
            return depth_frame_color, depth_frame

    def get_resolution(self):
        return self.resolution


class ROI:
    def __init__(self, white_rect, black_rect):
        self.whiteRect = white_rect
        self.whiteRect.setRect(0, 0, 100, 100)
        self.whiteRect.setPen(QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 255), 5))
        self.whiteRect.setBrush(QtGui.QBrush())

        self.blackRect = black_rect
        self.blackRect.setRect(0, 0, 100, 100)
        self.blackRect.setPen(QtGui.QPen(QtGui.QColor.fromRgb(0, 0, 0), 4))
        self.blackRect.setBrush(QtGui.QBrush())

    def update(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        if x1 < x2:
            x = x1
        else:
            x = x2
        if y1 < y2:
            y = y1
        else:
            y = y2
        w = abs(x1 - x2)
        h = abs(y1 - y2)
        self.whiteRect.setRect(x, y, w, h)
        self.blackRect.setRect(x, y, w, h)


def clamp(n, smallest, largest):
    return int(max(smallest, min(n, largest)))


class Frame(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, roi):
        super().__init__()
        self.pixmap = None
        self.camera = None
        self.p1 = None
        self.p2 = None
        self.acceptHoverEvents()
        self.roi = roi
        self.cameraEnabled = False
        self.width = 0
        self.height = 0
        self.depth_roi = None
        self.depth_frame = None

    def get_depth_frame(self):
        return self.depth_frame

    def get_roi(self):
        if self.p1 is None and self.p2 is None:
            return None, None
        resolution = self.camera.get_resolution()
        sbox = [int(self.p1[0]*resolution[0]/self.width), int(self.p1[1]*resolution[1]/self.height)]
        ebox = [int(self.p2[0]*resolution[0]/self.width), int(self.p2[1]*resolution[1]/self.height)]
        if sbox[0] > ebox[0]:
            sbox[0], ebox[0] = ebox[0], sbox[0]
        if sbox[1] > ebox[1]:
            sbox[1], ebox[1] = ebox[1], sbox[1]
        return sbox, ebox

    def update_frame(self):
        if not self.cameraEnabled:
            return
        frames = self.camera.get_frame()
        if frames is None:
            return
        cv_frame, self.depth_frame = frames
        if cv_frame is None:
            return
        q_image = QtGui.QImage(cv_frame.data, cv_frame.shape[1], cv_frame.shape[0], colorMode)
        pixmap = QtGui.QPixmap.fromImage(q_image)
        self.pixmap = pixmap.scaled(630, 480, QtCore.Qt.KeepAspectRatio)
        if self.width == 0 or self.height == 0:
            self.width = self.pixmap.width()
            self.height = self.pixmap.height()
            self.p1 = [int(self.width * 0.4), int(self.height * 0.4)]
            self.p2 = [int(self.width * 0.6), int(self.height * 0.6)]
            self.roi.update(self.p1, self.p2)
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.p1 = [event.pos().x(), event.pos().y()]
        self.p1[0] = clamp(self.p1[0], 0, self.width)
        self.p1[1] = clamp(self.p1[1], 0, self.height)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.p2 = [int(event.pos().x()), int(event.pos().y())]
        self.p2[0] = clamp(self.p2[0], 0, self.width)
        self.p2[1] = clamp(self.p2[1], 0, self.height)
        self.roi.update(self.p1, self.p2)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.p2 = [int(event.pos().x()), int(event.pos().y())]
        self.p2[0] = clamp(self.p2[0], 0, self.width)
        self.p2[1] = clamp(self.p2[1], 0, self.height)
        self.roi.update(self.p1, self.p2)

    def enable_camera(self, lrcheck, subpixel, extended):
        self.camera = Camera(lrcheck, subpixel, extended)
        self.cameraEnabled = True

    def disable_camera(self):
        self.camera.device.close()
        self.cameraEnabled = False
        if self.pixmap is not None:
            self.pixmap.fill()
        self.setPixmap(self.pixmap)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, dialog):
        super().__init__(dialog)
        self.whiteRect = QtWidgets.QGraphicsRectItem()
        self.blackRect = QtWidgets.QGraphicsRectItem()
        self.roi = ROI(self.whiteRect, self.blackRect)
        self.frame = Frame(self.roi)
        self.addItem(self.frame)
        self.addItem(self.whiteRect)
        self.addItem(self.blackRect)

    def get_frame(self):
        return self.frame

def pixel_coord_np(startX, startY, endX, endY):
    """
    Pixel in homogenous coordinate
    Returns:
        Pixel coordinate:       [3, width * height]
    """
    # print(startX, startY, endX, endY)
    x = np.linspace(startX, endX - 1, endX - startX).astype(np.int32)
    y = np.linspace(startY, endY - 1, endY - startY).astype(np.int32)

    [x, y] = np.meshgrid(x, y)
    return np.vstack((x.flatten(), y.flatten(), np.ones_like(x.flatten())))


def search_depth_pos(x, y, depth):
    def_x = x
    def_y = y
    while depth[y, x] == 0:
        if depth[y + 1, x] != 0:
            y += 1
        elif depth[y, x + 1] != 0:
            x += 1
        else:
            y += 1
            x += 1
        if abs(def_x - x) > 10 or abs(def_y - y) > 10:
            return x, y, False
    return x, y, True


def search_depth_neg(x, y, depth):
    def_x = x
    def_y = y
    while depth[y, x] == 0:
        if depth[y - 1, x] != 0:
            y -= 1
        elif depth[y, x - 1] != 0:
            x -= 1
        else:
            y -= 1
            x -= 1
        if abs(def_x - x) > 10 or abs(def_y - y) > 10:
            return x, y, False
    return x, y, True


def search_depth(x, y, depth):
    up_x, up_y, status = search_depth_pos(x, y, depth)
    if not status:
        up_x, up_y, status = search_depth_neg(x, y, depth)
    return up_x, up_y


def fit_plane_LTSQ(XYZ):
    (rows, cols) = XYZ.shape
    G = np.ones((rows, 3))
    G[:, 0] = XYZ[:, 0]  #X
    G[:, 1] = XYZ[:, 1]  #Y
    Z = XYZ[:, 2]
    (a, b, c), resid, rank, s = np.linalg.lstsq(G, Z, rcond=None)
    normal = (a, b, -1)
    nn = np.linalg.norm(normal)
    normal = normal / nn
    return c, normal


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # DepthTest = QtWidgets.QMainWindow()
        self.fill_rate = None
        self.gt_plane_rmse = None
        self.plane_fit_rmse = None
        self.gt_plane_mse = None
        self.plane_fit_mse = None
        self.error = None
        self.true_distance = 0
        self.ui = Ui_DepthTest()
        self.ui.setupUi(self)
        self.scene = Scene(self)
        self.ui.preview_video.setScene(self.scene)
        # self.ui.preview_video.onm
        self.ui.b_start.clicked.connect(self.button_event)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000 // 30)
        try: #TODO Find a way to scan for USB ports
            self.serial_reader = serial.Serial("/dev/ttyUSB0", 115200)
        except:
            self.serial_reader = None
        self.ui.r_sensor.setChecked(True)
        self.count = 0
        self.pass_count = 0
        self.fail_count = 0
        self.max_error = 0
        self.min_plane_error = 100
        self.average_error = None
        self.set_result('')
        self.z_distance = 0

    def set_result(self, result):
        self.ui.l_result.setText(result)
        self.ui.l_result.adjustSize()
        if result == "PASS": self.ui.l_result.setStyleSheet("color: green")
        if result == "FAIL": self.ui.l_result.setStyleSheet("color: red")

    def button_event(self):
        if self.ui.b_start.text() == "Save":
            self.scene.get_frame().disable_camera()
            self.ui.b_start.setText("Start")
            self.ui.l_test.setText('Depth Test')
            if self.pass_count < 10 and self.fail_count < 10:
                self.average_error = self.error
            self.average_error = round(self.average_error, 2)
            self.save_csv()
            self.set_result('')
            self.ui.options_group.setDisabled(False)
        else:
            self.scene.get_frame().enable_camera(self.ui.c_lrcheck.isChecked(), self.ui.c_subpixel.isChecked(), self.ui.c_extended.isChecked())

            # print(f'{self.ui.c_lrcheck.isChecked()}, {self.ui.c_subpixel.isChecked()}, {self.ui.c_extended.isChecked()}')
            self.error = 0
            self.average_error = 0
            self.count = 0
            self.pass_count = 0
            self.fail_count = 0
            self.sum = 0
            self.ui.l_gt_plane_rmse.setText('None')
            self.ui.l_fill_rate.setText('')
            self.ui.l_lidar.setText('')
            self.ui.b_start.setText("Save")
            self.ui.l_test.setText(str(product))
            self.ui.options_group.setDisabled(True)

    def save_csv(self):
        path = os.path.realpath(__file__).rsplit('/', 1)[0] + '/depth_result/' + str(product) + '.csv'
        print(path)
        if os.path.exists(path):
            file = open(path, 'a')
        else:
            file = open(path, 'w')
            file.write(CSV_HEADER + '\n')
        if self.ui.l_result.text() != 'PASS' and self.ui.l_result.text() != 'FAIL':
            self.ui.l_result.setText('NOT TESTED')
        side = ''
        if self.ui.r_left.isChecked():
            side = 'left'
        elif self.ui.r_right.isChecked():
            side = 'right'
        elif self.ui.r_center.isChecked():
            side = 'center'
        file.write(f'   {int(time.time())},{mx_id},{self.true_distance},{self.z_distance},{self.plane_fit_mse},\
                        {self.gt_plane_mse},{self.plane_fit_rmse},{self.gt_plane_rmse},{self.fill_rate},\
                        {self.ui.l_result.text()},{side}\n')
        file.close()

    def calculate_errors(self):
        depth_frame = self.scene.get_frame().get_depth_frame()
        sbox, ebox = self.scene.get_frame().get_roi()
        if sbox is None or ebox is None:
            return False
        depth_roi = depth_frame[sbox[1]:ebox[1], sbox[0]:ebox[0]]
        coord = pixel_coord_np(*sbox, *ebox)
        # Removing Zeros from coordinates
        cam_coords = np.dot(inter_conv, coord) * depth_roi.flatten() / 1000.0
        # Removing outliers from Z coordinates. top and bottoom 0.5 percentile of valid depth
        try:
            valid_cam_coords = np.delete(cam_coords, np.where(cam_coords[2, :] == 0.0), axis=1)
            valid_cam_coords = np.delete(valid_cam_coords, np.where(valid_cam_coords[2, :] <= np.percentile(valid_cam_coords[2, :], 0.5)), axis=1)
            valid_cam_coords = np.delete(valid_cam_coords, np.where(valid_cam_coords[2, :] >= np.percentile(valid_cam_coords[2, :], 99.5)), axis=1)
        except IndexError:
            return

        # Subsampling 4x4 grid points in the selected ROI
        subsampled_pixels = []
        subsampled_pixels_depth = []
        x_diff = ebox[0] - sbox[0]
        y_diff = ebox[1] - sbox[1]
        for i in range(4):
            x_loc = sbox[0] + int(x_diff * (i / 3))
            for j in range(4):
                y_loc = sbox[1] + int(y_diff * (j / 3))
                subsampled_pixels.append([x_loc, y_loc, 1])
                if depth_frame[y_loc, x_loc] == 0:
                    x_loc, y_loc = search_depth(x_loc, y_loc, depth_frame)
                subsampled_pixels_depth.append(depth_frame[y_loc, x_loc])
                # print("Coordinate at {}, {} is {} & {} with depth of {}".format(i, j, x_loc, y_loc, depth_img[y_loc, x_loc]))
        subsampled_pixels_depth = np.array(subsampled_pixels_depth)
        subsampled_pixels = np.array(subsampled_pixels).transpose()
        sub_points3D = np.dot(inter_conv, subsampled_pixels) * subsampled_pixels_depth.flatten() / 1000.0  # [x, y, z]
        sub_points3D = sub_points3D.transpose()
        # sc._offsets3d = (sub_points3D[:, 0], sub_points3D[:, 1], sub_points3D[:, 2]) #3D Plot
        c, normal = fit_plane_LTSQ(sub_points3D)
        # maxx = np.max(sub_points3D[:, 0])
        # maxy = np.max(sub_points3D[:, 1])
        # minx = np.min(sub_points3D[:, 0])
        # miny = np.min(sub_points3D[:, 1])
        #
        d = -np.array([0.0, 0.0, c]).dot(normal)
        # # fitPlane = (normal, d)
        # xx, yy = np.meshgrid([minx, maxx], [miny, maxy])
        # self.z_distance = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
        # print("Distance of subpixel from plane")
        # print(sub_points3D[0].dot(normal) + d)
        plane_offset_error = 0
        gt_offset_error = 0
        planeR_ms_offset_rror = 0
        gtR_ms_offset_error = 0
        for roi_point in valid_cam_coords.transpose():
            fitPlaneDist = roi_point.dot(normal) + d
            gt_normal = np.array([0, 0, 1], dtype=np.float32)
            gt_plane = (gt_normal, -self.true_distance)
            gt_plane_dist = roi_point.dot(gt_plane[0]) + gt_plane[1]
            plane_offset_error += fitPlaneDist
            gt_offset_error += gt_plane_dist
            planeR_ms_offset_rror += fitPlaneDist ** 2
            gtR_ms_offset_error += gt_plane_dist ** 2
            
        self.plane_fit_mse = plane_offset_error / valid_cam_coords.shape[1]
        self.gt_plane_mse = gt_offset_error / valid_cam_coords.shape[1]
        self.plane_fit_rmse = np.sqrt(planeR_ms_offset_rror / valid_cam_coords.shape[1])
        self.gt_plane_rmse = round(np.sqrt(gtR_ms_offset_error / valid_cam_coords.shape[1]), 3)

        totalPixels = (ebox[0] - sbox[0]) * (ebox[1] - sbox[1])
        flatRoi = depth_roi.flatten()
        sampledPixels = np.delete(flatRoi, np.where(flatRoi == 0))
        self.fill_rate = 100 * sampledPixels.shape[0] / totalPixels
        return True

    def timer_event(self):
        self.scene.get_frame().update_frame()
        if not self.calculate_errors():
            return

        if self.ui.r_manual.isChecked():
            self.true_distance = self.ui.spin_manual.value()
        else:
            if self.serial_reader is not None:
                try:
                    result = ""
                    while True:
                        c = self.serial_reader.read().decode()
                        if c == '\n':
                            break
                        result += c
                    try:
                        self.true_distance = float(result[-7:-3])
                    except ValueError:
                        pass
                except serial.serialutil.PortNotOpenError:
                    pass
            else:
                try:
                    self.serial_reader = serial.Serial("/dev/ttyUSB0", 115200)
                except:
                    self.serial_reader = None
                self.true_distance = 0
        self.ui.l_lidar.setText(f'{self.true_distance}')

        # if self.true_distance > 0 and self.z_distance > 0:
        if self.count < 30:
            if self.max_error < self.gt_plane_rmse:
                self.max_error = self.gt_plane_rmse
            if self.min_plane_error > self.fill_rate:
                self.min_plane_error = self.fill_rate
            self.count += 1
        else:
            # self.error = round(self.sum / 30, 2)
            self.ui.l_fill_rate.setText(f'{self.fill_rate}')
            self.ui.l_gt_plane_rmse.setText(f'{self.max_error}')
            self.ui.l_plane_fit_mse.setText(f'{self.plane_fit_mse}')
            self.ui.l_gt_plane_mse.setText(f'{self.gt_plane_mse}')
            self.ui.l_plane_fit_mse.setText(f'{self.plane_fit_mse}')

            if self.true_distance <= 1:
                error_threshold = 0.03
            elif self.true_distance >= 2:
                error_threshold = 0.06
            else:
                error_threshold = self.true_distance*0.03
            if self.max_error < error_threshold and self.min_plane_error > 0.98:
                self.set_result('PASS')
            else:
                self.set_result('FAIL')
            self.count = 0
            self.max_error = 0
            self.min_plane_error = 100


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    class_instance = Application()
    class_instance.show()
    sys.exit(app.exec_())