# uni-teamarbeit-laserscanner
catkin_make baut alle Projekte
setub.bash in /devel muss zu jedem ersten Start ausgeführt werden

## Für Git Commit
```
git add .
git status # Sollte hinzugefügte Dateien grün anzeigen
git commit -m "Commitmessage" # -m optional, dann startet Editor, in welchen man die Commitmessage eingeben kann
git push
```


## rosbag wiedergabe Befehle (jeweils eigene Terminals)
```
roscore
rostopic echo /Joystick
rosbag play "name"
```
Zum Starten folgende Befehle in jeweils eigene Terminals:
```
roscore
rosrun hokuyo_node hokuyo_node
rosrun beginner_tutorials subscriber
```

Algorithmus:
analyse_kick liefert x y Koordinaten für Ball während Flug
 * Berechnet für jeden Punkt Initialgeschw.
 * Berechnet Median(Geschwindigkeiten)
 * Berechnet entsprechenden Abschusswinkel (wie algorithmisch?)
    * Bisher durch ausprobiern (Augenmaß) in Exel
Alles in Abhängigkeit von Schussstärke (Ladezeit)
