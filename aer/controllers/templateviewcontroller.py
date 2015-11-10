from PyQt5 import QtGui

from aer.config.configconstants import TEMPLATE_IMAGE_ZOOM
from aer.domain.template import Template
from aer.domain.templatefile import TemplateFile
from aer.image.drawing import Drawing
from aer.utils.imageutil import pil2pixmap


class TemplateViewController:

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ui = mainwindow.ui
        self.config = mainwindow.config_manager

        self.ui.templateTextEdit.textChanged.connect(self.template_text_changed)
        self.ui.templateViewLabel.mousePressed.connect(self.on_mouse_press)
        self.ui.templateViewLabel.mouseReleased.connect(self.on_mouse_release)
        self.ui.templateViewLabel.mouseMove.connect(self.on_mouse_move)
        self.ui.templateViewLabel.wheelScrolled.connect(self.on_wheel_scroll)

        self.tmp_rect = None
        self._default_exam = None
        self._selected_template = None
        self._scale = self.config.get_property(TEMPLATE_IMAGE_ZOOM, 1.0)
        self.mouse_pressed = False

        self.drawing = Drawing(None, self._scale)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.config.set_property(TEMPLATE_IMAGE_ZOOM, self._scale)
        self.drawing = Drawing(self.default_exam, self._scale)
        self._draw_template()

    @property
    def selected_template(self):
        return self._selected_template

    @selected_template.setter
    def selected_template(self, filename):
        size = None
        if self._default_exam is not None:
            size = (self._default_exam.size[0], self._default_exam.size[1])
        self._selected_template = TemplateFile(filename, size)
        self._selected_template.statusChanged.connect(self._draw_template)
        self._selected_template.statusChanged.connect(self._change_title)
        self._selected_template.template.templateChanged.connect(self._draw_template)
        self._selected_template.template.templateChanged.connect(self._change_text)
        self._change_text()
        self._draw_template()

    @property
    def default_exam(self):
        return self._default_exam

    @default_exam.setter
    def default_exam(self, exam):
        self._default_exam = exam
        self.drawing = Drawing(exam, self.scale)
        self._draw_template()

    def _draw_template(self):
        if self._default_exam is not None:
            if self._selected_template is not None:
                image = self.drawing.draw_template(self._selected_template.template, self.tmp_rect)
            else:
                image = self.drawing.resize(self._default_exam, self._scale)
            self.ui.templateViewLabel.setPixmap(pil2pixmap(image))

    def _change_text(self):
        content = self._selected_template.template.to_json()
        self._selected_template.changed = True
        self.ui.templateTextEdit.setText(content)

    def _change_title(self):
        self.mainwindow.setWindowTitle(self.mainwindow.WINDOW_TITLE + " - " + self.selected_template.file.name if self.selected_template.file is not None else "")

    def template_text_changed(self):
        data = self.ui.templateTextEdit.toPlainText()
        try:
            if self.selected_template.template.to_json() != data:
                template = Template.from_json(data)
                self._selected_template.template = template
                self._selected_template.template.templateChanged.connect(self._draw_template)
                self._selected_template.template.templateChanged.connect(self._change_text)
            color = QtGui.QColor("white")
        except (ValueError, Exception):
            color = QtGui.QColor("#ff9999")
        palette = self.ui.templateTextEdit.palette()
        palette.setColor(QtGui.QPalette.Base, color)
        self.ui.templateTextEdit.setPalette(palette)

    def on_mouse_press(self, event):
        self.mouse_pressed = True
        if self._selected_template is not None:
            x = int(event.pos().x() / self._scale)
            y = int(event.pos().y() / self._scale)
            tmp_rect = self._selected_template.template.remove_field_at(x, y)
            if tmp_rect is None:
                self.tmp_rect = (x, y, 0, 0)
            else:
                self.tmp_rect = tmp_rect
            self._draw_template()

    def on_mouse_move(self, event):
        if self._selected_template is not None:
            if self.mouse_pressed and self.tmp_rect is not None:
                self._common_move(event.pos())
            pass

    def _common_move(self, pos):
        m_x, m_y = int(pos.x() / self._scale), int(pos.y() / self._scale)
        x, y, w, h = self.tmp_rect
        self.tmp_rect = (x, y, m_x - x, m_y - y)
        if self.tmp_rect[2] < 0:
            l = list(self.tmp_rect)
            l[2] = abs(l[2])
            l[0] -= l[2]
            self.tmp_rect = tuple(l)
        if self.tmp_rect[3] < 0:
            l = list(self.tmp_rect)
            l[3] = abs(l[3])
            l[1] -= l[3]
            self.tmp_rect = tuple(l)
        self._draw_template()

    def on_mouse_release(self, event):
        if self._selected_template is not None:
            x, y, w, h = self.tmp_rect
            if w == 0 and h == 0:
                self.tmp_rect = None
                self._draw_template()
            self.mouse_pressed = False

    def on_wheel_scroll(self, event):
        if self.default_exam is not None:
            delta = event.angleDelta().y()
            if delta > 0 and self.scale <= 2.0:
                self.scale += 0.1
            if delta < 0 and self.scale >= 0.2:
                self.scale -= 0.1
