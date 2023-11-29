from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning
from process import process_video

filename = ''
output_video_path = ''


def select_video(label):
    global filename
    filetypes = (
        ('mp4', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select a video',
        initialdir='/',
        filetypes=filetypes)

    if filename:
        label.configure(text="Selected video: " + filename)
    else:
        showwarning(
            title='Warning',
            message='Video isn\'t selected!'
        )


def select_output_directory(label):
    global output_video_path

    output_video_path = fd.askdirectory(
        title='Select the output directory',
        initialdir='/')

    if output_video_path:
        label.configure(text="Selected output directory: " + output_video_path)
    else:
        showwarning(
            title='Warning',
            message='Directory isn\'t selected!'
        )


def start_process():
    if not filename:
        showerror(
            title='Error',
            message='Video isn\'t selected!'
        )
    elif not output_video_path:
        showerror(
            title='Error',
            message='Output folder isn\'t selected!'
        )
    else:
        process_video(filename, output_video_path + '/output_video.mp4')
