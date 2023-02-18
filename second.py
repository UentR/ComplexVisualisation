import numpy as np
from PIL import Image, ImageDraw

class Grid:
    Width = 4
    def __init__(self, f, Res:np.ushort=np.ushort(4000), Square:np.ushort=np.ushort(2), CenterX:np.short=np.short(0), CenterY:np.short=np.short(0), Radius:np.ushort=np.ushort(10)) -> None:
        self.Image = Image.new('RGB', (Res, Res), color='black')
        self.Draw = ImageDraw.Draw(self.Image)
        
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
                x, y = np.round((np.real(Coords1)-self.MinX)*(self.XRadius),0), np.round((np.imag(Coords1)-self.MinY)*(self.YRadius),0)
                self.Draw.rectangle((x-self.Width, y-self.Width, x+self.Width, y+self.Width),(0, 255, 0))
                x, y = np.round((np.real(Coords2)-self.MinX)*(self.XRadius),0), np.round((np.imag(Coords2)-self.MinY)*(self.YRadius),0)
                self.Draw.rectangle((x-self.Width, y-self.Width, x+self.Width, y+self.Width), (0, 255, 0))
        Coords1 = np.csingle(0+0j)
        x, y = np.round((np.real(Coords1)-self.MinX)*(self.XRadius),0), np.round((np.imag(Coords1)-self.MinY)*(self.YRadius),0)
        self.Draw.rectangle((x-self.Width, y-self.Width, x+self.Width, y+self.Width),(255, 255, 255))
        self.Image.save(f'images2/{int(t*Nbr)}.png', 'PNG')
        self.Image.close()
        self.Image = Image.new('RGB', (self.Res-1, self.Res-1), color='black')
        self.Draw = ImageDraw.Draw(self.Image)


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
    return np.round(Coords**2, 5)


U = Grid(func, 1000)

Nbr = 100
for i in range(Nbr+1):
    U.Save(i/Nbr)