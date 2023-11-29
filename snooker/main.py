import tkinter as tk
from tkinter import ttk
from gui import select_video, select_output_directory, start_process

if __name__ == '__main__':
    # create the root window
    root = tk.Tk()
    root.title('Snooker point counter')
    root.resizable(False, False)
    root.geometry('600x300')
    root.grid_anchor('center')

    # create label to selected video
    selected_video_label = ttk.Label(
        root,
        text="Selected video: Video isn't selected!"
    )
    selected_video_label.grid(row=0, column=0)

    # create button to select video
    select_video_button = ttk.Button(
        root,
        text='Select video',
        command=lambda: select_video(selected_video_label)
    )
    select_video_button.grid(row=1, column=0)

    # create label to selected output directory
    selected_output_directory_label = ttk.Label(
        root,
        text="Selected output directory: Directory isn't selected!"
    )
    selected_output_directory_label.grid(row=3, column=0)

    # create button to select output directory
    select_output_directory_button = ttk.Button(
        root,
        text='Select output directory',
        command=lambda: select_output_directory(selected_output_directory_label)
    )
    select_output_directory_button.grid(row=4, column=0)

    # create start process button
    start_button = ttk.Button(
        root,
        text='Start process',
        command=start_process
    )
    start_button.grid(row=6, column=0)

    root.mainloop()
