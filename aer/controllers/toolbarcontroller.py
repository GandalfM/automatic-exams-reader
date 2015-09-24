class ToolbarController:

    EXAMS_INDEX = 0
    TEMPLATES_INDEX = 1

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui

        self.ui.actionZoomIn.triggered.connect(self.on_zoom_in_triggered)
        self.ui.actionZoomOut.triggered.connect(self.on_zoom_out_triggered)

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
