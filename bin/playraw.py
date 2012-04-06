#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main:
	
	def __init__(self, directoryname="/tmp"):
		self.dir = directoryname
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Video-Player")
		window.set_default_size(500, 400)
#		window.fullscreen()
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		window.show_all()
		
		self.player = gst.element_factory_make("playbin2", "player")

		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

		self.player.set_property("uri", "file:///tmp/anim-1.mov")
		self.player.set_state(gst.STATE_PLAYING)
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			filepath = self.entry.get_text()
			if os.path.isfile(filepath):
				self.button.set_label("Stop")
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
						
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.player.set_property("uri", "file://" + self.get_next_file())
			self.player.set_state(gst.STATE_PLAYING)
			#self.player.set_state(gst.STATE_NULL)
			#self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.button.set_label("Start")

	def get_next_file(self):
		return "/tmp/homer.avi"


	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", False)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			gtk.gdk.threads_leave()
			
if len (sys.argv) != 2:
  sys.exit (1)
GTK_Main(sys.argv[1])
gtk.gdk.threads_init()
gtk.main()

