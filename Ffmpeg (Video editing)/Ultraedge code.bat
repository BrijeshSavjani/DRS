@echo off
::formatting
title DRS Backend
prompt DRS$G


::ChangeDir
cd B:\Desktop\T1
B:
cls


::front_camera
ffmpeg -i front.mp4 -filter:v "setpts =2*PTS" -an front_out.mp4


::Ultraedge_Sound
ffmpeg -i side_input.mp4 -filter:a "atempo=0.5,volume=2" output.mp3
ffmpeg -i output.mp3 -filter_complex "[0:a] showwaves=s=112*208:mode=line:colors=#FFFF00,format=yuv420p[v]" -map "[v]" -map 0:a ywaves.mp4
ffmpeg -i ywaves.mp4 -filter:v "negate" bwave.mp4
ffmpeg -loop 1 -i Ultraedge.png -i bwave.mp4 -filter_complex "overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p" -c:a copy Ultraedge.avi



::side_camera
ffmpeg -i side_input.mp4 -filter:v "setpts = 2*PTS" -an side_temp_out.mp4
ffmpeg -i side_temp_out.mp4 -i output.mp3 -c:v copy -c:a aac side_out.mp4

del side_temp_out.mp4
del ywaves.mp4
del bwave.mp4
del output.mp3
cls
ffplay Ultraedge.avi
cls
pause
cls
ffplay front_out.mp4
cls
pause
ffplay side_out.mp4