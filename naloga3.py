import cv2 as cv
import numpy as np
import math

def evklidska_razdalja(piksel, center, dimenzija):
    '''Izračuna Evklidsko razdaljo med pikslom in centrom.'''
    piksel = np.array(piksel, dtype=np.float64)
    center = np.array(center, dtype=np.float64)
    if dimenzija == 3:
        # Če imamo samo barvo
        dr = piksel[0] - center[0]
        dg = piksel[1] - center[1]
        db = piksel[2] - center[2]
        return math.sqrt(dr*dr + dg*dg + db*db)
    elif dimenzija == 5:
        # Če imamo tudi lokacijo
        dx = piksel[0] - center[0]
        dy = piksel[1] - center[1]
        dr = piksel[2] - center[2]
        dg = piksel[3] - center[3]
        db = piksel[4] - center[4]
        return math.sqrt(dx*dx + dy*dy + dr*dr + dg*dg + db*db)
    
def gaussovo_jedro(d, h):
    return np.exp(-d**2 / (2 * h**2))

def kmeans(slika, k=3, iteracije=10, dimenzija=5):
    '''Izvede segmentacijo slike z uporabo metode k-means.'''
    visina, sirina, kanali = slika.shape

    if dimenzija == 3:
        centri = izracunaj_centre(slika, "nakljucno", dimenzija, 5, k)
        segmentirana_slika = np.zeros((visina, sirina, 3), dtype=np.uint8)
    elif dimenzija == 5:
        centri = izracunaj_centre(slika, "rocno", dimenzija, 200, k)
        segmentirana_slika = np.zeros((visina, sirina, 3), dtype=np.uint8)
    
    oznake = np.zeros((visina, sirina), dtype=np.int32)
    toleranca = 1

    for i in range(iteracije):
        if dimenzija == 3:
            # 1. Označimo vsak piksel s številko centra
            for y in range(visina):
                for x in range(sirina):
                    piksel = np.array([slika[y,x][0], slika[y,x][1], slika[y,x][2]], dtype=np.float64)

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
                            pikseli.append([slika[y,x][0], slika[y,x][1], slika[y,x][2]])

                # Izračunamo povprečje
                if len(pikseli) > 0:
                    povprecje = np.mean(pikseli, axis=0)
                    novi_centri.append(povprecje)
                else:
                    novi_centri.append(centri[i])

            # 3. Preverimo, ali so se centri spremenili
            premiki = []
            for i in range(k):
                premik = evklidska_razdalja(centri[i], novi_centri[i], dimenzija)
                premiki.append(premik)

            # Če so se centri premaknili manj kot toleranca, končamo
            if all(premik < toleranca for premik in premiki):
                print(f"Končali po {i} iteracijah.")
                break
            else:
                # Posodobimo centre
                centri = novi_centri

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

            # 3. Preverimo, ali so se centri spremenili
            premiki = []
            for i in range(k):
                premik = evklidska_razdalja(centri[i], novi_centri[i], dimenzija)
                premiki.append(premik)

            # Če so se centri premaknili manj kot toleranca, končamo
            if all(premik < toleranca for premik in premiki):
                print(f"Končali po {i} iteracijah.")
                break
            else:
                # Posodobimo centre
                centri = novi_centri

    # 4. Ustvarimo segmentirano sliko
    for y in range(visina):
        for x in range(sirina):
            if dimenzija == 3:
                segmentirana_slika[y, x] = centri[oznake[y, x]][:3]
            elif dimenzija == 5:
                segmentirana_slika[y, x] = centri[oznake[y, x]][2:5]

    return segmentirana_slika


def meanshift(slika, velikost_okna=30, dimenzija=5, iteracije=5):
    '''Izvede segmentacijo slike z uporabo metode mean-shift.'''
    visina, sirina = slika.shape[:2]
    točke = np.zeros((visina, sirina, dimenzija), dtype=np.float32)

    # Zbiranje podatkov za vsak piksel v sliki
    for y in range(visina):
        for x in range(sirina):
            barva = slika[y, x]
            if dimenzija == 3:
                točke[y, x] = [barva[0], barva[1], barva[2]]
            elif dimenzija == 5:
                točke[y, x] = [x, y, barva[0], barva[1], barva[2]]
    
    konvergirane_tocke = np.zeros((visina, sirina, dimenzija), dtype=np.float32)

    # Proces za vsako točko v sliki
    for y in range(visina):
        for x in range(sirina):
            trenutna_tocka = točke[y, x]

            for _ in range(iteracije):
                uteži_vsote = 0.0
                uteženi_sestevek = np.zeros(dimenzija, dtype=np.float32)

                for j in range(visina):
                    for i in range(sirina):
                        točka = točke[j, i]
                        razdalja = evklidska_razdalja(trenutna_tocka, točka, dimenzija)
                        utež = gaussovo_jedro(razdalja, velikost_okna)
                        uteži_vsote += utež
                        uteženi_sestevek += točka * utež

                if uteži_vsote == 0:
                    break

                nova_tocka = uteženi_sestevek / uteži_vsote
                razdalja = evklidska_razdalja(trenutna_tocka, nova_tocka, dimenzija)

                if razdalja < 0.1:
                    break

                trenutna_tocka = nova_tocka

            konvergirane_tocke[y, x] = trenutna_tocka

     # Združevanje konvergiranih točk v centre
    min_cd = 200
    centri = []
    oznake = np.zeros((visina, sirina), dtype=np.int32)

    for y in range(visina):
        for x in range(sirina):
            tocka = konvergirane_tocke[y, x]
            dodeljen = False                
            for j, center in enumerate(centri):
                if evklidska_razdalja(tocka, center, dimenzija) < min_cd:
                    oznake[y, x] = j 
                    dodeljen = True
                    break

            if not dodeljen:
                centri.append(tocka.copy())
                oznake[y, x] = len(centri) - 1 

    # Ustvarimo segmentirano sliko
    segmentirana_slika = np.zeros_like(slika, dtype=np.uint8)

    for y in range(visina):
        for x in range(sirina):
            segment = oznake[y, x]

            if dimenzija == 3:
                barva_segmenta = centri[segment][:3]
            elif dimenzija == 5:
                barva_segmenta = centri[segment][2:5]

            segmentirana_slika[y, x] = barva_segmenta

    return segmentirana_slika

            
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
                center = np.array([barva[0], barva[1], barva[2]])
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
                    center = np.array([barva[0], barva[1], barva[2]])
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

    slika = cv.imread(".utils/zelenjava_mega_small.jpg")
    slika = cv.resize(slika, (50,50))
    if slika is None:
        print("Napaka: Slika ni bila naložena.")
        exit()
    else:
        print("Slika uspešno naložena:", slika.shape)

    seg_slika = meanshift(slika)

    cv.imshow("seg slika", seg_slika)
    cv.waitKey(0)
    cv.destroyAllWindows()