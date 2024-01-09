# Projektname
Chess

## Überblick und Motivation
Mein Schachspiel wurde in Python geschrieben und wird durch PyQt6 dargestellt.
Das Ziel war es das Spiel mit allen gängigen und auch speziellen Regeln nachzubauen, da ich mich für Schach interessiere und ich mich selbst herausfordern wollte.

## Ziele und Projektumfang
Das Hauptziel war, ein funktionstüchtiges Schachprogramm nachzubauen dass sich an alle offiziellen Regeln hält.
Eingeschlossen sind ebenfalls die Sonderregeln "En Passant", Rochade, und die Bauernumwandlung. Ebenfalls besteht die Möglichkeit nach dem fertigspielen eines Spiels, es nochmal zu spielen.
Was bisher noch nicht implementiert wurde ist ein Multiplayer oder eine Ai.

## Technologien und Werkzeuge
Das Projekt wurde in Pycharm geschrieben, benutzt und kennengelernt habe ich bisher PyQt, pytest, git und puml

## Funktionalitäten und Features
Mein Projekt wurde in drei Teile aufgebaut:

Model: 
  chessboard: das chessboard beinhaltet den aktuellen Stand des Spiels und besitzt die verschiedenen Spielfiguren.
  player: enthält Informationen über eigene Figuren, deren möglichen Züge und den aktuellen Schachstand.
  chesspieces: diese haben Informationen über ihr mögliches Bewegungsmuster.

View:
  ui_chessboard: ist dem chessboard model nachempfunden und enthält für alle Felder des Schachbretts jeweils ein QLabel dass passend dunkel oder hell gefärbt ist.
                  Ebebso zeigt es die Koordinaten an den Seitenrändern an, das heißt 1-8 und A-H.
  
  clickable_label: eine überschriebene QLabel Klasse deren drag and drop Vorgang sowie das hinzufügen von svg Bildern bishin zu dem animieren des Labels selbst überarbeitet wurde.

Controller: 
  check_management:
    check_resolver: berechnet die möglichen Verteidigungszüge deiner Figuren sobald du im Schach stehst.
    move_validator_king_in_check: berechnet die möglichen Züge des Königs wenn er im Schach steht.
    check_handler: überprüft den aktuellen Schachstatus und reagiert demnach darauf. Besitzt den check_resolver und move_validator_king_in_check als Felder. 

  move_execution:
    special_rules_handler: berechnet alle Sonderregeln wie "En Passant", Rochade und Bauernumwandlung.
    move_executor: führt den letztendlichen Zug aus und updated alle wichtigen Informationen. Besitzt den special_rules_handler als Feld.

  move_validation: 
    move_safety_checker: berechnet und simuliert die möglichen Züge deiner verbündeten Figuren und überprüft danach den Einfluss auf den eigenen König.
    move_validator: berechnet und simuliert die möglichen Züge für den eigenen König, überprüft ebenfalls auf Patt.

  controller: dieser interagiert mit dem Model, der View und den verschiedenen Logiken und bringt den Spielfluss zum laufen. Er besitzt demnach die ganze Logik, sowohl das Model und die View als Felder.

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
Ich habe versucht, so akkurat wie möglich mich an das MVC Modell zu halten.
Der genaue Aufbau ist in meinem Diagramm nachschaubar: 

## Entwicklungsprozess und -methodik
- Angewandte Entwicklungsprozesse und Methodiken
- Übersicht über den Entwicklungszyklus

## Herausforderungen und Lösungen
- Wichtige Herausforderungen während der Entwicklung
- Angewandte Lösungen

## Schlussfolgerungen und Lernerfahrungen
Ich habe gelernt mich deutlich besser bei einem Projekt zu organisieren
- Zusammenfassung der Lernerfahrungen
- Beitrag zur persönlichen oder beruflichen Entwicklung

## Zukünftige Arbeit und Verbesserungen
- Mögliche Verbesserungen und Erweiterungen für das Projekt

