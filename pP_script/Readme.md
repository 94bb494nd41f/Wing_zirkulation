# Readme für die Zirkulation Tools
für die Auswertung muss im Case ein *p*ost *P*rocessing Ordner *pP_script* erstellt werden. In diesem Ordner müssen nun die entsprechenden Files hinzugefügt werden. Beispiel: 
pP_script/direction_of_vortex.py
pP_script/rot_zirkulation.py
pP_script/rotate_gamma.sc

Die Tools müssen aus dem pP_script Ordner mit *./* gestartet werden. Unter Umständen muss vorher noch chmod +x angewandt werden


## Zirkulationsauswertung bei Beliebiger Wirbelorientierung
### Files:direction_of_vortex.py
### Files:rot_zirkulation.py
### Files:rotate_gamma.sc

Anwendung: zunächst muss die Datei *sampleDict_plane_vorticity_file* in /system kopiert und in *sampleDict_plane_vorticity* umbenannt werden. In der Datei selber muss nun eine den Wirbelkern schneidende Ebene definiert (normalVector und basePoint) werden.
Für das Tool ist es essentiell, dass die maximale Vorticity im Wirbelkern zu finden ist, ein schneiden von Grenzschichten sollte daher unbedingt vermieden werden. 

### direction_of_vortex.py
In direction_of_vortex wird die die maximale Voriticity bestimmt und ein Vektor kollinear zum Wirbelkern bestimmt. 

Um die Genauigkeit zu erhöhen, kann die Vorticity über eine Bereich gemittelt werden. In der Hauptfunktion lässt sich mit dem Faktor *bandbreite* die Größe der auf die gesampelte Ebende projezierte Kugel bestimmen. Code beispiel:
>    if sig_x == -1:
>        x_up = max_line.item(0) * (1 - bandbreite)
>        x_low = max_line.item(0) * (1 + bandbreite)


Auf Basis der maximalen Vorticity und des Vektors kollinear zum Wirbelkern, a, werden nun die Vektoren b und c bestimmt, die alle orthogonal zueinander stehen. 

Mithilfe der Vektoren b und c sowie der *real_length*, zu finden direkt am Anfang des Programms (Programm =! Funktion), werden die Eckpunkte des zu Sampelnden Fensters bestimmt.

Da die Vektoren b und c einen je einen Freiheitsgrad haben, kann nicht gewährleistet sein, dass die Linien des Rechtecks parallel zu einer Wand o.ä. Verlaufen. Der Einfluss auf das Ergebnis sollte aber vernachlässigbar sein. 

Mit der Funktion *sampledict* werden die zu Sampelnden Linien in eine Datei niedergeschrieben, die im nächsten Schritt von rotate_gamma.sc -> Foam aufgerufen wird. 

### rot_zirkulation.py
Hier werden die gesampelten Linien eingelesen und integriert (Trapezverfahren). Das Ergebniss wird im Terminal ausgegeben.
