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
    visina, sirina = slika.shape[:2]
    centri = []

    # Izberemo naključne centre
    if izbira == "nakljucno":
        x = np.random.randint(0, sirina)
        y = np.random.randint(0, visina)
            
        barva = slika[y, x]
        if dimenzija_centra == 5:
            center = np.array([x, y, barva[0], barva[1], barva[2]])
            # print(f"Center: {center}")
        elif dimenzija_centra == 3:
            center = np.array([x,y, barva])
            # print(f"Center: {center}")
        
    elif izbira == "nakljucno":
        pass
    

if __name__ == "__main__":
    print("Naloga 3: Segmentacija slik")