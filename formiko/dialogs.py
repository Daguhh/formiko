# -*- coding: utf-8 -*-
from gi.repository import Gtk

from formiko import __version__, __author__, __copyright__, __comment__


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, transient_for):
        super(AboutDialog, self).__init__(transient_for=transient_for,
                                          modal=False)
        self.set_program_name("Formiko")
        self.set_version(__version__)
        self.set_copyright(__copyright__ + ' ' + __author__)
        self.set_comments(__comment__)
        self.set_website("https://github.com/ondratu/formiko")
        # self.set_website("https://formiko.zeropage.cz")
        # self.set_logo("formiko.svg")


class QuitDialogWithoutSave(Gtk.MessageDialog):
    def __init__(self, parent, file_name):
        super(QuitDialogWithoutSave, self).__init__(
            parent,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL,
            "File %s not saved.\n"
            "Are you sure to quite without save ?" % file_name)


class FileChooserDialog(Gtk.FileChooserDialog):
    def __init__(self, title, parent, action):
        if action == Gtk.FileChooserAction.SAVE:
            label = Gtk.STOCK_SAVE
        else:
            label = Gtk.STOCK_OPEN
        super(FileChooserDialog, self).__init__(
            title,
            parent,
            action,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             label, Gtk.ResponseType.ACCEPT))

    def add_filter_rst(self):
        filter_rst = Gtk.FileFilter()
        filter_rst.set_name("reSructuredText")
        filter_rst.add_pattern("*.rst")
        filter_rst.add_pattern("*.RST")
        self.add_filter(filter_rst)

    def add_filter_plain(self):
        filter_txt = Gtk.FileFilter()
        filter_txt.set_name("plain text")
        filter_txt.add_mime_type("plain/text")
        self.add_filter(filter_txt)

    def add_filter_all(self):
        filter_all = Gtk.FileFilter()
        filter_all.set_name("all files")
        filter_all.add_pattern("*")
        self.add_filter(filter_all)


class FileOpenDialog(FileChooserDialog):
    def __init__(self, parent):
        super(FileOpenDialog, self).__init__(
            "Open file", parent, Gtk.FileChooserAction.OPEN
        )


class FileSaveDialog(FileChooserDialog):
    def __init__(self, parent):
        super(FileSaveDialog, self).__init__(
            "Save as file", parent, Gtk.FileChooserAction.SAVE
        )