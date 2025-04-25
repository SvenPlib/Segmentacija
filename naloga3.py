import cv2 as cv

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