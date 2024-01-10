# Projektname
Chess

## Ziele und Projektumfang
Das Hauptziel war, ein funktionstüchtiges Schachprogramm nachzubauen, das sich an alle offiziellen Regeln hält.
Da mich Schach schon lange interessiert und ich meine Kenntnisse in der Informatik verbessern wollte habe ich mich dafür entschieden das Spiel von Grund auf nachzubauen um ebenfalls ein besseres Verständnis der Schachmechanik zu bekommen.

## Technologien und Werkzeuge
Das Projekt wurde in Pycharm geschrieben, benutzt und kennengelernt habe ich bisher PyQt6, pytest, git, PyInstaller und PlantUML

## Funktionalitäten und Features
Mein Projekt wurde in drei Teile aufgebaut:

- **Model**: 
  - `chessboard`: Das chessboard beinhaltet den aktuellen Stand des Spiels und besitzt die verschiedenen Spielfiguren.
  - `player`: Enthält Informationen über eigene Figuren, deren möglichen Züge und den aktuellen Schachstand.
  - `chesspieces`: Diese haben Informationen über ihr mögliches Bewegungsmuster.

- **View**:
  - `ui_chessboard`: Ist dem chessboard model nachempfunden und enthält für alle Felder des Schachbretts jeweils ein QLabel, das passend dunkel oder hell gefärbt ist. Ebenso zeigt es die Koordinaten an den Seitenrändern, also 1-8 und A-H, an.
  - `clickable_label`: Eine überschriebene QLabel Klasse, deren Drag-and-Drop-Vorgang sowie das Hinzufügen von SVG-Bildern bis hin zu dem Animieren des Labels selbst überarbeitet wurde.

- **Controller**: 
  - `check_management`:
    - `check_resolver`: Berechnet die möglichen Verteidigungszüge deiner Figuren, sobald du im Schach stehst.
    - `move_validator_king_in_check`: Berechnet die möglichen Züge des Königs, wenn er im Schach steht.
    - `check_handler`: Überprüft den aktuellen Schachstatus und reagiert demnach darauf. Besitzt den `check_resolver` und `move_validator_king_in_check` als Felder. 

  - `move_execution`:
    - `special_rules_handler`: Berechnet alle Sonderregeln wie "En Passant", Rochade und Bauernumwandlung.
    - `move_executor`: Führt den letztendlichen Zug aus und updated alle wichtigen Informationen. Besitzt den `special_rules_handler` als Feld.

  - `move_validation`: 
    - `move_safety_checker`: Berechnet und simuliert die möglichen Züge deiner verbündeten Figuren und überprüft danach den Einfluss auf den eigenen König.
    - `move_validator`: Berechnet und simuliert die möglichen Züge für den eigenen König, überprüft ebenfalls auf Patt.

  - `controller`: Dieser interagiert mit dem Model, der View und den verschiedenen Logiken und bringt den Spielfluss zum Laufen. Er besitzt demnach die ganze Logik, sowohl das Model und die View als Felder.

Wie läuft das Spiel nun ab?

Nach beginn des Spiels werden erstmals alle nötigen Informationen initilisiert, wie die Zuweisung der alive_pieces(list) des jeweiligen Spielers(player), 
das berechnen der möglichen Züge der Figuren und das laden der Figurenbilder entsprechend dem chessboard status nach.
Nachdem anklicken einer Figur aus deinem Team, wird für jeden möglichen Zug das entsprechende Feld(clickable_label) grün gefärbt.
Während des drag and drop Prozesses wird bei dem droppen überprüft, welche Farbe das Feld hat um demnach ein Signal an den Controller weiterzuleiten,
der die ensprechende methode danach ausführt.
Nachdem der move_executor alle wichtigen Daten überarbeitet hat und der Zug ausgeführt wurde wird überprüft ob eine Sonderregel möglich ist, dies wird dann markiert.
Eine mögliche Rochade wird als möglicher Zug gelb gefärbt und En Passant blau. Bei der Bauernumwandlung öffnet sich ein Fenster, mit dem man sich durch einen Klick aussuchen kann,
welche Figur man haben möchte. Dabei übergibt die Ui natürlich andere Signale an den Controller als bei einem normalen Zug.
Danach werden die möglichen Züge neuberechnet und passen sich dem neuen Schachbrettstand an. Danach prüft der chech_handler ob ein Schach vorliegt.
Ist dies der Fall, dann wird das Feld des Königs und der bedrohenden Figur rot gefärbt und die player Klasse weiß, dass sie im Schach steht.
Dies wird vor dem Spielertausch überprüft. Sollte der Spieler nicht im Schach stehen so kümmert sich der move_validator um die möglichen Züge und überprüft, welche wirklich legal sind.
Dies passiert nach dem Spielertausch. In diesem Muster wird das Spiel solange laufen, bis der check_handler erkennt dass du Schachmatt bist und somit keine möglichen Züge mehr hast,
oder der move_validator der dich auf Patt überprüft. In beiden Fällen wird sich ein Dialogfenster öffnen und es gibt die Wahl, ob man erneut spielen möchte oder ob man das Spiel schließen will.


## Architektur und Design
Ich habe versucht, mich so akkurat wie möglich an das MVC Modell zu halten.

## Entwicklungsprozess und -methodik
Für mein Projekt wurde ein MVC Model verwendet um klare Trennungen zwischen der Datenlogik, der Anwendungslogik und Benutzeroberfläche zu garantieren.
Das Projekt enthält eine organisierte Ordnerstruktur, die das navigieren des Projekts vereinfacht. Ebenso hält es den code übersichtlich.
Um die Systemstruktur und die Architektur so gut es geht zu veranschaulichen habe ich mich für ein Plant Uml Diagramm entschieden.
Damit man einen guten Überblick über das Vollständige Projekt zu erlangen war eine Dokumentation davon sehr sinnvoll.
Ebenfalls habe ich unit tests geschrieben, die den code überprüfen und robuster machen.
Um den code modularer zu gestalten wurden ebenfalls design pattern benutzt um dies zu gewährleisten.

## Herausforderungen und Lösungen
Eine große Herausforderung bestand darin, den Aufwand nicht zu unterschätzen, den das Schreiben zahlreicher Algorithmen zur Abdeckung aller legalen Züge mit sich bringt. 
Oft hatte ich das Gefühl, dass der Algorithmus alles beachten würde, bis mir bei dem testen ein Fehler aufgefallen ist. Dies konnte ich mit vielem 
testen, debugging und überarbeiten der Klassen und Methoden letztendlich beheben.

## Schlussfolgerungen und Lernerfahrungen
Ich habe gelernt mich deutlich besser bei einem Projekt zu organisieren und habe ein deutlich besseres Verständnis von Softwarearchitektur bekommen.
Ich konnte definitiv mein lösungsorientiertes Arbeiten steigern und habe einen deutlich stärkeren Ehrgeiz entwickelt. 
Ebenfalls habe ich gelernt wie man sich effektiv eigenständig Dinge beibringt und aktiv an einem Projekt arbeitet ohne aufzugeben obwohl man auch verzweifeln kann.
Ich konnte meine Kenntnisse in python deutlich stärken und habe PyQt kennengelernt und wie diese miteinander agieren.

## Zukünftige Arbeit und Verbesserungen
Ich habe vor, bessere tests zu schreiben die mehr Fälle abdecken und dem Programm mehr Sicherheit gewähren.
Ebenfalls bin ich daran interessiert eine Ai einzubauen, gegen die man auf verschiedenen Schwierigkeitsstufen spielen kann.
Eine Implementierung davon, gegen andere Spieler online spielen zu können.

