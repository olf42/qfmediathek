# qfmediathek

## A minimalist mediathek service

### Summary

This program serves a single-page mediathek. Recordings can be played back,
but not downloaded (at least not directly). This is required by the 
"GEMA-Rahmenvertrag" (contract with the rightsholder). Therefore I will 
not implement it. :(

### Requirements

* CherryPy==5.1.0
* Jinja2==2.8
* MarkupSafe==0.23

### Installation

Put it on a webserver, and let it run. :)
You need to symlink a directory containing the recordings
as well as json-description file. This job can be done by
qfrecord, a simple tool, to record, and name streamdumps
using a (hopefully) provided stationxml file.

### StationXML

Is a crude, ugly XML standard to save schedules for
radiostations. As it is ugly, Querfunk descided, to make 
it worse, and use its own dialect. Hooray. Therefore, my
stationxml parser is useless for everybody, whose not 
specifically interested in Querfunk. :D
