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

def error( string="!?" ):
	print( f"[ERR!] {string}" )

def warning( string="!?" ):
	print( f"[Warn ] {string}" )

def info( string="!?" ):
	print( f"[info] {string}" )


def create_dir_if_nonexistant( folderPath ):
	if not os.path.exists( folderPath ) :
		os.mkdir( folderPath )
	

class project:
	
	project = {"name":"uninitialized"}
	projectPath = None
	pathOfSourceVideo = None
	
	# init the project
	def __init__( self, projectPath=None ):
		if projectPath == None :
			error( "No path for project" )
		else:
			if os.path.exists( projectPath ):
				info( "loading project..." )
				self.load( projectPath )
			else:
				# Initialize a new project
				info( "creating new project..." )
				self.projectPath = projectPath
				create_dir_if_nonexistant( self.projectPath )
				create_dir_if_nonexistant( self.projectPath+"\\frames" )
				create_dir_if_nonexistant( self.projectPath+"\\pages" )
				
				self.project = {"name":"", "exportFrames":True, "exportPages":False, "pathOfSourceVideo":""}
				self.project["frame"] = {"width":160, "height":120, "stretch":False}
				self.project["page"] = {"frameNumber":24, "framesPerLines":6}
				self.project["video"] = {"width":640, "height":480, "fps":24, "codec":{"final":"VP9", "draft":"VP8"}}
				self.project["ffmpeg"] = {"generalOptions":"-hide_banner -loglevel error"}
				
				with open( self.projectPath+"\\project.json", "w" ) as writeFile :
					json.dump( self.project, writeFile, indent=2, separators=(",", ": ") )
	
	
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
		
		stringToReturn += str( self.project )
		
		return stringToReturn
	
	# Load a project
	def load( self, projectPath=None ):
		if os.path.exists( projectPath ):
			self.projectPath = projectPath
			
			with open( f"{projectPath}\\project.json", "r" ) as readFile :
				data = json.load(readFile)
			
			smells = 0
			if "name" not in data : smells+=2
			if "frame" not in data : smells+=1
			if "page" not in data : smells+=1
			if "video" not in data : smells+=2
			if "ffmpeg" not in data : smells+=1
			
			info( f"{smells} smells while opening the project" )
			if smells > 3 :
				error( "Too many smells while trying to load the project, please, check the files" )
			else:
				info( "Ok, loading" )
				self.project = data.copy()
			
	
	# Save project
	def save( self ):
		with open( self.projectPath+"\\project.json", "w" ) as writeFile :
			json.dump( self.project, writeFile, indent=2, separators=(",", ": ") )
	
	# Set source video
	def set_source_video_path( self, pathOfSourceVideo=None ):
		if not os.path.exists( pathOfSourceVideo ):
			error( f"Video not found '{pathOfSourceVideo}'" )
		else:
			self.project["pathOfSourceVideo"] = pathOfSourceVideo
			
			input = self.project["pathOfSourceVideo"]
			output = f"{self.projectPath}\\config.json"
			options = self.project["ffmpeg"]["generalOptions"]
			commandLine = f'ffprobe {options} -v quiet -print_format json -show_format -show_streams "{input}">"{output}"'
			os.system( commandLine )
			
			with open( output, "r" ) as readFile :
				data = json.load(readFile)
			
			self.project["video"]["fps"] = data["streams"][0]["r_frame_rate"]
			
	
	# Set the fps for extraction/reconstruction
	def set_fps( self, fps=None ):
		if fps == None :
			error( "No fps given" )
		else:
			self.project["video"]["fps"] = fps
	
	# Extract frames from video
	def extract_frames_from_video( self ):
		print( f"{self.projectPath} : Vid 2 Images" )
		ressourcesOk = True
		input = self.project["pathOfSourceVideo"]
		
		
		if input == None :
			error( "No video source set" )
			ressourcesOk = False
		
		if os.path.exists( f"{self.projectPath}\\frames\\frame0001.png" ):
			error( "Frame(s) already exists. Please delete yourself first." )
			ressourcesOk = False
		
		if ressourcesOk:
			ffmpegGeneralOptions = self.project["ffmpeg"]["generalOptions"]
			fps = self.project["video"]["fps"]
			
			w = self.project["frame"]["width"]
			h = self.project["frame"]["height"]
			if self.project["frame"]["stretch"] :
				videoFilter = f"scale={w}:{h}"
			else:
				videoFilter = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:-1:-1:color=black"
			
			output = f"{self.projectPath}\\frames\\frame%04d.png"
			commandLine = f'ffmpeg {ffmpegGeneralOptions} -i "{input}" -r {fps} -f image2 -vf "{videoFilter}" "{output}"'
			os.system( commandLine )
			
			output = f"{self.projectPath}\\audio.ogg"
			commandLine = f'ffmpeg -y {ffmpegGeneralOptions} -i "{input}" -vn -c:a libopus "{output}"'
			os.system( commandLine )
			
	
	
	def generate_video_from_frames( self, pathOfSourceVideo=None ):
		info( f"{self.projectPath} : Images 2 Vid" )
		ressourcesOk = True
		
		images = f"{self.projectPath}\\frames\\frame%04d.png"
		if not os.path.exists( f"{self.projectPath}\\frames\\frame0001.png" ):
			error( f"No frame found! How can I make a video?" )
			ressourcesOk = False
		
		audio = f"{self.projectPath}\\audio.ogg"
		if not os.path.exists( audio ):
			error( f"Audio file '{audio}' not found. Please give one." )
			ressourcesOk = False
		
		data = None
		jsonFilePath = f"{self.projectPath}\\config.json"
		if not os.path.exists( jsonFilePath ) :
			error( f"'{jsonFilePath}' file not found. Make a project first!" )
			ressourcesOk = False
		
		
		if ressourcesOk :
			with open( jsonFilePath, "r" ) as readFile :
				data = json.load(readFile)
			
			# Codec selection
			codec = "webm"
			encoding = "fast"
			
			if codec == "webm" :
				output = f"{self.projectPath}\\generated.webm"
				if encoding == "fast" :
					info( "codec VP8" )
					videoCodec = '-c:v libvpx'
				else:
					info( "codec VP9" )
					videoCodec = '-c:v libvpx-vp9'
				audioCodec = '-c:a libopus'
			elif codec == "mp4":
				output = f"{self.projectPath}\\generated.mp4"
				if encoding == "fast" :
					info( "codec x264" )
					videoCodec = '-c:v libx264'
				else:
					info( "codec x265" )
					videoCodec = '-c:v libx265'
				audioCodec = '-c:a aac'
			else :
				error( "codec unknown" )
				codec = None
			
			# Video encoding
			if codec != None :
				if os.path.exists( output ) :
					error( f"'{output}' file already exists. Please delete yourself." )
				else :
					ffmpegGeneralOptions = self.project["ffmpeg"]["generalOptions"]
					fps = self.project["video"]["fps"]
					
					w = self.project["video"]["width"]
					h = self.project["video"]["height"]
					videoOptions = f'-vf "scale={w}:{h},setsar=1:1" -sws_flags neighbor'
					
					commandLine = f'ffmpeg {ffmpegGeneralOptions} -framerate {fps} -i "{images}" -i "{audio}" {videoCodec} {videoOptions} {audioCodec} "{output}"'
					os.system( commandLine )
			
		
	

# Lib test
if __name__ == "__main__" :
	
	p = project( "tmptptpmmtp" )
	print( p )
	p.set_source_video_path( "aCAT47.webm" )
	print( p )
	p.set_fps( 6 )
	print( p )
	p.save()
	print( p )
	p.extract_frames_from_video()
	p.generate_video_from_frames()

