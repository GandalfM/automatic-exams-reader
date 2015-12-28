from PyQt5.QtWidgets import QInputDialog, QLineEdit
from aer.domain.field import FieldType
from aer.controllers.templateviewcontroller import Mode
from aer.controllers.addfielddialog import AddFieldDialog

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
        self.ui.actionAddMark.triggered.connect(self.on_add_mark_triggered)
        self.ui.actionEditMode.toggled.connect(self.on_edit_mode_toggled)

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

    def on_edit_mode_toggled(self, active):
        if active:
            self.mainwindow.template_view_controller.tmp_rect = None
            self.mainwindow.template_view_controller.redraw()
            self.mainwindow.template_view_controller.mode = Mode.EDIT
        else:
            self.mainwindow.template_view_controller.commit_rect()
            self.mainwindow.template_view_controller.redraw()
            self.mainwindow.template_view_controller.mode = Mode.CREATE


    def on_add_field_triggered(self):
        self.on_add_rectangle()

    def on_add_mark_triggered(self):
        self.on_add_rectangle("mark")

    def on_add_rectangle(self, name=None):
        rect = self.mainwindow.template_view_controller.tmp_rect
        field_type = FieldType.HANDWRITTEN
        if rect is not None:
            if name is None:
                dialog = AddFieldDialog()
                dialog.show(name=self._default_name())

                if not dialog.ok:
                    return
                name = dialog.name
                field_type = dialog.field_type

            template = self.mainwindow.template_view_controller.selected_template.template
            self.mainwindow.template_view_controller.tmp_rect = None
            try:
                template.add_field(name, rect, field_type=field_type)
            except Exception as ex:
                self.mainwindow.template_view_controller.tmp_rect = rect
                self.ui.statusbar.showMessage(str(ex))

    def _default_name(self):
        template = self.mainwindow.template_view_controller.selected_template.template
        while template.field_exists("default {}".format(self.counter)):
            self.counter += 1
        return "default {}".format(self.counter)