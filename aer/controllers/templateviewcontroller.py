import time
from enum import Enum

from PyQt5 import QtCore
from PyQt5 import QtGui

from aer.config.configconstants import TEMPLATE_IMAGE_ZOOM
from aer.domain.template import Template
from aer.domain.templatefile import TemplateFile
from aer.image.drawing import Drawing
from aer.utils.imageutil import pil2pixmap


class Mode(Enum):
    CREATE = 1
    EDIT = 2
    MOVE = 3
    SCALE = 4


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
        self.ui.templateViewLabel.keyPressed.connect(self.on_key_press)

        self.mode = Mode.CREATE
        self.edit_mode = Mode.MOVE
        self.tmp_rect = None
        self._default_exam = None
        self._selected_template = None
        self._scale = self.config.get_property(TEMPLATE_IMAGE_ZOOM, 1.0)
        self.scale_rect_margin = 30

        self.mouse_pressed = False
        self.mouse_pressed_pos = None
        self.mouse_pos_rect_offset = None
        self.original_rect_pos = None
        self.draw_time = 0

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
                image = self.drawing.draw_template(
                    self._selected_template.template,
                    self.tmp_rect,
                    self.original_rect_pos)
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
        if self._selected_template is not None:
            x = int(event.pos().x() / self._scale)
            y = int(event.pos().y() / self._scale)
            self.mouse_pressed = True
            self.mouse_pressed_pos = (x, y)

            if self.mode == Mode.EDIT:
                clicked_field = self._selected_template.template.get_field_at(x, y)
                if clicked_field and self.tmp_rect is None:
                    clicked_rect_tuple = (clicked_field.name, clicked_field.rect)
                    self.tmp_rect = clicked_rect_tuple if clicked_rect_tuple is None else clicked_rect_tuple[1]
                    self.mouse_pos_rect_offset = (x - self.tmp_rect[0], y - self.tmp_rect[1])
                    self.original_rect_pos = (self.tmp_rect[0], self.tmp_rect[1])
                    if self.distance_to_scale(self.mouse_pressed_pos, self.tmp_rect):
                        self.edit_mode = Mode.SCALE
                    else:
                        self.edit_mode = Mode.MOVE
                elif self.tmp_rect is not None:
                    self.commit_rect()
                self._draw_template()
            else:
                self.tmp_rect = (x, y, 0, 0)
                self._draw_template()

    def distance_to_scale(self, point, rect):
        x, y, w, h = rect
        xp, yp = point
        dx = x + w - xp
        dy = y + h - yp
        return 0 < dx < self.scale_rect_margin and 0 < dy < self.scale_rect_margin

    def commit_rect(self):
        if self.tmp_rect is not None:
            x, y, _, __ = self.tmp_rect
            o_x, o_y = self.original_rect_pos
            field = self._selected_template.template.get_field_at(o_x + 1, o_y + 1)
            if self.edit_mode == Mode.MOVE and self.original_rect_pos != (x, y):
                self._selected_template.template.move_field_to(field.name, self.tmp_rect[0], self.tmp_rect[1])
            else:
                self._selected_template.template.scale_field(field.name, self.tmp_rect[2], self.tmp_rect[3])
            self.original_rect_pos = None
            self.tmp_rect = None

    def on_mouse_move(self, event):
        if self._selected_template is not None:
            if self.mouse_pressed and self.tmp_rect is not None:
                if self.mode == Mode.CREATE:
                    self._common_move(event.pos())
                elif self.edit_mode == Mode.MOVE:
                    self._move_rect(event.pos())
                else:
                    self._common_move(event.pos())

                if time.time() - self.draw_time > 0.01:
                    self._draw_template()
                    self.draw_time = time.time()

    def _move_rect(self, pos):
        m_x, m_y = int(pos.x() / self._scale), int(pos.y() / self._scale)
        x, y, w, h = self.tmp_rect
        new_x = self.original_rect_pos[0] + m_x - self.mouse_pressed_pos[0]
        new_y = self.original_rect_pos[1] + m_y - self.mouse_pressed_pos[1]
        self.tmp_rect = (new_x, new_y, w, h)

    def _common_move(self, pos):
        m_x, m_y = int(pos.x() / self._scale), int(pos.y() / self._scale)
        x, y, w, h = self.tmp_rect
        self.tmp_rect = (x, y, m_x - x, m_y - y)

    def redraw(self):
        self._draw_template()

    def on_mouse_release(self, event):
        self.mouse_pressed = False
        if self._selected_template is not None and self.mode == Mode.CREATE:
            x, y, w, h = self.tmp_rect
            if w == 0 and h == 0:
                self.tmp_rect = None
                self._draw_template()

    def on_wheel_scroll(self, event):
        if self.default_exam is not None:
            delta = event.angleDelta().y()
            if delta > 0 and self.scale <= 2.0:
                self.scale += 0.1
            if delta < 0 and self.scale >= 0.2:
                self.scale -= 0.1

    def on_key_press(self, event):
        if event.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            if self.mode == Mode.EDIT and self.tmp_rect:
                self.tmp_rect = self._selected_template.template.remove_field_at(self.tmp_rect[0] + 1,
                                                                                 self.tmp_rect[1] + 1)
                self.tmp_rect = None
        if event.key() == QtCore.Qt.Key_E:
            self.change_mode(True)
        if event.key() == QtCore.Qt.Key_C:
            self.change_mode(False)
            self.original_rect_pos = None
            self.tmp_rect = None
        self._draw_template()

    def change_mode(self, edit):
        if edit:
            self.mode = Mode.EDIT
            self.tmp_rect = None
            self._draw_template()
            self.ui.actionEditMode.setChecked(True)
        else:
            self.mode = Mode.CREATE
            self.commit_rect()
            self._draw_template()
            self.ui.actionEditMode.setChecked(False)
