#!/usr/bin/env python
#! coding: utf-8
#! python3
# ~= Inept's Video Awesome Madness =~
# Dirty as hay, learn python with this file at your own risks.
# TheDarkTiger 2023
#
# Takes a video, and decompose it to sequences of images.
# Or take a sequence of images, and reconstruct the video.

import IVAM


print( "Hi Nepter!" )

# To convert from video to images
mode = "vid2img"

# To convert from images to video
# mode = "img2vid"


# Set the project folder here
project = IVAM.project( "WIP" )

# Set the source video here
project.set_source_video_path( "video.webm" )

# Force the fps to 12
# will affect frame generation and thus video generation
project.set_fps( 12 )

# Summary
print( project )

#Call to the scripts
if mode == "vid2img" :
	project.extract_frames_from_video()
	
elif mode == "img2vid" :
	project.generate_video_from_frames()
	
else :
	print( "Mode unknown" )

