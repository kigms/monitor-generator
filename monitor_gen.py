import maya.cmds as cmds

import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance


def get_maya_main_win():
    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class MonitorGeneratorWin(QtWidgets.QDialog):
    """Monitor Generator Window class"""
    def __init__(self):
        super(MonitorGeneratorWin, self).__init__(parent=get_maya_main_win())
        self.setWindowTitle("Monitor generator")
        self.monitor_gen = Monitor()
        self._create_ui()

    def _create_ui(self):
        self.main_lay = QtWidgets.QVBoxLayout()
        self._add_params_form()
        self._add_btns()
        self.setLayout(self.main_lay)

    def _add_params_form(self):
        self.form_lay = QtWidgets.QFormLayout()
        self._add_monitor_type_params()
        self._add_dimensions_params()
        self._add_panel_ratio_params()
        self._add_panel_front_params()
        self._add_panel_back_params()
        self._add_neck_ratio_params()
        self._add_base_ratio_params()
        self.main_lay.addLayout(self.form_lay)

    def _add_monitor_type_params(self):
        self.monitor_type_lay = QtWidgets.QHBoxLayout()

        self.fpd_radio_btn = QtWidgets.QRadioButton("Flat-Panel Display")
        self.fpd_radio_btn.setChecked(True)
        self.fpd_radio_btn.setIcon(QtGui.QIcon(""))  # add icon
        self.fpd_radio_btn.setSizePolicy(
                                        QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.Preferred)

        self.crt_radio_btn = QtWidgets.QRadioButton("Cathode-Ray Tube")
        self.crt_radio_btn.setIcon(QtGui.QIcon(""))  # add icon
        self.crt_radio_btn.setSizePolicy(
                                        QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.Preferred)

        self.monitor_type_lay.addWidget(self.fpd_radio_btn)
        self.monitor_type_lay.addWidget(self.crt_radio_btn)

        self.form_lay.addRow(self.tr("Choose monitor type |"),
                             self.monitor_type_lay)

        self.fpd_radio_btn.toggled.connect(
                                          self._adjust_values_for_monitor_type)
        self.crt_radio_btn.toggled.connect(
                                          self._adjust_values_for_monitor_type)

    def _add_dimensions_params(self):
        self.dimensions_lay = QtWidgets.QHBoxLayout()

        self.width_lbl = QtWidgets.QLabel("Width:")

        self.width_dspnbx = QtWidgets.QDoubleSpinBox(value=90)
        self.width_dspnbx.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.Preferred)
        self.width_dspnbx.setRange(0.0, 9999.99)
        self.width_dspnbx.setMinimumWidth(50)
        self.width_dspnbx.setSingleStep(1.0)

        self.height_lbl = QtWidgets.QLabel("Height:")

        self.height_dspnbx = QtWidgets.QDoubleSpinBox(value=60)
        self.height_dspnbx.setSizePolicy(
                                        QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.Preferred)

        self.height_dspnbx.setRange(0.0, 9999.99)
        self.height_dspnbx.setMinimumWidth(50)
        self.height_dspnbx.setSingleStep(1.0)

        self.depth_lbl = QtWidgets.QLabel("Depth:")

        self.depth_dspnbx = QtWidgets.QDoubleSpinBox(value=15)
        self.depth_dspnbx.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                        QtWidgets.QSizePolicy.Preferred)
        self.depth_dspnbx.setRange(0.0, 9999)
        self.depth_dspnbx.setMinimumWidth(50)
        self.depth_dspnbx.setSingleStep(1.0)

        self.dimensions_lay.addWidget(self.width_lbl)
        self.dimensions_lay.addWidget(self.width_dspnbx)
        self.dimensions_lay.addWidget(self.height_lbl)
        self.dimensions_lay.addWidget(self.height_dspnbx)
        self.dimensions_lay.addWidget(self.depth_lbl)
        self.dimensions_lay.addWidget(self.depth_dspnbx)

        self.form_lay.addRow(self.tr("General |"), self.dimensions_lay)

    def _add_panel_ratio_params(self):
        self.panel_ratio_lay = QtWidgets.QHBoxLayout()

        self.panel_height_ratio_lbl = QtWidgets.QLabel("Relative height:")

        self.panel_height_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.8)
        self.panel_height_ratio_dspnbx.setMinimumWidth(50)
        self.panel_height_ratio_dspnbx.setRange(0.05, 1.00)
        self.panel_height_ratio_dspnbx.setSingleStep(0.05)
        self.panel_height_ratio_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.panel_height_ratio_slider.setRange(5, 100)

        self.panel_depth_ratio_lbl = QtWidgets.QLabel("Relative depth:")

        self.panel_depth_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.15)
        self.panel_depth_ratio_dspnbx.setMinimumWidth(50)
        self.panel_depth_ratio_dspnbx.setRange(0.05, 1.00)
        self.panel_depth_ratio_dspnbx.setSingleStep(0.05)
        self.panel_depth_ratio_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.panel_depth_ratio_slider.setRange(5, 100)

        self.panel_ratio_lay.addWidget(self.panel_depth_ratio_lbl)
        self.panel_ratio_lay.addWidget(self.panel_depth_ratio_dspnbx)
        self.panel_ratio_lay.addWidget(self.panel_depth_ratio_slider)

        self.panel_ratio_lay.addWidget(self.panel_height_ratio_lbl)
        self.panel_ratio_lay.addWidget(self.panel_height_ratio_dspnbx)
        self.panel_ratio_lay.addWidget(self.panel_height_ratio_slider)

        self.form_lay.addRow(self.tr("Panel (front) |"),
                             self.panel_ratio_lay)

        self.panel_height_ratio_slider.valueChanged.connect(
                                        self._update_panel_height_ratio_dspnbx)
        self.panel_height_ratio_dspnbx.textChanged.connect(
                                        self._update_panel_height_ratio_slider)

        self.panel_depth_ratio_slider.valueChanged.connect(
                                         self._update_panel_depth_ratio_dspnbx)
        self.panel_depth_ratio_dspnbx.textChanged.connect(
                                         self._update_panel_depth_ratio_slider)

    def _add_panel_front_params(self):
        self.panel_front_lay = QtWidgets.QHBoxLayout()

        self.screen_offset_amount_lbl = QtWidgets.QLabel("Offset:")

        self.scrn_offset_dspnbx = QtWidgets.QDoubleSpinBox(value=2)
        self.scrn_offset_dspnbx.setMinimumWidth(50)
        self.scrn_offset_dspnbx.setRange(0.05, 5.00)
        self.scrn_offset_dspnbx.setSingleStep(0.05)

        self.screen_offset_amount_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.screen_offset_amount_slider.setRange(5, 500)

        self.extrusion_offset_amount_lbl = QtWidgets.QLabel(
                                                           "Extrusion offset:")

        self.scrn_extrsn_offset_dspnbx = QtWidgets.QDoubleSpinBox(
                                                                     value=0.4)
        self.scrn_extrsn_offset_dspnbx.setMinimumWidth(50)
        self.scrn_extrsn_offset_dspnbx.setRange(0.05, 5.00)
        self.scrn_extrsn_offset_dspnbx.setSingleStep(0.05)

        self.extrusion_offset_amount_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.extrusion_offset_amount_slider.setRange(5, 500)

        self.extrusion_amount_lbl = QtWidgets.QLabel("Extrusion amount:")

        self.extrusion_amount_dspnbx = QtWidgets.QDoubleSpinBox(value=0.4)
        self.extrusion_amount_dspnbx.setMinimumWidth(50)
        self.extrusion_amount_dspnbx.setRange(0.05, 5.00)
        self.extrusion_amount_dspnbx.setSingleStep(0.05)

        self.extrusion_amount_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.extrusion_amount_slider.setRange(5, 500)

        self.panel_front_lay.addWidget(self.screen_offset_amount_lbl)
        self.panel_front_lay.addWidget(self.scrn_offset_dspnbx)
        self.panel_front_lay.addWidget(self.screen_offset_amount_slider)

        self.panel_front_lay.addWidget(self.extrusion_offset_amount_lbl)
        self.panel_front_lay.addWidget(self.scrn_extrsn_offset_dspnbx)
        self.panel_front_lay.addWidget(self.extrusion_offset_amount_slider)

        self.panel_front_lay.addWidget(self.extrusion_amount_lbl)
        self.panel_front_lay.addWidget(self.extrusion_amount_dspnbx)
        self.panel_front_lay.addWidget(self.extrusion_amount_slider)

        self.form_lay.addRow(self.tr("Screen |"), self.panel_front_lay)

        self.screen_offset_amount_slider.valueChanged.connect(
                                      self._update_screen_offset_amount_dspnbx)
        self.scrn_offset_dspnbx.textChanged.connect(
                                      self._update_screen_offset_amount_slider)

        self.extrusion_offset_amount_slider.valueChanged.connect(
                                          self._update_extrusion_offset_dspnbx)
        self.scrn_extrsn_offset_dspnbx.textChanged.connect(
                                          self._update_extrusion_offset_slider)

        self.extrusion_amount_slider.valueChanged.connect(
                                          self._update_extrusion_amount_dspnbx)
        self.extrusion_amount_dspnbx.textChanged.connect(
                                          self._update_extrusion_amount_slider)

    def _add_panel_back_params(self):
        self.panel_back_lay = QtWidgets.QHBoxLayout()

        self.back_panel_offset_lbl = QtWidgets.QLabel("Offset:")

        self.b_panel_offset_dspnbx = QtWidgets.QDoubleSpinBox(value=0.01)
        self.b_panel_offset_dspnbx.setMinimumWidth(50)
        self.b_panel_offset_dspnbx.setRange(0.05, 5.00)
        self.b_panel_offset_dspnbx.setSingleStep(0.05)

        self.back_panel_offset_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.back_panel_offset_slider.setRange(5, 500)

        self.back_panel_extrusion_offset_lbl = QtWidgets.QLabel(
                                                           "Extrusion offset:")

        self.b_panel_extrsn_offset_dspnbx = QtWidgets.QDoubleSpinBox(
                                                                       value=1)
        self.b_panel_extrsn_offset_dspnbx.setMinimumWidth(50)
        self.b_panel_extrsn_offset_dspnbx.setRange(0.05, 5.00)
        self.b_panel_extrsn_offset_dspnbx.setSingleStep(0.05)

        self.back_panel_extrusion_offset_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.back_panel_extrusion_offset_slider.setRange(5, 500)

        self.back_panel_extrusion_lbl = QtWidgets.QLabel("Extrusion amount:")

        self.b_panel_extrsn_dspnbx = QtWidgets.QDoubleSpinBox(value=3)
        self.b_panel_extrsn_dspnbx.setMinimumWidth(50)
        self.b_panel_extrsn_dspnbx.setRange(0.05, 20.00)
        self.b_panel_extrsn_dspnbx.setSingleStep(0.05)

        self.back_panel_extrusion_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.back_panel_extrusion_slider.setRange(5, 2000)

        self.panel_back_lay.addWidget(self.back_panel_offset_lbl)
        self.panel_back_lay.addWidget(self.b_panel_offset_dspnbx)
        self.panel_back_lay.addWidget(self.back_panel_offset_slider)

        self.panel_back_lay.addWidget(self.back_panel_extrusion_offset_lbl)
        self.panel_back_lay.addWidget(self.b_panel_extrsn_offset_dspnbx)
        self.panel_back_lay.addWidget(self.back_panel_extrusion_offset_slider)

        self.panel_back_lay.addWidget(self.back_panel_extrusion_lbl)
        self.panel_back_lay.addWidget(self.b_panel_extrsn_dspnbx)
        self.panel_back_lay.addWidget(self.back_panel_extrusion_slider)

        self.form_lay.addRow(self.tr("Panel (back) |"), self.panel_back_lay)

        self.back_panel_offset_slider.valueChanged.connect(
                                         self._update_back_panel_offset_dspnbx)
        self.b_panel_offset_dspnbx.textChanged.connect(
                                         self._update_back_panel_offset_slider)

        self.back_panel_extrusion_offset_slider.valueChanged.connect(
                               self._update_back_panel_extrusion_offset_dspnbx)
        self.b_panel_extrsn_offset_dspnbx.textChanged.connect(
                               self._update_back_panel_extrusion_offset_slider)

        self.back_panel_extrusion_slider.valueChanged.connect(
                                      self._update_back_panel_extrusion_dspnbx)
        self.b_panel_extrsn_dspnbx.textChanged.connect(
                                      self._update_back_panel_extrusion_slider)

    def _add_neck_ratio_params(self):
        self.neck_ratio_lay = QtWidgets.QHBoxLayout()

        self.neck_width_ratio_lbl = QtWidgets.QLabel("Relative width:")

        self.neck_width_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.15)
        self.neck_width_ratio_dspnbx.setMinimumWidth(50)
        self.neck_width_ratio_dspnbx.setRange(0.05, 1.00)
        self.neck_width_ratio_dspnbx.setSingleStep(0.05)
        self.neck_width_ratio_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.neck_width_ratio_slider.setRange(5, 100)

        self.neck_height_ratio_lbl = QtWidgets.QLabel("Relative height:")

        self.neck_height_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.2)
        self.neck_height_ratio_dspnbx.setMinimumWidth(50)
        self.neck_height_ratio_dspnbx.setRange(0.00, 1.00)
        self.neck_height_ratio_dspnbx.setSingleStep(0.01)
        self.neck_height_ratio_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.neck_height_ratio_slider.setRange(0, 100)

        self.neck_depth_ratio_lbl = QtWidgets.QLabel("Relative depth:")

        self.neck_depth_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.1)
        self.neck_depth_ratio_dspnbx.setMinimumWidth(50)
        self.neck_depth_ratio_dspnbx.setRange(0.05, 1.00)
        self.neck_depth_ratio_dspnbx.setSingleStep(0.05)
        self.neck_depth_ratio_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.neck_depth_ratio_slider.setRange(4, 100)

        self.neck_ratio_lay.addWidget(self.neck_width_ratio_lbl)
        self.neck_ratio_lay.addWidget(self.neck_width_ratio_dspnbx)
        self.neck_ratio_lay.addWidget(self.neck_width_ratio_slider)

        self.neck_ratio_lay.addWidget(self.neck_height_ratio_lbl)
        self.neck_ratio_lay.addWidget(self.neck_height_ratio_dspnbx)
        self.neck_ratio_lay.addWidget(self.neck_height_ratio_slider)

        self.neck_ratio_lay.addWidget(self.neck_depth_ratio_lbl)
        self.neck_ratio_lay.addWidget(self.neck_depth_ratio_dspnbx)
        self.neck_ratio_lay.addWidget(self.neck_depth_ratio_slider)

        self.form_lay.addRow(self.tr("Neck |"),
                             self.neck_ratio_lay)

        self.neck_width_ratio_slider.valueChanged.connect(
                                          self._update_neck_width_ratio_dspnbx)
        self.neck_width_ratio_dspnbx.textChanged.connect(
                                          self._update_neck_width_ratio_slider)

        self.neck_height_ratio_slider.valueChanged.connect(
                                         self._update_neck_height_ratio_dspnbx)
        self.neck_height_ratio_dspnbx.textChanged.connect(
                                         self._update_neck_height_ratio_slider)

        self.neck_depth_ratio_slider.valueChanged.connect(
                                          self._update_neck_depth_ratio_dspnbx)
        self.neck_depth_ratio_dspnbx.textChanged.connect(
                                          self._update_neck_depth_ratio_slider)

    def _add_base_ratio_params(self):
        self.base_ratio_lay = QtWidgets.QHBoxLayout()

        self.base_width_ratio_lbl = QtWidgets.QLabel("Relative width:")

        self.base_width_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.25)
        self.base_width_ratio_dspnbx.setMinimumWidth(50)
        self.base_width_ratio_dspnbx.setRange(0.05, 1.00)
        self.base_width_ratio_dspnbx.setSingleStep(0.05)
        self.base_width_ratio_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.base_width_ratio_slider.setRange(5, 100)

        self.base_height_ratio_lbl = QtWidgets.QLabel("Relative height:")

        self.base_height_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=0.05)
        self.base_height_ratio_dspnbx.setMinimumWidth(50)
        self.base_height_ratio_dspnbx.setRange(0.05, 1.00)
        self.base_height_ratio_dspnbx.setSingleStep(0.05)
        self.base_height_ratio_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.base_height_ratio_slider.setRange(5, 100)

        self.base_depth_ratio_lbl = QtWidgets.QLabel("Relative depth:")

        self.base_depth_ratio_dspnbx = QtWidgets.QDoubleSpinBox(value=1)
        self.base_depth_ratio_dspnbx.setMinimumWidth(50)
        self.base_depth_ratio_dspnbx.setRange(0.05, 1.00)
        self.base_depth_ratio_dspnbx.setSingleStep(0.05)
        self.base_depth_ratio_slider = QtWidgets.QSlider(
                                                          QtCore.Qt.Horizontal)
        self.base_depth_ratio_slider.setRange(5, 100)

        self.base_ratio_lay.addWidget(self.base_width_ratio_lbl)
        self.base_ratio_lay.addWidget(self.base_width_ratio_dspnbx)
        self.base_ratio_lay.addWidget(self.base_width_ratio_slider)

        self.base_ratio_lay.addWidget(self.base_height_ratio_lbl)
        self.base_ratio_lay.addWidget(self.base_height_ratio_dspnbx)
        self.base_ratio_lay.addWidget(self.base_height_ratio_slider)

        self.base_ratio_lay.addWidget(self.base_depth_ratio_lbl)
        self.base_ratio_lay.addWidget(self.base_depth_ratio_dspnbx)
        self.base_ratio_lay.addWidget(self.base_depth_ratio_slider)

        self.form_lay.addRow(self.tr("Base |"),
                             self.base_ratio_lay)

        self.base_width_ratio_slider.valueChanged.connect(
                                          self._update_base_width_ratio_dspnbx)
        self.base_width_ratio_dspnbx.textChanged.connect(
                                          self._update_base_width_ratio_slider)

        self.base_height_ratio_slider.valueChanged.connect(
                                         self._update_base_height_ratio_dspnbx)
        self.base_height_ratio_dspnbx.textChanged.connect(
                                         self._update_base_height_ratio_slider)

        self.base_depth_ratio_slider.valueChanged.connect(
                                          self._update_base_depth_ratio_dspnbx)
        self.base_depth_ratio_dspnbx.textChanged.connect(
                                          self._update_base_depth_ratio_slider)

    def _add_btns(self):
        self.buttons_lay = QtWidgets.QHBoxLayout()
        self.generate_btn = QtWidgets.QPushButton("Generate")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.generate_btn.clicked.connect(self.generate)
        self.cancel_btn.clicked.connect(self.cancel)
        self.buttons_lay.addWidget(self.generate_btn)
        self.buttons_lay.addWidget(self.cancel_btn)
        self.main_lay.addLayout(self.buttons_lay)

    @QtCore.Slot()
    def _adjust_values_for_monitor_type(self):
        radio_btn_selected = self.sender()
        if radio_btn_selected.isChecked() and radio_btn_selected.text() == "Cathode-Ray Tube":
            print("CRT")
            self.width_dspnbx.setValue(60)
            self.height_dspnbx.setValue(60)
            self.depth_dspnbx.setValue(25)

            self.panel_height_ratio_dspnbx.setValue(.8)
            self.panel_depth_ratio_dspnbx.setValue(.6)

            self.scrn_offset_dspnbx.setValue(3.0)
            self.scrn_extrsn_offset_dspnbx.setValue(1.5)
            self.extrusion_amount_dspnbx.setValue(2)

            self.b_panel_offset_dspnbx.setValue(5)
            self.b_panel_extrsn_offset_dspnbx.setValue(5)
            self.b_panel_extrsn_dspnbx.setValue(15)

            self.neck_width_ratio_dspnbx.setValue(.2)
            self.neck_depth_ratio_dspnbx.setValue(.5)
            self.neck_height_ratio_dspnbx.setValue(.02)

            self.base_width_ratio_dspnbx.setValue(.3)
            self.base_depth_ratio_dspnbx.setValue(.6)
            self.base_height_ratio_dspnbx.setValue(.05)

        elif radio_btn_selected.isChecked():
            print("FPD")
            self.width_dspnbx.setValue(90)
            self.height_dspnbx.setValue(60)
            self.depth_dspnbx.setValue(15)

            self.panel_height_ratio_dspnbx.setValue(.8)
            self.panel_depth_ratio_dspnbx.setValue(.15)

            self.scrn_offset_dspnbx.setValue(2)
            self.scrn_extrsn_offset_dspnbx.setValue(.4)
            self.extrusion_amount_dspnbx.setValue(.4)

            self.b_panel_offset_dspnbx.setValue(0.01)
            self.b_panel_extrsn_offset_dspnbx.setValue(1)
            self.b_panel_extrsn_dspnbx.setValue(3)

            self.neck_width_ratio_dspnbx.setValue(.15)
            self.neck_depth_ratio_dspnbx.setValue(.1)
            self.neck_height_ratio_dspnbx.setValue(.2)

            self.base_width_ratio_dspnbx.setValue(.25)
            self.base_depth_ratio_dspnbx.setValue(1)
            self.base_height_ratio_dspnbx.setValue(.05)

    @QtCore.Slot()
    def _update_panel_height_ratio_slider(self):
        slider_update = int(self.panel_height_ratio_dspnbx.value()*100)
        self.panel_height_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_panel_height_ratio_dspnbx(self):
        dspnbx_update = self.panel_height_ratio_slider.value()/100
        self.panel_height_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_panel_depth_ratio_slider(self):
        slider_update = int(self.panel_depth_ratio_dspnbx.value()*100)
        self.panel_depth_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_panel_depth_ratio_dspnbx(self):
        dspnbx_update = self.panel_depth_ratio_slider.value()/100
        self.panel_depth_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_screen_offset_amount_slider(self):
        slider_update = int(self.scrn_offset_dspnbx.value()*100)
        self.screen_offset_amount_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_screen_offset_amount_dspnbx(self):
        dspnbx_update = self.screen_offset_amount_slider.value()/100
        self.scrn_offset_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_extrusion_offset_slider(self):
        slider_update = int(self.scrn_extrsn_offset_dspnbx.value()*100)
        self.extrusion_offset_amount_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_extrusion_offset_dspnbx(self):
        dspnbx_update = self.extrusion_offset_amount_slider.value()/100
        self.scrn_extrsn_offset_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_extrusion_amount_slider(self):
        slider_update = int(self.extrusion_amount_dspnbx.value()*100)
        self.extrusion_amount_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_extrusion_amount_dspnbx(self):
        dspnbx_update = self.extrusion_amount_slider.value()/100
        self.extrusion_amount_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_back_panel_offset_slider(self):
        slider_update = int(self.b_panel_offset_dspnbx.value()*100)
        self.back_panel_offset_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_back_panel_offset_dspnbx(self):
        dspnbx_update = self.back_panel_offset_slider.value()/100
        self.b_panel_offset_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_back_panel_extrusion_offset_slider(self):
        slider_update = int(
                    self.b_panel_extrsn_offset_dspnbx.value()*100)
        self.back_panel_extrusion_offset_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_back_panel_extrusion_offset_dspnbx(self):
        dspnbx_update = self.back_panel_extrusion_offset_slider.value()/100
        self.b_panel_extrsn_offset_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_back_panel_extrusion_slider(self):
        slider_update = int(self.b_panel_extrsn_dspnbx.value()*100)
        self.back_panel_extrusion_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_back_panel_extrusion_dspnbx(self):
        dspnbx_update = self.back_panel_extrusion_slider.value()/100
        self.b_panel_extrsn_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_neck_width_ratio_slider(self):
        slider_update = int(self.neck_width_ratio_dspnbx.value()*100)
        self.neck_width_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_neck_width_ratio_dspnbx(self):
        dspnbx_update = self.neck_width_ratio_slider.value()/100
        self.neck_width_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_neck_height_ratio_slider(self):
        slider_update = int(self.neck_height_ratio_dspnbx.value()*100)
        self.neck_height_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_neck_height_ratio_dspnbx(self):
        dspnbx_update = self.neck_height_ratio_slider.value()/100
        self.neck_height_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_neck_depth_ratio_slider(self):
        slider_update = int(self.neck_depth_ratio_dspnbx.value()*100)
        self.neck_depth_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_neck_depth_ratio_dspnbx(self):
        dspnbx_update = self.neck_depth_ratio_slider.value()/100
        self.neck_depth_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_base_width_ratio_slider(self):
        slider_update = int(self.base_width_ratio_dspnbx.value()*100)
        self.base_width_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_base_width_ratio_dspnbx(self):
        dspnbx_update = self.base_width_ratio_slider.value()/100
        self.base_width_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_base_height_ratio_slider(self):
        slider_update = int(self.base_height_ratio_dspnbx.value()*100)
        self.base_height_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_base_height_ratio_dspnbx(self):
        dspnbx_update = self.base_height_ratio_slider.value()/100
        self.base_height_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def _update_base_depth_ratio_slider(self):
        slider_update = int(self.base_depth_ratio_dspnbx.value()*100)
        self.base_depth_ratio_slider.setValue(slider_update)

    @QtCore.Slot()
    def _update_base_depth_ratio_dspnbx(self):
        dspnbx_update = self.base_depth_ratio_slider.value()/100
        self.base_depth_ratio_dspnbx.setValue(dspnbx_update)

    @QtCore.Slot()
    def generate(self):
        print("Generating table...")
        self.set_monitor_properties()
        self.monitor_gen.make_monitor()

    @QtCore.Slot()
    def cancel(self):
        print("Cancelling...")
        self.set_monitor_properties()
        self.close()

    def set_monitor_properties(self):
        self.monitor_gen.width = self.width_dspnbx.value()
        self.monitor_gen.height = self.height_dspnbx.value()
        self.monitor_gen.depth = self.depth_dspnbx.value()

        self.monitor_gen.panel_height_ratio = self.panel_height_ratio_dspnbx.value()
        self.monitor_gen.panel_depth_ratio = self.panel_depth_ratio_dspnbx.value()

        self.monitor_gen.screen_offset_amount = self.scrn_offset_dspnbx.value()
        self.monitor_gen.scrn_extrsn_offset_amount = self.scrn_extrsn_offset_dspnbx.value()
        self.monitor_gen.screen_extrusion = self.extrusion_amount_dspnbx.value()

        self.monitor_gen.b_panel_offset = self.b_panel_offset_dspnbx.value()
        self.monitor_gen.b_panel_extrsn_offset = self.b_panel_extrsn_offset_dspnbx.value()
        self.monitor_gen.b_panel_extrsn = self.b_panel_extrsn_dspnbx.value()

        self.monitor_gen.neck_width_ratio = self.neck_width_ratio_dspnbx.value()
        self.monitor_gen.neck_height_ratio = self.neck_height_ratio_dspnbx.value()
        self.monitor_gen.neck_depth_ratio = self.neck_depth_ratio_dspnbx.value()

        self.monitor_gen.base_width_ratio = self.base_width_ratio_dspnbx.value()
        self.monitor_gen.base_height_ratio = self.base_height_ratio_dspnbx.value()
        self.monitor_gen.base_depth_ratio = self.base_depth_ratio_dspnbx.value()


