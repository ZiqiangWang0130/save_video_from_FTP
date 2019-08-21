# Hi everyone, the purpose of this scripts is to automate the process of backing up the videos we have in the FTP
#to our local desktop and potentially into our shared drive. Enjoy, Ziqiang.


####################The Scripts start here######################

#Import the standard module we need to use, BTW, we do not need to install other module such as "datetime" is because
#all those additional steps are make when we creating/recording/transferring the video from the camera to Pi
import sys
import os
import ftplib
from ftplib import FTP

def LocalNewVideo():

    #set the ftp address and credentials
    ftp_address = 'depot.cmc.ec.gc.ca'
    ftp_user = 'liul'
    ftp_pwd = 'wWAQQU+q'
    ftp_directory = '/FieldData/ON/video_test'
	# setting up the max time for communication between local and ftp to 300 s 
    ftp_maxtime = 300                
	#get the current path if you want to save the video and images on the folder where you keep the python code
    localfile_name = []
    video_number_downloaded = 0
    image_number_downloaded = 0
    storage_path = os.getcwd()
	#connecting the ftp server 
    session = ftplib.FTP(ftp_address, ftp_user, ftp_pwd, ftp_maxtime)
    session.cwd(ftp_directory)
    filelist = session.nlst()
    #go through all the videos and images already exist in local so that we don't download the redundant videos
    list_of_files_local = os.listdir(storage_path)
    list_of_videos_local = [os.path.join(storage_path,i) for i in list_of_files_local if i.endswith(".mp4")]
    list_of_images_local = [os.path.join(storage_path,i) for i in list_of_files_local if i.endswith(".jpeg")]
    list_of_videos_images_local = list_of_videos_local + list_of_images_local 
    # grab the file name instead of path
    for local_video_images	in list_of_videos_images_local:
        local_video_images = os.path.basename(local_video_images)
        localfile_name.append(local_video_images)
	#do the comparing 
    for files in filelist:
        if files.endswith(".mp4") or files.endswith(".jpeg"):
            if files not in localfile_name:
                print (files)
                localfile = open(files,'wb')
                session.retrbinary('RETR '+ files, localfile.write)  #write the file to local
                if files.endswith(".mp4"):
                   video_number_downloaded += 1
                if files.endswith(".jpeg"):
                   image_number_downloaded +=1
                localfile.close()
    print ("successfully download " + str(video_number_downloaded) +" videos and " + str(image_number_downloaded) +" images. Please close the program.")
    session.quit()
        
if __name__ == "__main__":
    LocalNewVideo()