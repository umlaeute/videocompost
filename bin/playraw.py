#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
from Compost import Compost

WIDTH=320
HEIGHT=240
FRAMERATE="(fraction)25/1"

class GTK_Main:
	
	def __init__(self, directoryname="/tmp"):
		self.blocksize = WIDTH * HEIGHT * 4

		self.dir = directoryname
		self.compost_init()
		## liste mit verfuegbaren chunks
		# self.compost._chunkss
		self.chunkindex=0
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("Video-Player")
		window.set_default_size(500, 400)
		window.fullscreen()
		window.connect("destroy", gtk.main_quit, "WM destroy")
		vbox = gtk.VBox()
		window.add(vbox)
		self.movie_window = gtk.DrawingArea()
		vbox.add(self.movie_window)
		window.show_all()

		self.pipeline = gst.Pipeline()

		# open a file		
		self.fileplayer = gst.element_factory_make("filesrc")
		self.pipeline.add(self.fileplayer)

		self.fileplayer.set_property("blocksize", self.blocksize)

		# force caps
		self.capsstring = "video/x-raw-rgb, bpp=(int)32, endianness=(int)4321, depth=(int)32, red_mask=(int)16711680, green_mask=(int)65280, blue_mask=(int)255, alpha_mask=(int)-16777216, width=(int)%d, height=(int)%d, framerate=%s, pixel-aspect-ratio=(fraction)1/1" % (WIDTH, HEIGHT, FRAMERATE)
		caps = gst.Caps(self.capsstring)
		self.capsfilter = gst.element_factory_make("capsfilter")
		self.pipeline.add(self.capsfilter)
		self.capsfilter.set_property("caps", caps)

		# colorspace converter
		self.colorspace = gst.element_factory_make("ffmpegcolorspace")
		self.pipeline.add(self.colorspace)

		# videorate converter
		self.videorate = gst.element_factory_make("videorate")
		self.pipeline.add(self.videorate)
		
		# output window
		self.sink = gst.element_factory_make("xvimagesink")
		self.pipeline.add(self.sink)

		self.sink.set_xwindow_id(self.movie_window.window.xid)

		gst.element_link_many(self.fileplayer, self.capsfilter, self.colorspace, self.videorate, self.sink)
		
		# bus magic
		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

		self.fileplayer.set_property("location", self.get_next_file())
		self.pipeline.set_state(gst.STATE_PLAYING)
		
# 	def start_stop(self, w):
# 		if self.button.get_label() == "Start":
# 			filepath = self.entry.get_text()
# 			if os.path.isfile(filepath):
# 				self.button.set_label("Stop")
# 				self.fileplayer.set_property("location", filepath)
# 				self.pipeline.set_state(gst.STATE_PLAYING)
# 		else:
# 			self.pipeline.set_state(gst.STATE_NULL)
# 			self.button.set_label("Start")
						
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.pipeline.set_state(gst.STATE_NULL)
			self.fileplayer.set_property("location", self.get_next_file())
			self.pipeline.set_state(gst.STATE_PLAYING)
			#self.pipeline.set_state(gst.STATE_NULL)
			#self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			self.pipeline.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
#			self.button.set_label("Start")

	def get_next_file(self):
		chunk = self.get_next_chunk()
		if chunk != None:
			return chunk._filename
		return None

	def get_next_chunk(self):
		if self.chunkindex < len(self.compost._chunks):
			i=self.chunkindex
			self.chunkindex+=1
			return self.compost._chunks[i]
		return self.compost_init()


	def compost_init(self):
		self.compost = Compost()
		self.compost.load()
		self.chunkindex=1
		return self.compost._chunks[0]
		



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
			
GTK_Main()
gtk.gdk.threads_init()
gtk.main()

