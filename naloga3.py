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
    visina, sirina, kanali = slika.shape

    

def meanshift(slika, velikost_okna, dimenzija):
    '''Izvede segmentacijo slike z uporabo metode mean-shift.'''
    pass

def izracunaj_centre(slika, izbira, dimenzija_centra, T, k):
    '''Izračuna centre za metodo kmeans.'''
    visina, sirina = slika.shape[:2]
    centri = []

    # Izberemo naključne centre
    if izbira == "nakljucno":
        while len(centri) < k:
            x = np.random.randint(0, sirina)
            y = np.random.randint(0, visina)
                
            barva = slika[y, x]

            if dimenzija_centra == 5:
                center = np.array([x, y, barva[0], barva[1], barva[2]])
                # print(f"Center: {center}")
            elif dimenzija_centra == 3:
                center = np.array([x,y, barva])
                # print(f"Center: {center}")

            if not centri:
                    centri.append(center)
            else:
                # Ali je center dovolj oddaljen od ostalih centrov
                oddaljenost_array = []
                for c in centri:
                    oddaljenost = evklidska_razdalja(center, c, dimenzija_centra)
                    oddaljenost_array.append(oddaljenost)
                    min_oddaljenost = min(oddaljenost_array)
                if min_oddaljenost > T:
                        centri.append(center)
                        
        return centri
    
    elif izbira == "rocno":
        izbrane_tocke = []

        def onclick(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN:
                barva = slika[y, x]
                if dimenzija_centra == 5:
                    center = np.array([x, y, barva[0], barva[1], barva[2]])
                elif dimenzija_centra == 3:
                    center = np.array([x, y, barva])
                izbrane_tocke.append(center)
                print(f"Izbran center {len(izbrane_tocke)}: {center}")
                cv.circle(slika, (x, y), 5, (0, 255, 0), -1)
                cv.imshow("Izvorna slika", slika)

                if len(izbrane_tocke) == k:
                    cv.destroyAllWindows()

        print(f"Klikni {k} točk na sliki za določitev centrov.")
        cv.imshow("Izvorna slika", slika)
        cv.setMouseCallback("Izvorna slika", onclick)
        cv.waitKey(0)
        cv.destroyAllWindows()

        return izbrane_tocke
    

if __name__ == "__main__":
    print("Naloga 3: Segmentacija slik")