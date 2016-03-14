#!/usr/bin/env python3

__author__ = 'olf'

import os
from datetime import datetime
import cherrypy
import os.path
import json
from jinja2 import Environment, PackageLoader
import locale

# The directory where recordings (mp3) and datafiles (json) are recorded to by qfrecord
RECORD_DIR = "../qfrecord/recordings"

class QFMediathek(object):

    def __init__(self, template_env):
        '''
        Initializes the lists which hold the files.
        '''
        self.audio_files = []
        self.data_files = []
        self.data = []
        self.env = template_env

    def fetch_files(self):
        '''
        Builds lists with files, and checks, if every audio/data file has
        a corresponding partner. The lists are ordered, such that the
        most recent recording is the first element (can be stripped easily,
        in case the recording is still incomplete, when served.
        it saves these lists in self.audio_files and self.data_files
        '''
        files = os.listdir(RECORD_DIR)
        self.audio_files = []
        self.data_files = []
        self.data = []
        self.newdata = []
        # Split files in audio an data files
        for record in files:
            if record.split('.')[1] == "json":
                self.data_files.append(record)
            elif record.split('.')[1] == "mp3":
                self.audio_files.append(record)

        # Bring the lists in a defined order
        self.audio_files.sort()
        self.data_files.sort()
        self.audio_files.reverse()
        self.data_files.reverse()

        # Check if every audio has a data file
        for audio, data in zip(self.audio_files, self.data_files):

            # We check if every audiofile has a corresponding data file
            if audio.split('.')[0] != data.split('.')[0]:
                raise ValueError("Some Audio is missing Data or vice versa!")

            # we put the filename in the datafile, s.t. we don't need to
            # give it to the template later
            with open(os.path.join(RECORD_DIR, data), 'r') as datafile:
                jsondata = json.loads(datafile.read())
                jsondata['filename'] = audio

                #Extract date info from filename
                datestring, jsondata['time'] = audio.split('_')[:2]
                airdate = datetime.strptime(datestring, "%Y-%m-%d")
                jsondata['date'] = airdate.strftime("%d.%m.%Y")
                jsondata['weekday'] = airdate.strftime("%A")

                self.data.append(jsondata)

        # set initial weekday
        weekday = self.data[0]['weekday']
        day = { weekday : []}

        # sort by weekday
        for element in self.data:
            if element['weekday'] == weekday:
                day[weekday].append(element)
            else:
                self.newdata.append(day)
                weekday = element['weekday']
                day = { weekday : []}
                day[weekday].append(element)
        #append the last day
        self.newdata.append(day)


    @cherrypy.expose
    def index(self):
        '''
        Mediathek index page containg all recordings of last week.
        :return:
        '''
        self.fetch_files()
        return self.env.get_template('index.html').render(content=self.newdata)

if __name__ == "__main__":

    # Ensure, that we end up with german names of the weekdays
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

    current_dir = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=PackageLoader('qfmediathek', 'templates'))

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8029,
        'server.thread_pool_max': 500,
        'server.thread_pool': 100,
        'log.screen': True
    })

    cherrypy.tree.mount(QFMediathek(env), "/", {
            '/': {'tools.staticdir.on': True,
                  'tools.staticdir.dir': os.path.join(current_dir, 'public'),
                  'tools.sessions.on': True,
                  'tools.sessions.storage_type' : "file",
                  'tools.sessions.storage_path' : os.path.join(current_dir, "sessions")
                  }
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
