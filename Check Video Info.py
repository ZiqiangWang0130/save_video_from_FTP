#This script will retrieve the property of MP4 files such as File Name, File Size in bytes, Date, Time. Frame rate, duration and resolution and create a Excel spread sheet based on th video information

# before run the script, ensure all the local video file is valid- no crashed video, no 0 MB video and so on.
import csv 
import sys
import os
import xlrd 
import xlsxwriter
import xlwt
import subprocess
from datetime import datetime
from itertools import islice
from moviepy.editor import VideoFileClip


#get all the local mp4 files
storage_path = os.getcwd()
list_of_files_local = os.listdir(storage_path)
list_of_videos_local = [os.path.join(storage_path,i) for i in list_of_files_local if i.endswith(".mp4")]

localfile_name = []
date = []
time =[]
filesize = []
durations = []
framerate = []
resolution = []
datetimes = []

#get the file name, file size, date and time 
for local_video	in list_of_videos_local:
        file_size = os.path.getsize(local_video)
        local_video = os.path.basename(local_video)
        filesize.append(file_size)
        localfile_name.append(local_video)
        temp_date = local_video[13:28]
        temp_date = temp_date[:4]+'-'+temp_date[4:6]+'-'+temp_date[6:8]+' '+temp_date[9:11]+':'+temp_date[11:13]+':'+temp_date[13:]
        date.append(local_video[13:21])
        time.append(local_video[22:28])
        datetimes.append(temp_date)

#get the video info like duration, fps, resolution
for video in localfile_name:
		temp = VideoFileClip(video)
		duration = temp.duration
		fps = temp.fps
		h = temp.h
		w = temp.w
		pixel = str(h) + "x" + str(w)
		print (pixel)
		temp.reader.close()
		durations.append(duration)
		framerate.append(fps)
		resolution.append(pixel)

#####adding the discharge and stage value to the video info
stage = []
temp = []
stagelevel = []
discharge = []
dischargelevel = []
timestamp = []
#get the stage value to match the time
path = os.getcwd() + "\\" + 'Stage.Working@02LB006_20190612.csv'

with open(path) as csvDataFile:																			
    csvReader = csv.reader(csvDataFile)
    for row in islice(csvReader, 34, None):
     stage.append([row[0][0:19], row[1]])

#make the stage string to time object in order to comparing
for i in range(len(stage)):
	stage[i].append(datetime.strptime(stage[i][0], '%Y-%m-%d %H:%M:%S'))

#get the discharge value to match the time
path2 = os.getcwd() + "\\" + 'Discharge.Working@02LB006_20190612.csv'
with open(path2) as csvDataFile:																			
    csvReader = csv.reader(csvDataFile)
    for row in islice(csvReader, 34, None):
     discharge.append([row[0][0:19], row[1]])

#make the discharge string to time object in order to comparing
for i in range(len(discharge)):
	discharge[i][0] = datetime.strptime(discharge[i][0], '%Y-%m-%d %H:%M:%S')

#get the time for video
new_path = os.getcwd() + "\\" + 'Video brief summary.xlsx'

#choose the third sheet from the excel file
wb = xlrd.open_workbook(new_path) 
sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows):
	temp.append(sheet.cell_value(i, 0))
	temp[i] = temp[i][13:28]
temp.pop(0)      #remove the title in the excel sheet

#make the datetime string to time object from excel
for i in range(len(temp)):
	temp[i] = datetime.strptime(temp[i], '%Y%m%d_%H%M%S')

#create the list of stage value 
for i in temp:
	for t in stage:
		if t[2] > i:
			stagelevel.append(t[1])
			timestamp.append(t[0])
			break			

#create the list of stage value
for i in temp:
	for t in discharge:
		if t[0] > i:
			dischargelevel.append(t[1])
			break		

		
# formatting the data in the spread sheet 
workbook = xlsxwriter.Workbook('Video brief summary.xlsx')
worksheet = workbook.add_worksheet()

row = 0
worksheet.write(row, 0, 'File Name')
worksheet.write(row, 1, 'File Size (bytes)')
worksheet.write(row, 2, 'Date')
worksheet.write(row, 3, 'Time')
worksheet.write(row, 4, 'Datetime')
worksheet.write(row, 5, 'Closest Datetime in Aquarius')
worksheet.write(row, 6, 'Stage(m)')
worksheet.write(row, 7, 'Discharge(m3/s)')
worksheet.write(row, 8, 'Frame Rate (fps)')
worksheet.write(row, 9, 'Duration (s)')
worksheet.write(row, 10, 'Resolution (The hight and width of the video in pixel)')
worksheet.write(row, 11, 'Camera Position')
worksheet.write(row, 12, 'Control Point Visibility')


row = 1
for video in localfile_name:
	worksheet.write(row, 0, video)
	row += 1

row = 1
for file in filesize:
	worksheet.write(row, 1, file)
	row += 1

row = 1
for day in date:
	worksheet.write(row, 2, day)
	row += 1

row = 1
for times in time:
	worksheet.write(row, 3, times)
	row += 1

row = 1
for time in datetimes:
	worksheet.write(row, 4, time)
	row += 1

row = 1
for value in timestamp:
	worksheet.write(row, 5, value)
	row +=1

row = 1
for value in stagelevel:
	worksheet.write(row, 6, value)
	row +=1

row = 1
for value in dischargelevel:
	worksheet.write(row, 7, value)
	row +=1

row = 1
for fps in framerate:
	worksheet.write(row, 8, fps)
	row += 1

row = 1
for period in durations:
	worksheet.write(row, 9, period)
	row += 1

row = 1
for res in resolution:
	worksheet.write(row, 10, res)
	row += 1



workbook.close()