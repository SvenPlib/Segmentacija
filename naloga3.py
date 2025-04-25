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

def kmeans(slika, k=3, iteracije=10, dimenzija=3):
    '''Izvede segmentacijo slike z uporabo metode k-means.'''
    visina, sirina, kanali = slika.shape

    if dimenzija == 3:
        slika_sivinska = cv.cvtColor(slika, cv.COLOR_BGR2GRAY)
        centri = izracunaj_centre(slika_sivinska, "nakljucno", dimenzija, 2, k)
        segmentirana_slika = np.zeros((visina, sirina), dtype=np.uint8)
    elif dimenzija == 5:
        centri = izracunaj_centre(slika, "nakljucno", dimenzija, 2, k)
        segmentirana_slika = np.zeros((visina, sirina, 3), dtype=np.uint8)
    
    oznake = np.zeros((visina, sirina), dtype=np.int32)

    for i in range(iteracije):
        if dimenzija == 3:
            # 1. Označimo vsak piksel s številko centra
            for y in range(visina):
                for x in range(sirina):
                    piksel = np.array([x, y, slika_sivinska[y,x]], dtype=np.float64)

                    # Izračunamo razdaljo do vseh centrov
                    razdalje = []
                    for center in centri:
                        razdalja = evklidska_razdalja(piksel, center, dimenzija)
                        razdalje.append(razdalja)

                    # Najdemo najbližji center
                    min_razdalja = min(razdalje)
                    min_index = razdalje.index(min_razdalja)

                    oznake[y,x] = min_index
            
            # 2. Izračunamo nove centre
            novi_centri = []

            for i in range(k):
                # Izberemo vse piksele, ki so dodeljeni centru i
                pikseli = []

                for y in range(visina):
                    for x in range(sirina):
                        if oznake[y,x] == i:
                            pikseli.append([x,y, slika_sivinska[y,x]])

                # Izračunamo povprečje
                if len(pikseli) > 0:
                    povprecje = np.mean(pikseli, axis=0)
                    novi_centri.append(povprecje)
                else:
                    novi_centri.append(centri[i])


        elif dimenzija == 5:
            # 1. Označimo vsak piksel s številko centra
            for y in range(visina):
                for x in range(sirina):
                    piksel = np.array([x, y, slika[y, x][0], slika[y, x][1], slika[y, x][2]], dtype=np.float64)
                    # Izračunamo razdaljo do vseh centrov
                    razdalje = []
                    for center in centri:
                        razdalja = evklidska_razdalja(piksel, center, dimenzija)
                        razdalje.append(razdalja)

                    # Najdemo najbližji center
                    min_razdalja = min(razdalje)
                    min_index = razdalje.index(min_razdalja)

                    # Dodelimo barvo centra
                    oznake[y, x] = min_index
            
            # 2. Izračunamo nove centre
            novi_centri = []

            for i in range(k):
                # Izberemo vse piksele, ki so dodeljeni centru i
                pikseli = []

                for y in range(visina):
                    for x in range(sirina):
                        if oznake[y,x] == i:
                            pikseli.append([x,y, slika[y,x][0], slika[y,x][1], slika[y,x][2]])

                # Izračunamo povprečje
                if len(pikseli) > 0:
                    povprecje = np.mean(pikseli, axis=0)
                    novi_centri.append(povprecje)
                else:
                    novi_centri.append(centri[i])


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

    slika = cv.imread(".utils/small.jpg")