#!/usr/bin/env python
#! coding: utf-8
#! python3
# ~= Inept's Video Awesome Madness =~
# Dirty as hay, learn python with this file at your own risks.
# TheDarkTiger 2023
#
# Takes a video, and decompose it to sequences of images.
# Or take a sequence of images, and reconstruct the video.

import os
import json

def create_dir_if_nonexistant( folderPath ):
	if not os.path.exists( folderPath ) :
		os.mkdir( folderPath )
	

class project:
	
	projectPath = None
	pathOfSourceVideo = None
	ffmpegGeneralOptions = "-hide_banner -loglevel error"
	
	# init the project
	def __init__( self, projectPath=None ):
		if projectPath == None :
			print( "[Err ] No path for project" )
		else:
			self.projectPath = projectPath
			create_dir_if_nonexistant( self.projectPath )
			create_dir_if_nonexistant( self.projectPath+"\\frames" )
	
	
	# Return the string of this project
	def __str__( self ):
		stringToReturn = "Unknown state"
		
		if self.projectPath == None :
			stringToReturn = "No path set"
		else :
			stringToReturn = f"Project folder: {self.projectPath}"
		
		if self.pathOfSourceVideo == None :
			stringToReturn += "\nNo video set"
		else :
			stringToReturn += f"\nSource video path:{self.pathOfSourceVideo}"
		
		return stringToReturn
	
	# Set source video
	def set_source_video_path( self, pathOfSourceVideo=None ):
		self.pathOfSourceVideo = pathOfSourceVideo
	
	# Extract frames from video
	def extract_frames_from_video( self ):
		print( f"{self.projectPath} : Vid 2 Images" )
		ressourcesOk = True
		
		if self.pathOfSourceVideo == None :
			print( "[Err ] No video source set" )
			ressourcesOk = False
		
		if os.path.exists( f"{self.projectPath}\\frames\\frame0001.png" ):
			print( "[Err ] Frame(s) already exists. Please delete yourself first." )
			ressourcesOk = False
		
		if ressourcesOk:
			input = self.pathOfSourceVideo
			
			output = f"{self.projectPath}\\config.json"
			commandLine = f'ffprobe {self.ffmpegGeneralOptions} -v quiet -print_format json -show_format -show_streams "{input}">"{output}"'
			os.system( commandLine )
			
			output = f"{self.projectPath}\\frames\\frame%04d.png"
			commandLine = f'ffmpeg -i "{input}" -r 30 -f image2 -vf "scale=-2:120" "{output}"'
			commandLine = f'ffmpeg {self.ffmpegGeneralOptions} -i "{input}" -f image2 -vf "scale=160:120:force_original_aspect_ratio=decrease,pad=160:120:-1:-1:color=black" "{output}"'
			os.system( commandLine )
			
			output = f"{self.projectPath}\\audio.ogg"
			commandLine = f'ffmpeg -y {self.ffmpegGeneralOptions} -i "{input}" -vn -c:a libopus "{output}"'
			os.system( commandLine )
			
	
	
	def generate_video_from_frames( self, pathOfSourceVideo=None ):
		print( f"{self.projectPath} : Images 2 Vid" )
		ressourcesOk = True
		
		images = f"{self.projectPath}\\frames\\frame%04d.png"
		if not os.path.exists( f"{self.projectPath}\\frames\\frame0001.png" ):
			print( f"[Err ] No frame found! How can I make a video?" )
			ressourcesOk = False
		
		audio = f"{self.projectPath}\\audio.ogg"
		if not os.path.exists( audio ):
			print( f"[Err ] Audio file '{audio}' not found. Please give one." )
			ressourcesOk = False
		
		framerate = 24
		data = None
		jsonFilePath = f"{self.projectPath}\\config.json"
		if not os.path.exists( jsonFilePath ) :
			print( f"[Err ] '{jsonFilePath}' file not found. Make a project first!" )
			ressourcesOk = False
		
		
		if ressourcesOk :
			with open( jsonFilePath, "r" ) as readFile :
				data = json.load(readFile)
			
			
			framerate = data["streams"][0]["r_frame_rate"]
			
			videoOptions = '-vf "scale=-2:480" -sws_flags neighbor'
			
			# Codec selection
			codec = "webm"
			encoding = "fast"
			
			if codec == "webm" :
				output = f"{self.projectPath}\\generated.webm"
				if encoding == "fast" :
					print( "[info] codec VP8" )
					videoCodec = '-c:v libvpx'
				else:
					print( "[info] codec VP9" )
					videoCodec = '-c:v libvpx-vp9'
				audioCodec = '-c:a libopus'
			elif codec == "mp4":
				output = f"{self.projectPath}\\generated.mp4"
				if encoding == "fast" :
					print( "[info] codec x264" )
					videoCodec = '-c:v libx264'
				else:
					print( "[info] codec x265" )
					videoCodec = '-c:v libx265'
				audioCodec = '-c:a aac'
			else :
				print( "[Err ] codec unknown" )
				codec = None
			
			# Video encoding
			if codec != None :
				if os.path.exists( output ) :
					print( f"[Err ] '{output}' file already exists. Please delete yourself." )
				else :
					commandLine = f'ffmpeg {self.ffmpegGeneralOptions} -framerate {framerate} -i "{images}" -i "{audio}" {videoCodec} {videoOptions} {audioCodec} "{output}"'
					os.system( commandLine )
			
		
	

# Lib test
if __name__ == "__main__" :
	
	p2 = project( "tmptptpmmtp" )
	p2.set_source_video_path( "aCAT47.webm" )
	print( p2 )
	# p2.extract_frames_from_video()
	# p2.generate_video_from_frames()

