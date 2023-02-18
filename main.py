from dataclasses import dataclass
import numpy as np
from PIL import Image, ImageDraw

# Up to 64k resolution
class Video:
    Final = np.array([])
    t = np.double(0)
    step = np.double(1/300)
    def __init__(self, f, /, Lerp:np.bool_=False, *, MinX:np.short=np.short(-10), MaxX:np.short=np.short(10), MinY:np.short=np.short(-10), MaxY:np.short=np.short(10), Res:np.uintc=np.uintc(8_294_400)) -> None:
        Res = 408_960
        Res = 8_000
        self.XMin, self.YMin = MinX, MinY
        self.Points = list()
        Sqrt = np.ushort(np.sqrt(Res))
        self.Sqrt = Sqrt
        self.XDiff, self.YDiff = np.double(Sqrt/(MaxX-MinX)), np.double(Sqrt/(MaxY-MinY))
        XStep = (MaxX-MinX)/Sqrt
        YStep = (MaxY-MinY)/Sqrt
        self.Image = Image.new('RGB', (Sqrt, Sqrt), color='black')
        self.Draw = ImageDraw.Draw(self.Image)
        Index = 0
        x = MinX
        while x < MaxX:
            y = MinY
            while y < MaxY:
                Coords = np.csingle(x+y*1j)
                self.Points.append(Point(Coords, f(Coords), True))
                Index += 1
                y += YStep
            x += XStep
        self.Points = np.array(self.Points)
        self.FirstSave()
    
    def FirstSave(self):
        Max, Min = -float('inf'), float("inf")
        for D in self.Points:
            Module = D.Module
            Max = max(Module, Max)
            Min = min(Module, Min)
        for D in self.Points:
            D.color = HSLtoHEX(D.Arg+180, (D.Module-Min)/(Max-Min))
            del D.Arg
            del D.Module
    
    def Save(self):
        for D in self.Points:
            x, y, Color = D.Get(self.t)
                
            self.Draw.point((x,y), Color)
        print(self.t/self.step)
        self.Image.save(f'images/{int(round(self.t/self.step, 0))}.png', 'PNG')
        self.Image.close()
        self.Image = Image.new('RGB', (self.Sqrt, self.Sqrt), color='black')
        self.Draw = ImageDraw.Draw(self.Image)
    
    def __iter__(self):
        return iter(self.Points)
    
    def __next__(self):
        self.t += self.step


@dataclass
class Point:
    origin: np.csingle
    end: np.csingle
    lerp: np.bool_ = False
    Third: np.csingle = np.csingle(0)
    color: np.ushort = np.ushort(0)
    
    def __post_init__(self):
        self.Module, self.Arg = np.absolute(self.origin), np.angle(self.origin, deg=True)
        if not self.lerp: 
            self.Current = self.LerpWt
            return
        self.Third = (self.origin+self.end)/2 + 3*(np.csingle((self.end-self.origin).imag - 1j*((self.end-self.origin).real))/np.abs(self.end-self.origin))
        self.Current = self.LerpW
        
    def LerpW(self, t) -> np.csingle:
        return (self.origin+self.end-2*self.Third)*t**2 + 2*(self.Third-self.origin)*t + self.origin

    def LerpWt(self, t) -> np.csingle:
        return self.end*t + self.origin*(1-t)
    
    def Get(self, t):
        Nbr = self.Current(t)
        return Nbr.real, Nbr.imag, self.color

def HSLtoHEX(h, s):
    L = np.half(0.4)
    a = np.half(s*L)
    def F(n):
        k = (n+h/30)%12
        return L - a * max(min(k-3, 9-k, 1), -1)
    return np.ubyte(F(0)*255), np.ubyte(F(8)*255), np.ubyte(F(4)*255)
    
        
    
def f(Coords:np.csingle):
    return Coords**2j + 9j - Coords**2

L = Video(f, False)
print('lourd')
for _ in L:
    L.Save()
    L.__next__()
    if L.t >= 1:
        break