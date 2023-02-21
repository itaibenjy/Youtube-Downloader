# YouTube Downloader

This application I wrote in Python using [pytube](https://github.com/pytube/pytube) to download YouTube videos, [custometkinter](https://github.com/TomSchimansky/CustomTkinter) as the UI-library which is based on Tkinter, and [moviepy](https://github.com/Zulko/moviepy) to attach audio to video files.

## Table of Contents 
* [Find via URL](#find-via-url)
* [Search](#search)
* [Downloads](#download)
* [Merging Audio and Video files](#merge-audio-and-video-files)
* [Settings](#settings)
* [Additional Features](#additional-features)

## Find via URL
This feature allows the User to paste a URL of the wanted YouTube video, Once the Find by URL button is pressed a tab view will load, the main tab is the Details tab with the YouTube Video thumbnail and details, the second tab is the Downloads tab where the user choose the wanted Type, Resolution, Format and FPS they want to download in.(This is the only place where the filter and download of YouTube streams is happening)

![URL-details](screenshots/URL-Details.png)
![URL-downloads](screenshots/URL-Downloads.png)
## Search 
This feature allows the User to search for a YouTube video as they would search for it on the YouTube website. When the search button pressed the videos will load in a scrollable frame, Once the User pressed the wanted video, he will be transfer to the URL frame with the video URL already pasted and the tab view already loading (see [find via URL](#find-via-url)).

![Search](screenshots/Search.png)
## Downloads
The Downloads frame consist of a tab view of "Completed" and "Downloading" tabs which the Downloading tab hold and display information of the ongoing downloads (thumbnail, type, resolution format, fps, and percentage of the download that is completed).
The Completed tab holds the information of the completed downloads (thumbnail, type, resolution format, fps, size), also allows to delete and open each completed download. The completed downloads are saved in a Json file and loaded from the file when the program starts.

![Downloads-Downloading](screenshots/Downloads-Downloading.png)
![Downloads-Completed](screenshots/Downloads-Completed.png)
## Merging Audio and Video Files
As the YouTube video streams available for downloads which include both video and audio is capped at a 720p resolution I wanted to find a solution to be able to download the videos in the highest Resolutions. The solution, combine Video Only and Audio Only files once they are downloads to a single video file.

In the Completed downloads tab of the [Downloads](#downloads) frame there is a Combine Mode toggle switch, once switched on every Completed downloads will have a checkbox near it, this allows the user to choose one Video only and one Audio only downloads of the same YouTube video and Combine them to one file (This is using the [movipy](https://github.com/Zulko/moviepy) library), this feature using the CPU heavily as it exports a new video.


![Merging](screenshots/Merging.png)
## Settings 
The Setting frame allows the user to chose an Appearance mode (Light of Dark, Dark is default), a Theme color (Blue, Green, Red, Purple, Yellow, Orange, Red is the default) and a Download location where all downloads will be saved at (default is the User Downloads folder).

![Settings](screenshots/Settings.png)
![Themes-Appearance](screenshots/Themes-Appearances.png)
## Additional Features
The program uses help tips on most elements for User guidance when the user put his mouse and doesn't move it more than 0.3 seconds, (for example the navigation bar that uses Icons, the titles of videos where they are too long, and most buttons).

The program also uses Alerts and Information dialogs for when a confirmation is needed or an additional guidance is required.

![Dialog-Alert](screenshots/alert-dialog.png)
![Dialog-Information](screenshots/information-dialog.png)
![Help-tip](screenshots/help-tip.png)
## Download and Use
This program is for personal use only. 

To Download and Use: soon