class Monitor(object):
    def __init__(self):
        self.panel = ''
        self.neck = ''
        self.base = ''

        self.width = 90.0
        self.height = 60.0
        self.depth = 15.0

        self.panel_height_ratio = 0.9
        self.panel_depth_ratio = 0.15

        self.screen_offset_amount = .5
        self.scrn_extrsn_offset_amount = .05
        self.screen_extrusion = .05

        self.b_panel_extrsn_offset = 1.0
        self.b_panel_offset = 5.0
        self.b_panel_extrsn = 0.0

        self.neck_width_ratio = 0.2
        self.neck_height_ratio = 0.1
        self.neck_depth_ratio = 0.1

        self.base_width_ratio = 0.3
        self.base_height_ratio = .05
        self.base_depth_ratio = .05

        self._reset()

    def _make_base(self):
        self.base_width = self.width * self.base_width_ratio
        self.base_depth = self.depth * self.base_depth_ratio

        base = cmds.polyCube(width=self.base_width, depth=self.base_depth,
                             height=self.height*self.base_height_ratio,
                             name="base")[0]
        self.base = base

        y_offset1 = self.height*self.base_height_ratio*.5
        cmds.xform(base, translation=[0, y_offset1, 0])

    def _make_neck(self):
        self.neck_width = self.width * self.neck_width_ratio
        self.neck_depth = self.depth * self.neck_depth_ratio

        neck = cmds.polyCube(width=self.neck_width, depth=self.neck_depth,
                             height=self.height*self.neck_height_ratio,
                             name="neck")[0]
        self.neck = neck

        y_offset2 = (
      self.height*self.neck_height_ratio)*.5+self.height*self.base_height_ratio
        cmds.xform(neck, translation=[0, y_offset2, 0])

    def _make_panel(self):
        self.panel_height = self.height * self.panel_height_ratio
        self.panel_depth = self.depth * self.panel_depth_ratio

        panel = cmds.polyCube(width=self.width, depth=self.panel_depth,
                              height=self.panel_height,
                              name="panel")[0]
        self.panel = panel

        cmds.select(f'{panel}.f[0]')
        cmds.polyExtrudeFacet(offset=self.screen_offset_amount)
        correct_direction = self.screen_extrusion*-1
        cmds.polyExtrudeFacet(localTranslateZ=correct_direction,
                              offset=self.scrn_extrsn_offset_amount)

        cmds.select(f'{panel}.f[2]')
        cmds.polyExtrudeFacet(offset=self.b_panel_offset)
        cmds.polyExtrudeFacet(localTranslateZ=self.b_panel_extrsn,
                              offset=self.b_panel_extrsn_offset)

        y_offset3 = self.panel_height*.5 + self.height*self.base_height_ratio + self.height*self.neck_height_ratio
        cmds.xform(panel, translation=[0, y_offset3, 0])

    def _grp_objects(self):
        stand = cmds.group([self.neck, self.base], name="stand")
        cmds.group([self.panel, stand], name="monitor")

    def _reset(self):
        self.base = ''
        self.neck = ''
        self.panel = ''
        self.master_grp_name = 'monitor_grp'

    def make_monitor(self):
        self._make_panel()
        self._make_neck()
        self._make_base()
        self._grp_objects()
