# Readme für die Zirkulation Tools
für die Auswertung muss im Case ein *p*ost *P*rocessing Ordner *pP_script* erstellt werden. In diesem Ordner müssen nun die entsprechenden Files hinzugefügt werden. Beispiel: 
pP_script/direction_of_vortex.py
pP_script/rot_zirkulation.py
pP_script/rotate_gamma.sc

Die Tools müssen aus dem pP_script Ordner mit *./* gestartet werden. Unter Umständen muss vorher noch chmod +x angewandt werden um die Datei ausführbar zu machen. 
## Was kann das Tool?
Das Tool kann über Lambda2 (max), Druck(min) oder Vorticity(max) das Wirbelzentrum bestimmen, über die Vorticity kann gleichzeitig auch die Wirbelachse berechnet werden. Bei gegebener Wirbelachse und Wirbelzentrum berechnet das Tool die Zirkulation, bei Druck und Vorticity auch einen Wirbelkerndurchmesser.

## Modi

### Vorticity
In direction_of_vortex wird die die maximale Voriticity bestimmt und ein Vektor kollinear zum Wirbelkern bestimmt. 

Um die Genauigkeit zu erhöhen, kann die Vorticity über eine Bereich gemittelt werden. In der Hauptfunktion lässt sich mit dem Faktoren *cellsize* und *cellcount* ein Radius berechnen. Mit dem Ort der maximalen Voritcity und dem Radius ergibt sich eine Kugel. Die Schnittmenge von Kugel UND gesampelten Werten ergibt die Menge an Werten über die die Voricity gemittelt wird. Ziel ist der Ausgleich von lokalen Schwankungen. Dieses Feature ist nur für die Voriticty sinnvoll und verfügbar.

Auf Basis der maximalen Vorticity und des Vektors kollinear zum Wirbelkern, c, werden nun die Vektoren a und b bestimmt, die alle orthogonal zueinander stehen. 


Mithilfe der Vektoren a und b sowie der *real_length* werden die Eckpunkte des zu sampelnden Fensters bestimmt.

Mit der Funktion *sampledict* werden die zu Sampelnden Linien in eine Datei niedergeschrieben, die im nächsten Schritt von rotate_gamma.sc -> Foam aufgerufen wird. 


### Druck
Für die auswertung über den Druck muss entweder die Wirbelachse (*c_i*) oder die Vektoren, die das Rechteck aufspannen (*a_i*,*b_i*), definiert werden. Ist die Wirbelachse gegeben werden *a_i*,*b_i* analog zur Vorticity berechnet. 

Als Wirbelzentrum werden die Koordinaten des Druckminimum genutzt.

Mithilfe der Vektoren a und b sowie der *real_length* werden die Eckpunkte des zu sampelnden Fensters bestimmt.

Mit der Funktion *sampledict* werden die zu Sampelnden Linien in eine Datei niedergeschrieben, die im nächsten Schritt von rotate_gamma.sc -> Foam aufgerufen wird. 

### Manuell

Es wird ein Wirbelzentrum benötigt. Analog zum Druck kann das Rechteck über die definition einer Wirbelachse oder über die definition der Rechtecktvektoren bestimmt werden




### Bestimmung auf Basis des Voritcitymaximums
Bestimmung der Zirkulation auf Basis eines Vorticitymaximums. Der Bereich, in dem der Wirbel gesucht werden soll kann durch Gebietsdefinition eingeschränkt werden. Es ist daher auch möglich in Ebenen zu suchen, die die Grenzschicht schneiden. Die Wirbelachse, sowie die zum Aufspannen des Rechtecks benötigten Vektoren, werden berechnet. Die Orientierunt der Seiten des Rechtecks im Raum ist dabei beliebig.

### Bestimmung der Zirkulation auf Basis von definierten Vektoren, Wirbelzentrum und Fenstergröße.

Selbsterklärend, oder?



####################################################################################################################
# Die Programmteile
## rotate_gamma.sc
Anwendung: zunächst muss die Datei *sampleDict_plane_vorticity_file* oder sampleDict_plane_pressure_file* in /system kopiert und in *sampleDict_plane_vorticity* oder *sampleDict_plane_pressure* umbenannt werden. In der Datei selber muss nun eine den Wirbelkern schneidende Ebene definiert (normalVector und basePoint) werden. Die Ebene ist so zu wählen, dass der wirbel möglichst orthogonal geschnitten wird.

Schneidet die Ebene zusätzlich eine Grenzschicht, müssen in ### direction_of_vortex.py die Variablen xup, xlow usw so gewählt werden, dass sie den Wirbel Beinhalten, die Grenzschicht jedoch ausschließen. 

Das Tool wählt in dem Ordner /postProcessing immer den aktuellsten eintrag von *sampleDict_plane_pressure* und *sampleDict_plane_vorticity* aus. somit wird in ### rotate_gamma.sc definiert, ob die Auswertung über den Druck oder die Vorticity definiert wird. Ist weder *sampleDict_plane_pressure* noch *sampleDict_plane_vorticity* vorhanden, erfolgt die Auswertung manuell, es müssen also Vektoren, Wirbelzentrum und Fenstergröße definiert werden


## direction_of_vortex.py
### Parameter

*xz*, *yz*, *zz*, *rad* (float in m, not null) Einschränken des Suchbereichs. Schneidet die definierte Ebene eine Grenzschicht oder möchte man die Suche nach einem Mini/maxima einschränken, kann dies über die Definition eines Punktes und einem Radius abgehend von diesem Punkt geschehen. Soll keine Einschränkung erfolgen müssen diese Parameter entsprechend hoch gewählt werden.

*real_length* (float in m, not null) Größe des Rechtecks, dass später um den Wirbelkern gelegt wird. 
*cellsize*(float in m), *cellcount*(int(float möglich)), Mittelung der Vorticity. Alle Punkte die innerhalb des *radius*liegen, werden zur Mittlung genutzt. Der *radius*(berechnet sich normalerweise, kann manuell definiert werden)  kann direkt definiert werden, oder aber über das Produkt aus *cellsize* (im Wirbelkern) und der Anzahl der Zellen (*cellcount*) in einer Richtung, über die gemittelt werden soll.

*x_c*, *y_c*, z_c*(float in m) manuelle definition eines Wirbelzentrums, funktioniert nur im Manuellen Modus(-> keinerlei "sampleDichts[..]" im postProcessing Ordner) 

*c_i*(float in m) manuelle definition einer Wirbelachse. Auf dieser Basis können auch die Rechteckvektoren berechnet werden. Wenn nicht definiert _muss_ der Vorticity modus genutzt werden. 
*a_i*, *b_i* Rechteckvektoren, falls nicht definiert werden diese über die Wirbelachse berechnet. 

### Funktionen innerhalb des Programms

**def length_norm(x, y, z, length):** normt den Vektor xyz auf die Länge length

**def Einlesen1():** ließt die Daten ein. Ordnerstruktur muss '../postProcessing/sampleDict_plane_XX/timestep/' sein, XX steht für pressure/lambda/vorticity.
Die Funktion gibt *array* und *dummy* wieder, array beinhaltet die eingelesenen Daten, *dummy* nimmt "n" für den manuellen Modus, "v" für Vorticity, "p" für Druck und "l" für Lambda2 an. Wichtig für die weiter Datenverarbeitung.

**def find_max(array, dummy, xz, yz, zz, rad):** Findet das Maximum/Minimum in einem Bereich der durch den Punkt(xz, yz, zz) und dem Radius (rad) definiert ist. Das Minimum des Drucks und das Maximum der Wirbelstärke werden in eine Datei geschrieben, auf ihrer Basis wird im zweiten Teil der Wirbelkerndurchmesser berechnet. 

**def avg_vorticity(array, max_line, radius ):** Mittelt die Voritcity im Radius (radius) um ihr Maximum (max_line), die Wirbelachse kann so genauer bestimmt werden. Nur für Wirbelstärkenmodus verfügbar.

**def sampledict (punkte):** schreibt die zu sampelnden Linien raus, auf deren Basis später die Zirkulation berechnet werden soll in eine für openFoam zu lesende Datei. 

**def Rotationsmatrix(c_1, c_2, c_3):** Bestimmt einen Vektor a, der Senkrecht auf Vektor c (Wirbelachse) steht. Vektor b ergibt sich aus Vektor a, der um 90 Grad um Vektor c gedreht wurde. siehe https://de.wikipedia.org/wiki/Drehmatrix



## rot_zirkulation.py
Diese Programm liest die gesampelten Linien ein, berechnet die Zirkulation und 
Hier werden die gesampelten Linien eingelesen und integriert (Trapezverfahren). Mithilfe der Zirkulation wird im Druck oder Wirbelstärkenmodus auch ein Wirbeldurchmesser ermittelt. Das Ergebniss wird  _nur_ Terminal ausgegeben.
### Parameter
*rho* (float in kg/m³, not null) Wird für die Berechnung des Wirbelkerndurchmessers basierend auf Druck benötigt.
### Funktionen
**def Einlesen():** Liest die 4 Liniensets aus *sampleDicht_python_plotlines* ein. Unelegant aber es funktioniert sehr gut. 
**def integration(data_array):** Entlang der Linien wird die kollinear Geschwindigkeitskomponente aufintegriert. Dieser Vorgang wird für jede Linie wiederholt, die Ergebnisse aufsummiert. 

### Bestimmung des viskosen Radius / Wirbelkerndurchmesser nach Burgers
p_min = Druckminimum 

p_inf = umgebungsdruck

\rho = dichte

\Gamma = Zirkulation

a = Radius des Wirbels

\frac{p_{min}-p_{\infty}}{\rho} = -0.871 { \frac{\Gamma}{2 \pi a} }^2

 umgestellt zu 
 
 a = \frac{\Gamma}{2 \pi} [ \frac{p_min - p_inf}{\rho *-0.871}]^-0.5
 
 Die Bestimmung des Wirbelkerndurchmesser ist nur Verfügbar, wenn der "Druckmodus" genutzt und eine Wirbelachse definiert ist.

## Zirkulationsauswertung bei beliebiger Wirbelorientierung
### Files:direction_of_vortex.py
### Files:rot_zirkulation.py
### Files:rotate_gamma.sc
