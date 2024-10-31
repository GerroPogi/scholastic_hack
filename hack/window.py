import logging
import tkinter
from typing import Optional

class Window(tkinter.Tk):
    widgets={}
    def __init__(self,size):
        super().__init__()
        self.geometry(size)
    def add_entry(self,name:str,size:int = 10,default_entry="",font=('Arial 24'),pos=[]):
        logging.info("Created entry: %s", name)
        
        entry=tkinter.Entry(self,width=size,font=font,textvariable=default_entry)
        if pos:
            entry.place(x=pos[0],y=pos[1])
        else:
            entry.pack()
        self.widgets[name]=entry
    
    def add_scale(self,name,from_,to,default,orient=tkinter.HORIZONTAL,pos=[]):
        logging.info("Created scale: %s", name)
        
        scale=tkinter.Scale(self,orient=orient,from_=from_,to=to,variable=tkinter.DoubleVar(value=default))
        if pos:
            scale.place(x=pos[0],y=pos[1])
        else:
            scale.pack()
        self.widgets[name]=scale
    
    def get_widget(self,widget:str):
        return self.widgets[widget]
    
    def add_button(self,name:str,text:str,command,size:int = 10,font=('Arial 24'),pos=[],**kwargs):
        logging.info("Created button: %s", name)
        
        button=tkinter.Button(self,text=text,width=size,font=font,command=command)
        button.configure(**kwargs)
        if pos:
            button.place(x=pos[0],y=pos[1])
        else:
            button.pack()
        self.widgets[name]=button
    def add_label(self, name:str, text:str,font=('Arial 24'),pos=[],**kwargs):
        logging.info("Created label: %s", name)
        label=tkinter.Label(text=text,font=font)
        label.configure(**kwargs)
        if pos:
            label.place(x=pos[0],y=pos[1])
        else:
            label.pack()
        self.widgets[name]=label
    def add_box(self,name,size,color,pos=[],**kwargs):
        box= Box(self,size,pos,color,**kwargs)
        box.packs()
        self.widgets[name]=box
    
    def run(self):
        self.mainloop()
    def get_pos(self):
        return self.winfo_x(),self.winfo_y()
    def set_alpha(self, alpha:float):
        self.attributes('-alpha',alpha)
    
    def add_dropdown(self, name,default,options,pos=[]):
        logging.info("Created dropdown: %s", name)
        
        var=tkinter.StringVar()
        var.set(default)
        dropdown=tkinter.OptionMenu(self,var,*options)
        
        if pos:
            dropdown.place(x=pos[0],y=pos[1])
        else:
            dropdown.pack()
        self.widgets[name]=[dropdown,var]
    def set_size(self,size:list):
        self.geometry(str(size[0])+"x"+str(size[1]))
    def set_color(self,color:Optional[list|str]):
        logging.info("Set color to: %s", color)
        
        if type(color)==str:
            self.configure(bg=color)
        if type(color)==list:
            self.configure(bg='#%02x%02x%02x' % color)
    def add_checkbox(self,name,text,default=False,pos=[],**kwargs):
        logging.info("Created checkbox named: %s",name)
        self.widgets[name]=[0,default]
        checkBox=tkinter.Checkbutton(self,text=text,command=lambda: self.widgets[name].__setitem__(1,not self.widgets[name][1]),**kwargs)
        checkBox.toggle() if default else 0
        if pos:
            checkBox.place(x=pos[0],y=pos[1])
        else:
            checkBox.pack()
    

class Box(tkinter.Frame):
    widgets={}
    def __init__(self,master,size,pos=[],color=None,**kwargs):
        super().__init__(master=master,bg=color,width=size[0],height=size[1],**kwargs)
        self.pos=pos
        self.size=size
        self.new_pos=pos
        self.width=size[0]
        self.height=size[1]
    def center(self):
        return self.new_pos[0] + (self.width/2),self.new_pos[1] + (self.height/2)
    
    def add_checkbox(self,name,text,default=False,pos=[],**kwargs):
        logging.info("Created checkbox named: %s",name)
        self.widgets[name]=[0,tkinter.IntVar(self,value=1 if default else 0)]
        
        checkBox=tkinter.Checkbutton(
            self,
            text=text,
            command=lambda: print(self.widgets[name][1].get()),
            variable=self.widgets[name][1],
            onvalue=1,
            offvalue=0,
            **kwargs
            )
        if pos:
            checkBox.place(x=pos[0],y=pos[1])
        else:
            checkBox.pack()
        
        
        self.widgets[name][0]=checkBox
    
    def get_relative_corners(self):
        return [int(self.new_pos[0]),int(self.new_pos[1]),int(self.new_pos[0]+self.width),int(self.new_pos[0]+self.height)]
        
    def get_corners(self,master_pos=[0,0]):
        x=master_pos[0]+self.new_pos[0]+8
        y=master_pos[1]+self.new_pos[1]+32
        return [int(x),int(y),int(x+self.width),int(y+self.height)]
    def packs(self):
        
        if self.pos:
            self.place(x=self.pos[0],y=self.pos[1])
        else:
            self.pack()
    def add_entry(self,name:str,size:int = 10,default_entry="",font=('Arial 24'),pos=[]):
        
        entry=tkinter.Entry(master=self,width=size,font=font,textvariable=default_entry)
        if pos:
            entry.place(x=pos[0],y=pos[1])
        else:
            entry.pack()
        self.widgets[name]=entry
    def add_scale(self,name,from_,to,default,orient=tkinter.HORIZONTAL,pos=[],**kwargs):
        logging.info("Created scale: %s", name)
        
        scale=tkinter.Scale(self,orient=orient,from_=from_,to=to,variable=tkinter.DoubleVar(value=default),**kwargs)
        if pos:
            scale.place(x=pos[0],y=pos[1])
        else:
            scale.pack()
        self.widgets[name]=scale
    
    def get_widget(self,widget:str):
        return self.widgets[widget]
    
    def add_button(self,name:str,text:str,command,size:int = 10,font=('Arial 24'),pos=[]):
        
        button=tkinter.Button(master=self,text=text,width=size,font=font,command=command)
        if pos:
            button.place(x=pos[0],y=pos[1])
        else:
            button.pack()
        self.widgets[name]=button
    def add_label(self, name:str, text:str,font=('Arial 24'),pos=[],**kwargs):
        label=tkinter.Label(master=self,text=text,font=font,**kwargs)
        if pos:
            label.place(x=pos[0],y=pos[1])
        else:
            label.pack()
        self.widgets[name]=label
        
    def set_color(self,color):
        self.config(fg=color)

class DraggableBox(Box):
    def __init__(self,size,pos=[],color=None,master=None):
        super().__init__(master,size,pos,color=color)
        self.new_pos=pos
        
        self.root = self.winfo_toplevel()
        self.bind("<B1-Motion>",self.on_drag)
        self.bind("<ButtonRelease>",self.on_drop)
        self.configure(cursor="hand1")
        
    def on_drag(self,event):
        self.place(x=self.root.winfo_pointerx()-self.root.winfo_rootx(),y=self.root.winfo_pointery()-self.root.winfo_rooty())
    
    def place_on_screen(self,x,y):
        self.place(x=x-self.root.winfo_rootx(),y=y-self.winfo_rooty())
    
    def on_drop(self,event):
        self.place(x=self.root.winfo_pointerx()-self.root.winfo_rootx(),y=self.root.winfo_pointery()-self.root.winfo_rooty())
        self.new_pos=[self.root.winfo_pointerx()-self.root.winfo_rootx(),self.root.winfo_pointery()-self.root.winfo_rooty()]
    
    