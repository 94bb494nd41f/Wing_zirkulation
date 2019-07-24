# Readme für die Zirkulation Tools
Die Anleitung kann über Gitprint als .pdf gedruckt werden. 

Für die Auswertung muss im Case ein _p_ost _P_rocessing_ der Ordner _pP_script_ erstellt werden. In diesem Ordner müssen nun die 

Files hinzugefügt werden: 

pP_script/direction_of_vortex.py

pP_script/rot_zirkulation.py

pP_script/rotate_gamma.sc

Das Tool muss aus dem pP_script Ordner mit _./_ gestartet werden. Unter Umständen muss vorher noch chmod +x angewandt werden um die Datei ausführbar zu machen. 

Bei Unklarheiten empfiehlt sich auf jeden Fall ein Blick in den Code.

## Was kann das Tool?
Das Tool kann über Lambda2 (max), Druck (min) oder Vorticity (max) das Wirbelzentrum bestimmen. Über die Vorticity kann gleichzeitig auch die Wirbelachse berechnet werden. Bei gegebener Wirbelachse und Wirbelzentrum berechnet das Tool die Zirkulation, bei Druck und Vorticity auch einen Wirbelkerndurchmesser.

## Modi

### Vorticity
In _direction_of_vortex_ wird die die maximale Voriticity bestimmt und ein Vektor kollinear zum Wirbelkern bestimmt.
 
Um die Genauigkeit zu erhöhen, kann die Vorticity über einen Bereich gemittelt werden. In der Hauptfunktion lässt 
sich mit den Faktoren _cellsize_ und _cellcount_ ein Radius berechnen. Mit dem Ort der maximalen Voritcity und 
dem Radius ergibt sich eine Kugel. Die Schnittmenge von Kugel UND gesampelter Ebene 
ergibt die Menge an Werten, über die die Voricity gemittelt wird. Ziel ist der Ausgleich von lokalen Schwankungen.
 Dieses Feature ist nur für die Voriticty sinnvoll und verfügbar.

Auf Basis der maximalen Vorticity und des Vektors kollinear zum Wirbelkern, _c_, werden nun die Vektoren 
_a_ und _b_ bestimmt, die alle orthogonal zueinander stehen. 


Mithilfe der Vektoren _a_ und _b_ sowie der _real_length_ werden die Eckpunkte des zu sampelnden Fensters bestimmt.

Mit der Funktion _sampledict_ werden die zu sampelnden Linien in eine Datei niedergeschrieben, 
die im nächsten Schritt von _rotate_gamma.sc_ -> _Foam_ aufgerufen wird. 


### Druck
Für die Auswertung über den Druck müssen entweder die Wirbelachse (_c_i_) oder die Vektoren, die das Rechteck aufspannen (_a_i_, _b_i_), definiert werden. Ist die Wirbelachse gegeben, werden _a_i_, _b_i_ analog zur Vorticity berechnet. 

Als Wirbelzentrum werden die Koordinaten des Druckminimums genutzt.

Mithilfe der Vektoren _a_ und _b_ sowie der _real_length_ werden die Eckpunkte des zu sampelnden Fensters bestimmt.

Mit der Funktion _sampledict_ werden die zu sampelnden Linien in eine Datei niedergeschrieben, die im nächsten Schritt von rotate_gamma.sc -> Foam aufgerufen wird. 

### Manuell

Es wird ein Wirbelzentrum benötigt. Analog zum Druck kann das Rechteck über die Definition einer Wirbelachse oder über die Definition der Rechtecktvektoren bestimmt werden



####################################################################################################################
# Die Programmteile
## rotate_gamma.sc
===================================
Anwendung: zunächst muss die Datei _sampleDict_plane_vorticity_file_ oder _sampleDict_plane_pressure_file_ in 
/system kopiert und in _sampleDict_plane_vorticity_ oder _sampleDict_plane_pressure_ umbenannt werden. 
In der Datei selber muss nun eine, den Wirbelkern schneidende, Ebene definiert werden (normalVector und basePoint).
 Die Ebene ist so zu wählen, dass der wirbel möglichst orthogonal geschnitten wird.

Schneidet die Ebene zusätzlich eine Grenzschicht, müssen in _direction_of_vortex.py_
die Variablen _xup_, _xlow_ usw so gewählt werden, dass sie den Wirbel beinhalten, 
die Grenzschicht jedoch ausschließen. 

Das Tool wählt in dem Ordner /postProcessing immer den aktuellsten Eintrag 
von _sampleDict_plane_XX_ aus. Somit wird in _rotate_gamma.sc_ definiert, 
ob die Auswertung über den Druck oder die Vorticity definiert wird. 

Soll die Auswertung manuell erfolgen, muss der Ordner _postProcessing_ 
frei von Ordnern mit dem Namen _sampleDict_ sein. Für die manuelle Auswertung müssen in _direction_of_vortex.py_ 
in _Parameter_ die entsprechenden Definitionen vorhanden sein.

## direction_of_vortex.py
=======================
### Parameter

_xz_, _yz_, _zz_, _rad_ (float in m) Einschränken des Suchbereichs. 
Schneidet die definierte Ebene eine Grenzschicht oder möchte man die Suche nach einem Minimum/Maximum einschränken, 
kann dies über die Definition eines Punktes und eines Radius abgehend von diesem Punkt geschehen. 
Soll keine Einschränkung erfolgen, müssen diese Parameter entsprechend hoch gewählt oder nicht definiert werden. 

