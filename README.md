# SZTE-snooker
Szegedi Tudományegyetem ProgInfo MSc - Képfeldolgozás haladóknak gyak.

# Előfeltételek
- Python verzió: [3.11.5]
- Modulok:
  - **matplotlib**
    ```
    pip install matplotlib
    ```
  - **cv2**
    ```
    pip install opencv-python
    ```
  - **numpy**
    ```
    pip install numpy
    ```

# Futtatás
  - *snooker* mappában:
    ```
    py main.py
    ```

# Használat

 - Kell választani egy bementi videót, valamint egy kimeneti foldert
 - A videos folderban van egy snooker_video.mp4, amire teszteltünk
 - Ha megnyomod a start process gombot elkezdődik a felismerés egy új ablakba
 - Elhatárolja az asztalt, valamint kijelöli a különböző golyókat
 - Megjelenik minden nem fehér golyóra egy segéd egyenes, amely megmutatja, hogy teli találat esetén merre menne az adott színes golyó
 - Ha egy golyó lemegy egyik lyukon, akkor megmondja, hogy az hány pontot ért
 - Amikor a feliserés befejeződik, a generált videót lementi a kimeneti folderba `output_video.mp4` néven