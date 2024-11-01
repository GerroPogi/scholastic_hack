from .grab import PySide6GrabWindow
from .window import DraggableBox
from pyautogui import locateCenterOnScreen,locateOnScreen
grab=PySide6GrabWindow()
class Choice(DraggableBox):
    def __init__(self,size,choice:str,pos=[],color=None,master=None):
        super().__init__(size,pos,color,master)
        self.choice=choice
        self.img=None
        if not pos:
            self.new_pos=[0,0]
    def get_choice_center_position(self):
        pos=locateCenterOnScreen("hack/scholastic/"+self.choice+".png",confidence=0.8)
        print(pos)
        assert pos is not None, "The choice: "+self.choice+" is not found"
        return pos[0],pos[1]
    def get_choice_position(self):
        pos=locateOnScreen("hack/scholastic/"+self.choice+".png")
        print(pos)
        assert pos is not None, "The choice: "+self.choice+" is not found"
        return pos[0],pos[1]
    def take_screenshot(self,master):
        self.img=grab.grab(bbox=self.get_corners([master.winfo_x(),master.winfo_y()]))
        return self.img
    def recheck_bounds(self):
        if self.choice in "ac":
            a=locateCenterOnScreen("hack/scholastic/a.png",confidence=0.8)
            c=locateCenterOnScreen("hack/scholastic/c.png",confidence=0.8)
            dis=abs((a[1]-c[1])/2)
            if self.choice=="a":
                self.new_pos[1]=a[1]-75
            if self.choice=="c":
                self.new_pos[1]=c[1]-dis
        if self.choice in "bd":
            b=locateCenterOnScreen("hack/scholastic/b.png",confidence=0.8)
            d=locateCenterOnScreen("hack/scholastic/d.png",confidence=0.9)
            dis=abs((b[1]-d[1])/2)
            if self.choice=="b":
                self.new_pos[1]=b[1]-75
            if self.choice=="d":
                self.new_pos[1]=d[1]-dis
        
        self.new_update()
    def new_update(self):
        self.place(x=self.new_pos[0],y=self.new_pos[1])