_real_length_ (float in m, not null) Größe des Rechtecks, das später um den Wirbelkern gelegt wird. 

_cellsize_ (float in m), _cellcount_ (int(float möglich)), Mittelung der Vorticity. 
Alle Punkte die innerhalb des _radius_ liegen, werden zur Mittlung genutzt. 
Der _radius_(wird berechnet, kann manuell definiert werden)  kann direkt definiert werden, 
oder aber über das Produkt aus _cellsize_ (im Wirbelkern) und 
der Anzahl der Zellen (_cellcount_) berechnet werden. Alle Werte, die sich in der Kugel um den Maximalen Wert befinden, werden zur Mittelung genutzt.

_x_c_, _y_c_, _z_c_ (float in m) manuelle Definition eines Wirbelzentrums, 
funktioniert nur im manuellen Modus(-> keinerlei "sampleDicts[..]" im postProcessing Ordner).

_c_i_ (float in m) manuelle Definition einer Wirbelachse. Auf dieser Basis können auch die Rechteckvektoren 
berechnet werden. Wenn nicht definiert, _muss_ der Vorticitymodus genutzt werden. 

_a_i_, _b_i_ Rechteckvektoren, falls nicht definiert, werden diese über die Wirbelachse berechnet. 

### Funktionen innerhalb des Programms

__def length_norm(x, y, z, length):__ normt den Vektor xyz auf die Länge _length_

__def Einlesen1():__ ließt die Daten ein. Ordnerstruktur muss '../postProcessing/sampleDict_plane_XX/timestep/' 
 sein, XX steht für pressure/lambda/vorticity.
Die Funktion gibt _array_ und _dummy_ wieder. _array_ beinhaltet die eingelesenen Daten, 
_dummy_ nimmt "n" für den manuellen Modus, "v" für Vorticity, "p" für Druck und "l" für Lambda2 an. 
Wichtig für die weitere Datenverarbeitung.

__def find_max(array, dummy, xz, yz, zz, rad):__ Findet das Maximum/Minimum in einem Bereich der durch den 
Punkt (_xz_, _yz_, _zz_) und den Radius (_rad_) definiert ist. Das Minimum des Drucks und das Maximum der 
Wirbelstärke werden in eine Datei geschrieben. Auf ihrer Basis wird im zweiten Teil der Wirbelkerndurchmesser 
berechnet. 

__def avg_vorticity(array, max_line, radius ):__ Mittelt die Voritcity im Radius (_radius_) um ihr Maximum 
(_max_line_, Tupel mit x|y|z|...). Die Wirbelachse kann so genauer bestimmt werden. Nur für Wirbelstärkenmodus verfügbar.

__def sampledict (punkte):__ schreibt die zu sampelnden Linien raus, auf deren Basis später die 
Zirkulation berechnet werden soll, in eine für openFoam zu lesende Datei. 

__def Rotationsmatrix(c_1, c_2, c_3):__ Bestimmt einen Vektor _a_, der senkrecht auf Vektor _c_ 
(Wirbelachse) steht. Vektor _b_ ergibt sich aus Vektor _a_, der um 90 Grad um Vektor _c_ gedreht wurde. siehe https://de.wikipedia.org/wiki/Drehmatrix


## rot_zirkulation.py
Diese Programm liest die gesampelten Linien ein und berechnet die Zirkulation. 
Mithilfe der Zirkulation wird im Druck- oder Wirbelstärkenmodus auch ein Wirbeldurchmesser ermittelt. 
Das Ergebniss wird  _nur_ im Terminal ausgegeben.
### Parameter
_rho_ (float in kg/m³, not null) Wird für die Berechnung des Wirbelkerndurchmessers basierend auf dem Druck benötigt.
### Funktionen
__def Einlesen():__ liest die 4 Liniensets aus _sampleDicht_python_plotlines_ ein. Unelegant funktioniert aber sehr gut. 

__def integration(data_array):__ Entlang der Linien wird die kollineare Geschwindigkeitskomponente aufintegriert. Dieser Vorgang wird für jede Linie wiederholt, die Ergebnisse werden aufsummiert. 

### Bestimmung des viskosen Radius / Wirbelkerndurchmesser nach Burgers
p_min = Druckminimum 

p_inf = Umgebungsdruck

\rho = Dichte

\Gamma = Zirkulation

a = Radius des Wirbels

\frac{p_{min}-p_{\infty}}{\rho} = -0.871 { \frac{\Gamma}{2 \pi a} }^2

 umgestellt zu 
 
 a = \frac{\Gamma}{2 \pi} [ \frac{p_min - p_inf}{\rho _-0.871}]^-0.5
 
 Die Bestimmung des Wirbelkerndurchmesser ist nur verfügbar, wenn der "Druckmodus" genutzt und eine Wirbelachse definiert ist.
### Bestimmung des Wirbelkerndurchemsser nach Dag Feder
Bei Fragen an Dag Feder wenden. Nur im "Vorticitymodus" verfügbar.

a = sqrt(2.513 Gamma / (2 pi vorticity_0) )
