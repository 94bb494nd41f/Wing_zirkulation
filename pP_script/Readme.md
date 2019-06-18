# Readme für die Zirkulation Tools
für die Auswertung muss im Case ein *p*ost *P*rocessing Ordner *pP_script* erstellt werden. In diesem Ordner müssen nun die entsprechenden Files hinzugefügt werden. Beispiel: 
pP_script/direction_of_vortex.py
pP_script/rot_zirkulation.py
pP_script/rotate_gamma.sc
# To Do


Die Tools müssen aus dem pP_script Ordner mit *./* gestartet werden. Unter Umständen muss vorher noch chmod +x angewandt werden um die Datei ausführbar zu machen. 
## was kann das Tool?
### Bestimmung auf Basis des Druckminimums
Bestimmung der Zirkulation auf Basis eines Druckminimums. Der Bereich, in dem der Wirbel gesucht werden soll kann durch Gebietsdefinition eingeschränkt werden. Es ist daher auch möglich in Ebenen zu suchen, die die Grenzschicht schneiden. 

Bei dieser Variante muss eine Wirbelachse definiert werden. Aus der Wirbelachse werden die zum Aufspannen des Rechtecks benötigten Vektoren berechnet. Die Orientierunt der Seiten des Rechtecks im Raum ist dabei beliebig. Das Gleichungssystem zur bestimmtung der "Rechteck-Vektoren" hat drei Freiheitsgrade, die willkürlich beschränkt wurden. Forderung der Art "Rechteckseite A parallel zu Y-Achse" können daher implementiert werden.

Es können auch die Vektoren definiert werden, die das Rechteck aufspannen. Eine Wirbelachse wird hierbei nicht benötigt.

Das Rechteck wird um das Druckminimum aufgespannt.


### Bestimmung auf Basis des Voritcitymaximums
Bestimmung der Zirkulation auf Basis eines Vorticitymaximums. Der Bereich, in dem der Wirbel gesucht werden soll kann durch Gebietsdefinition eingeschränkt werden. Es ist daher auch möglich in Ebenen zu suchen, die die Grenzschicht schneiden. Die Wirbelachse, sowie die zum Aufspannen des Rechtecks benötigten Vektoren, werden berechnet. Die Orientierunt der Seiten des Rechtecks im Raum ist dabei beliebig. Das Gleichungssystem zur bestimmtung der "Rechteck-Vektoren" hat drei Freiheitsgrade, die willkürlich beschränkt wurden. Forderung der Art "Rechteckseite A parallel zu Y-Achse" können daher implementiert werden.

### Bestimmung der Zirkulation auf Basis von definierten Vektoren, Wirbelzentrum und Fenstergröße.

## Zirkulationsauswertung bei beliebiger Wirbelorientierung
### Files:direction_of_vortex.py
### Files:rot_zirkulation.py
### Files:rotate_gamma.sc


####################################################################################################################
### rotate_gamma.sc
Anwendung: zunächst muss die Datei *sampleDict_plane_vorticity_file* oder sampleDict_plane_pressure_file* in /system kopiert und in *sampleDict_plane_vorticity* oder *sampleDict_plane_pressure* umbenannt werden. In der Datei selber muss nun eine den Wirbelkern schneidende Ebene definiert (normalVector und basePoint) werden. Die Ebene ist so zu wählen, dass der wirbel möglichst orthogonal geschnitten wird.

Schneidet die Ebene zusätzlich eine Grenzschicht, müssen in ### direction_of_vortex.py die Variablen xup, xlow usw so gewählt werden, dass sie den Wirbel Beinhalten, die Grenzschicht jedoch ausschließen. 

Das Tool wählt in dem Ordner /postProcessing immer den aktuellsten eintrag von *sampleDict_plane_pressure* und *sampleDict_plane_vorticity* aus. somit wird in ### rotate_gamma.sc definiert, ob die Auswertung über den Druck oder die Vorticity definiert wird. Ist weder *sampleDict_plane_pressure* noch *sampleDict_plane_vorticity* vorhanden, erfolgt die Auswertung manuell, es müssen also Vektoren, Wirbelzentrum und Fenstergröße definiert werden


## direction_of_vortex.py
Schneidet die definierte Ebene eine Grenzschicht oder möchte man die Suche nach einem Mini/maxima einschränken, kann dies über die Parameter *xup*, *xlow* etc geschehen. Soll keine Einschränkung erfolgen müssen diese Parameter entsprechend hoch gewählt werden.
Folgende Parameter können editiert werden:
real_length = 0.4  # absolute groeße des Fensters, ist quadratisch

    cellsize = 0.0082  # cellsize in core vortex

    cellcount = 20      # calculates with the cellsize to the radius, which is used to average around the maximum

    # Grenzen in denen Nach Maxi/minima gesucht werden soll
    xup =10000
    xlow =-10000

    yup = 10000
    ylow = -10000

    zup = 10000
    zlow = -10000

    radius = cellcount * cellsize
    # Manuelle Definition des Zentrums
    #x_c
    #y_c
    #z_c

    #definition der Vektoren
    #Richtung des Wirbels:
    c_1=3
    c_2=4
    c_3=5
    
    # #Vektor fuer Rechteck in Richtung 1
    # a_1=9
    # a_2=9
    # a_3=9
    
    # # Vektor fuer Rechteck in Richtung 2
    # b_1=9
    # b_2=9
    # b_3=9

### Vorticity
In direction_of_vortex wird die die maximale Voriticity bestimmt und ein Vektor kollinear zum Wirbelkern bestimmt. 

Um die Genauigkeit zu erhöhen, kann die Vorticity über eine Bereich gemittelt werden. In der Hauptfunktion lässt sich mit dem Faktoren *cellsize* und *cellcount* ein Radius berechnen. Mit dem Ort der maximalen Voritcity und dem Radius ergibt sich eine Kugel. Die Schnittmenge von Kugel UND gesampelten Werten ergibt die Menge an Werten über die die Voricity gemittelt wird. Ziel ist der Ausgleich von lokalen Schwankungen. Dieses Feature ist nur für die Voriticty sinnvoll und verfügbar.

Auf Basis der maximalen Vorticity und des Vektors kollinear zum Wirbelkern, a, werden nun die Vektoren b und c bestimmt, die alle orthogonal zueinander stehen. 

Mithilfe der Vektoren b und c sowie der *real_length*, zu finden direkt am Anfang des Programms (Programm =! Funktion), werden die Eckpunkte des zu Sampelnden Fensters bestimmt.

Da die Vektoren b und c einen je einen Freiheitsgrad haben, kann nicht gewährleistet sein, dass die Linien des Rechtecks parallel zu einer Wand o.ä. Verlaufen. Der Einfluss auf das Ergebnis sollte aber vernachlässigbar sein. 

Mit der Funktion *sampledict* werden die zu Sampelnden Linien in eine Datei niedergeschrieben, die im nächsten Schritt von rotate_gamma.sc -> Foam aufgerufen wird. 


### Druck
Für die auswertung über den Druck muss entweder die Wirbelachse (*c_i*) oder die Vektoren, die das Rechteck aufspannen (*a_i*,*b_i*), definiert werden. Ist die Wirbelachse gegeben werden *a_i*,*b_i* analog zur Vorticity berechnet. 

Als Wirbelzentrum werden die Koordinaten des Druckminimum genutzt.

### Manuell

Es wird ein Wirbelzentrum benötigt. Analog zum Druck kann das Rechteck über die definition einer Wirbelachse oder über die definition der Rechtecktvektoren bestimmt werden. 

### rot_zirkulation.py
Hier werden die gesampelten Linien eingelesen und integriert (Trapezverfahren). Das Ergebniss wird im ### nur Terminal ausgegeben.
