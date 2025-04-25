import cv2 as cv
import numpy as np
import math

def evklidska_razdalja(piksel, center, dimenzija):
    '''Izračuna Evklidsko razdaljo med pikslom in centrom.'''
    piksel = np.array(piksel, dtype=np.float64)
    center = np.array(center, dtype=np.float64)
    if dimenzija == 3:
        # Če imamo samo barvo
        dx = piksel[0] - center[0]
        dy = piksel[1] - center[1]
        ds = piksel[2] - center[2]
        return math.sqrt(dx*dx + dy*dy + ds*ds)
    elif dimenzija == 5:
        # Če imamo tudi lokacijo
        dx = piksel[0] - center[0]
        dy = piksel[1] - center[1]
        dr = piksel[2] - center[2]
        dg = piksel[3] - center[3]
        db = piksel[4] - center[4]
        return math.sqrt(dx*dx + dy*dy + dr*dr + dg*dg + db*db)

def kmeans(slika, k=3, iteracije=10):
    '''Izvede segmentacijo slike z uporabo metode k-means.'''
    pass

def meanshift(slika, velikost_okna, dimenzija):
    '''Izvede segmentacijo slike z uporabo metode mean-shift.'''
    pass

def izracunaj_centre(slika, izbira, dimenzija_centra, T):
    '''Izračuna centre za metodo kmeans.'''
    # Izberemo naključne centre
    if izbira == "nakljucno":
        if dimenzija_centra == 5:
            print("Izbrali smo naključne centre v 5D prostoru.")
        elif dimenzija_centra == 3:
            print("Izbrali smo naključne centre v 3D prostoru.")
        
    elif izbira == "nakljucno":
        pass
    

if __name__ == "__main__":
    print("Naloga 3: Segmentacija slik")