7.7
==================================

häcksler:
        GSTreamer(?) konvertiert alle video-files in normalisierte chunks (width*height, RGBA, maxlength)
        test-file: in raw RGBA


schaufler:
        fügt neue chunks zum komposthaufen dazu
             komposthaufen wächst




bots (python)
     manipulieren daten auf selbst-bestimmter ebene (frames, pixels, bytes)

     werden zyklisch aufgerufen

     kompost kann auch wieder schrumpfen

  kleines Framework?

  * composter.py
    ruft zyklisch die Bots aus der Liste (class BotList) auf.
  * cutvideo.py
    zerstückelt eingehende Videos zu Chunks und fügt sie in die
    an zufälliger Stelle in die ChunkList ein.
  * gluechunks.py
    Fügt die Chunks aus der ChunkList zu einem (großen) File zusammen,
    das dann mit playraw.sh gespielt oder mit raw2video.sh wieder
    komprimiert werden kann.
  * addBotToList.py
    Fügt einen Bot zur BotList hinzu.

  * Klassen
    * Chunk(.py)
      Abstraktion für ein Stück eines Videos.
    * ChunkList(.py)
      Liste von Chunks mit Methoden zum Management und zum Datenzugriff.
  * CompostAccess(.py)
    Eine Art Interface für Bots um auf Videodaten zugreifen zu können.
  * BotList(.py)
    Liste der Bots/Agents

Verzeichnisse und Files:

  home:       /home/vc/             :: basedir
  scripts:    /home/bc/bin/*        :: .sh and .py files
  chunks:     /home/vc/chunks/      :: .raw video chunks
  configs:    /home/vc/config/      :: configs for .py files
  incoming:   /home/vc/incoming/    :: incoming .ogv files
  raw video:  /home/vc/video.raw    :: result of gluechunks.py
  ogg video:  /home/vc/video.ogv    :: result of raw2video.sh
  new video:  /home/vc/infile.raw   :: result of video2raw.sh

