#!/usr/bin/python3
import os
import cv2 as cv
import numpy as np
from tkinter import *
import tkinter as tk
from PIL import Image as pitImg
from PIL import ImageTk
from tkinter import filedialog



gui = Tk()
gui.wm_title("Remove Watermark")
gui.geometry("1300x570") # 1280x620
gui.configure(bg='#202637')
gui.resizable(width=0, height=0)

def browseFiles():
    filename = filedialog.askopenfilename(initialdir= "/", title= "Select a File",filetypes = (("Text files", "*.mp4*"), ("all files", "*.*")))      
    video_stream(filename)

def SelectROI():
    global ROI_Selected
    x,y,w,h = cv.selectROI(frame, False)
    ROI_Selected= [x,y,w,h]
    cv.destroyAllWindows()

def SaveVideo():
    check_SaveVideo.set(TRUE)
    print("KernelSize:", check_GaussianBlur.get())



Label(gui, text=" Remove watermark from videos ", background='#343A40', foreground="white", font=("Courier", 30) ).place(x=200, y=25) 

y=105
mainFrame = Frame(gui)
mainFrame.place(x=15, y=y) 
lmain = tk.Label(mainFrame)
lmain.grid(row=0, column=0)  
Label(gui, text = " Original video ", background='#343A40', foreground="white").place(x=15, y=y) 

mainFrame2 = Frame(gui)
mainFrame2.place(x=580, y=y)   
lmain2 = tk.Label(mainFrame2)
lmain2.grid(row=50, column=50)        
Label(gui, text = " Processed Video - No Watermark ", background='#343A40', foreground="white").place(x=580, y=y) 



frame_menu = Frame(gui)
frame_menu.pack(fill=tk.Y, ipadx=80, side=tk.RIGHT)
x= 10;
Button(frame_menu, text="Select Video", command= browseFiles).place(x=x+10, y=10)  
Button(frame_menu, text="Select ROI", command= SelectROI).place(x=x+15, y=45)  

x2height= 1.4
x2width= 15
y= 20;

KernelSize= StringVar(frame_menu)
VGaussian= StringVar(gui)
CGaussian= StringVar(frame_menu)
VMedian= StringVar(frame_menu)
CMedian= StringVar(frame_menu)
VBlur= StringVar(frame_menu)
CBlur= StringVar(frame_menu)

Label(frame_menu, text="Kernel Size:").place(x=x-5, y=70+y)  
Entry(frame_menu, textvariable=KernelSize, width=x2width, bd=2).place(x=x, y=90+y) 
KernelSize.set("9,9")

Label(frame_menu, text="Value Gaussian:").place(x=x-5, y=120+y)  
Entry(frame_menu, textvariable=VGaussian, width=x2width, bd=2).place(x=x, y=140+y) 

Label(frame_menu, text="Counter Gaussian:").place(x=x-5, y=170+y)  
Entry(frame_menu, textvariable=CGaussian, width=x2width, bd=2).place(x=x, y=190+y) 

Label(frame_menu, text="Value MedianBlur:").place(x=x-5, y=220+y)  
Entry(frame_menu, textvariable=VMedian, width=x2width, bd=2).place(x=x, y=240+y) 

Label(frame_menu, text="Counter MedianBlur:").place(x=x-5, y=270+y)  
Entry(frame_menu, textvariable=CMedian, width=x2width, bd=2).place(x=x, y=290+y) 

Label(frame_menu, text="Kernel Size Blur:").place(x=x-5, y=320+y)  
Entry(frame_menu, textvariable=VBlur, width=x2width, bd=2).place(x=x, y=340+y) 

Label(frame_menu, text="Counter Blur:").place(x=x-5, y=370+y)  
Entry(frame_menu, textvariable=CBlur, width=x2width, bd=2).place(x=x, y=390+y) 

check_GaussianBlur = BooleanVar()
check_MedianBlur = BooleanVar()
check_Blur = BooleanVar()
check_RepeatVideo = BooleanVar()
check_SaveVideo = BooleanVar()

y=190
Checkbutton(frame_menu, onvalue=1, offvalue=0, name="gaussianBlur", variable=check_GaussianBlur).place(x=x-5, y=260+y) 
Label(frame_menu, text="GaussianBlur").place(x=x+20, y=260+y)
check_GaussianBlur.get()

Checkbutton(frame_menu, onvalue=1, offvalue=0, name="medianBlur", variable=check_MedianBlur).place(x=x-5, y=280+y) 
Label(frame_menu, text="MedianBlur").place(x=x+20, y=280+y)

Checkbutton(frame_menu, onvalue=1, offvalue=0, name="blur", variable=check_Blur).place(x=x-5, y=300+y) 
Label(frame_menu, text="Blur").place(x=x+20, y=300+y) 

Checkbutton(frame_menu, onvalue=1, offvalue=0, name="repeatVideo", variable=check_RepeatVideo).place(x=x-5, y=320+y) 
Label(frame_menu, text="Repeat Video").place(x=x+20, y=320+y) 

