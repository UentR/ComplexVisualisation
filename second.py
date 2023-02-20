import numpy as np
from PIL import Image, ImageDraw
import cv2

class Grid:
    Width = 2
    def __init__(self, f, Res:np.ushort=np.ushort(4000), Square:np.ushort=np.ushort(2), CenterX:np.short=np.short(0), CenterY:np.short=np.short(0), Radius:np.ushort=np.ushort(10)) -> None:
        self.Out = cv2.VideoWriter('OutputVideo.avi', cv2.VideoWriter_fourcc(*'DIVX'), 60, (Res, Res))
        
        self.ImageNp = np.ones((Res+1, Res+1, 3), dtype=np.ubyte)
        
        self.Res = Res+1
        self.Lines = np.ndarray([2*Radius//Square+1, 2], dtype=np.object_)
        self.MinX, self.MaxX, self.MinY, self.MaxY = np.short(CenterX-Radius), np.short(CenterX+Radius), np.short(CenterY-Radius), np.short(CenterY+Radius)
        self.XRadius = np.double(Res/(self.MaxX-self.MinX))
        self.YRadius = np.double(Res/(self.MaxY-self.MinY))
        X = self.MinX
        Y = self.MinY
        Idx = 0
        while X <= CenterX+Radius:
            self.Lines[Idx] = [Line(f, Res, True, X, self.MinY, self.MaxY), Line(f, Res, False, Y, self.MinX, self.MaxX)]
            Idx += 1
            X += Square
            Y += Square
    
    def Save(self, t):
        for V, H in self.Lines:
            for i in range(self.Res):
                Coords1, Coords2 = V(i, t), H(i, t)
                y, x = np.round((np.real(Coords1)-self.MinX)*(self.XRadius),0), np.round((np.imag(Coords1)-self.MinY)*(self.YRadius),0)
                if 0 < x <= self.Res and 0 <= y < self.Res:
                    self.ImageNp[self.Res-int(x)][int(y)] = (0,86,137)
                    
                y, x = np.round((np.real(Coords2)-self.MinX)*(self.XRadius),0), np.round((np.imag(Coords2)-self.MinY)*(self.YRadius),0)
                if 0 < x <= self.Res and 0 <= y < self.Res:
                    self.ImageNp[self.Res-int(x)][int(y)] = (255,137,93)
        self.Out.write(self.ImageNp)
        self.ImageNp = np.ones((self.Res, self.Res, 3), dtype=np.ubyte)
        


class Line:
    def __init__(self, f, Res:np.ushort=np.ushort(4000),  V:np.bool_=np.bool_(True), Pad:np.short=np.short(-10), Start:np.short=np.short(-10), End:np.short=np.short(10)) -> None:
        self.Points = np.ndarray((Res+1, 2), dtype='F')
        
        Pas = np.double((End-Start)/Res)
        Index = 0
        while Index<=Res:
            i = Start + Pas*Index
            if V: Point = np.csingle(Pad+i*1j)
            else: Point = np.csingle(i+Pad*1j)
            self.Points[Index] = [Point, f(Point)]
            Index += 1
                
        self.Points.flags.writeable = False
    
    def __call__(self, Index=0, t=0):
        return self.Points[Index][0]*(1-t) + self.Points[Index][1]*t

    def __repr__(self) -> str:
        return f'{self.Points[0][0]}, {self.Points[-1][0]}'

def func(Coords:np.csingle):
    # return Coords*1j + 1 + 1j
    return np.round(Coords**2j + 9j - Coords**2, 5)


U = Grid(func, 500)

Nbr = 300
for i in range(Nbr+1):
    U.Save(i/Nbr)
    print(i)
U.Out.release()