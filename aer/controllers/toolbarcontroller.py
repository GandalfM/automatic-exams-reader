from PyQt5.QtWidgets import QInputDialog, QLineEdit

class ToolbarController:

    EXAMS_INDEX = 0
    TEMPLATES_INDEX = 1

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        # counter to differentiate field name
        self.counter = 0

        self.ui.actionZoomIn.triggered.connect(self.on_zoom_in_triggered)
        self.ui.actionZoomOut.triggered.connect(self.on_zoom_out_triggered)
        self.ui.actionAddField.triggered.connect(self.on_add_field_triggered)

    def on_zoom_in_triggered(self):
        if self.ui.mainTabs.currentIndex() == ToolbarController.EXAMS_INDEX:
            self.on_zoom_in(self.mainwindow.examcontroller.selected_exam, self.mainwindow.examcontroller)
        elif self.ui.mainTabs.currentIndex() == ToolbarController.TEMPLATES_INDEX:
            self.on_zoom_in(self.mainwindow.template_view_controller.default_exam, self.mainwindow.template_view_controller)

    def on_zoom_out_triggered(self):
        if self.ui.mainTabs.currentIndex() == ToolbarController.EXAMS_INDEX:
            self.on_zoom_out(self.mainwindow.examcontroller.selected_exam, self.mainwindow.examcontroller)
        elif self.ui.mainTabs.currentIndex() == ToolbarController.TEMPLATES_INDEX:
            self.on_zoom_out(self.mainwindow.template_view_controller.default_exam, self.mainwindow.template_view_controller)

    def on_zoom_out(self, image, controller):
        if image is not None:
            scale = controller.scale
            if scale >= 0.2:
                controller.scale -= 0.1

    def on_zoom_in(self, image, controller):
        if image is not None:
            scale = controller.scale
            if scale <= 2.0:
                controller.scale += 0.1

    def on_add_field_triggered(self):
        rect = self.mainwindow.template_view_controller.tmp_rect
        if rect is not None:
            template = self.mainwindow.template_view_controller.selected_template.template
            while template.field_exists("default" + str(self.counter)):
                self.counter += 1
            default = "default{}".format(self.counter)
            text, ok = QInputDialog.getText(self.mainwindow, 'Field name', 'Enter field name:',  QLineEdit.Normal, default)

            if ok:
                self.counter += 1
                template = self.mainwindow.template_view_controller.selected_template.template
                self.mainwindow.template_view_controller.tmp_rect = None

                template.add_field(text, rect)