Checkbutton(frame_menu, onvalue=1, offvalue=0, name="saveVideo", variable=check_SaveVideo).place(x=x-5, y=350+y) 
Label(frame_menu, text="Save Video").place(x=x+20, y=350+y) 


frameframe= FALSE
ROI_Selected= FALSE


FileAddr= FALSE
VidWriter= FALSE
def video_stream(addr=0):
    global FileAddr, VidWriter;
    if FileAddr:
        addr= FileAddr
    else:
        FileAddr= addr

    cap= cv.VideoCapture(addr)
    if check_SaveVideo.get():
        fourcc= cv.VideoWriter_fourcc(*'mp4v')
        VideoSize= (int(cap.get(3)),int(cap.get(4)))
        VidWriter = cv.VideoWriter("./Result.mp4", fourcc, 20.0, VideoSize) #cv2.VideoWriter_fourcc(*'XVID')
        print("Start Write. Size Video:", VideoSize)

    def play_video():
        global frame, VideoWrite, VidWriter;
        ret, frame = cap.read()

        if not ret:
            if check_SaveVideo.get():
                print("Stop Write")
                VidWriter.release()
                check_SaveVideo.set(FALSE)
            if check_RepeatVideo.get():
                video_stream()
            return;

        frame_processed= frame.copy()

        Ksize=(3,3);
        try:
            XKernelSize= KernelSize.get().split(",")
            if int(XKernelSize[0])>2 and int(XKernelSize[1])>2:
                Ksize= (int(XKernelSize[0]),int(XKernelSize[1]))
        except:
            print("ERROR KernelSize", KernelSize.get())    


        if check_GaussianBlur.get():    
            Gvalue=0
            GCounter=1
            try:
                Gvalue= int(VGaussian.get());
            except:
                pass

            try:
                GCounter= int(CGaussian.get())
            except:
                pass

            if ROI_Selected:
                [x,y,w,h]= ROI_Selected
                for i in range(GCounter):
                    blurred_img= cv.GaussianBlur(frame_processed[y:y+h,x:x+w], Ksize, Gvalue)
                    frame_processed[y:y+h,x:x+w]= blurred_img
            else:
                for i in range(GCounter):
                    frame_processed= cv.GaussianBlur(frame_processed, Ksize, Gvalue)

        if check_MedianBlur.get():
            Mvalue=1
            MCounter=1
            try:
                if int(VMedian.get()) %2 != 0:
                    Mvalue= int(VMedian.get());
            except:
                pass

            try:
                MCounter= int(CMedian.get())
            except:
                pass

            if ROI_Selected:
                [x,y,w,h]= ROI_Selected
                min_Mvalue=1
                if Mvalue>=2:
                    t=2
                    if Mvalue>=10:
                        t=4
                    min_Mvalue= int(Mvalue/t)
                    if min_Mvalue %2 == 0 and min_Mvalue>=2:
                        min_Mvalue-=1
                    
                for i in range(MCounter):
                    bias= 5
                    blurred_img= cv.medianBlur(frame_processed[y:y+h,x:x+w], Mvalue)
                    frame_processed[y:y+h,x:x+w]= blurred_img
                    blurred_img= cv.medianBlur(frame_processed[y-bias:y+h+bias,x-bias:x+w+bias], min_Mvalue)
                    frame_processed[y-bias:y+h+bias,x-bias:x+w+bias]= blurred_img
            else:
                for i in range(MCounter):
                    frame_processed= cv.medianBlur(frame_processed, Mvalue)

        if check_Blur.get():
            BKsize=(1,1)
            BCounter=1
            try:
                BKernelSize= VBlur.get().split(",")
                if int(BKernelSize[0])>0 and int(BKernelSize[1])>0:
                    BKsize= (int(BKernelSize[0]),int(BKernelSize[1]))
            except:
                pass

            try:
                BCounter= int(CBlur.get())
            except:
                pass

            if ROI_Selected:
                [x,y,w,h]= ROI_Selected
                for i in range(BCounter):
                    blurred_img= cv.blur(frame_processed[y:y+h,x:x+w], BKsize)
                    frame_processed[y:y+h,x:x+w]= blurred_img
            else:
                for i in range(BCounter):
                    frame_processed= cv.blur(frame_processed, BKsize)


        if check_SaveVideo.get():
            try:
                VidWriter.write(frame_processed)
            except:
                print("ERROR write.", VidWriter)
        

        ###############  Show Video in windows  ###############
        frame= cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_processed= cv.cvtColor(frame_processed, cv.COLOR_BGR2RGB)

        img= pitImg.fromarray(frame).resize((550, 450))
        imgtk = ImageTk.PhotoImage(image = img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

        frame_detect= pitImg.fromarray(frame_processed).resize((550, 450))
        imgtk2= ImageTk.PhotoImage(image = frame_detect)
        lmain2.imgtk = imgtk2
        lmain2.configure(image=imgtk2)
        lmain2.after(10, play_video)
    
    play_video()


# video_stream("sh.mp4")

mainloop()