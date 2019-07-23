#!/usr/bin/env python3
from ctypes import *
from contextlib import contextmanager
import pyaudio
import speech_recognition as sr
import pyttsx3

import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import datetime
import time

engine = pyttsx3.init()
voice_id ='english-US'
engine.setProperty('voice', voice_id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
def say(text):
    engine.say(text)
    engine.say("   ")
    engine.runAndWait()

say("hi")
say("what can i do for you?")
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)



r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)

    print(r.energy_threshold)
    print("Chucking rate: ", source.CHUNK)
    print("format rate :", source.format)
    print('')
    print('')
    print("Say something!...")

    r.energy_threshold +=300
    print(r.energy_threshold)
    audio = r.listen(source)

    # Speech recognition using Google Speech Recognition

try:
    print("Parsing ...")  # Debugging To
    # for testing purposes, we're just using the default API key
    text = r.recognize_google(audio, language='en-US')
    print("You said: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
except sr.HTTPError as e:
    print("Couldn't connect to the websites perhaps , Hyper text transfer protocol error", e)

rec = ['recognise me','who am I','identify me','ID','identifying me','identification']
if text in rec:
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval != True:
        raise ValueError("Can't read frame")

    cv2.imwrite('test.jpg', frame)


    def get_encoded_faces():
        """
        looks through the faces folder and encodes all
        the faces

        :return: dict of (name, image encoded)
        """
        encoded = {}

        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in names:
                if f.endswith(".Jpg") or f.endswith(".Png"):
                    face = fr.load_image_file("faces/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding

        return encoded


    def unknown_image_encoded(img):
        """
        encode a face given the file name
        """
        face = fr.load_image_file("faces/" + img)
        encoding = fr.face_encodings(face)[0]

        return encoding


    def classify_face(im):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        :param im: str of file path
        :return: list of face names
        """
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())

        img = cv2.imread(im, 1)
        # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        # img = img[:,:,::-1]

        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Draw a box around the face
                cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)

        # Display the resulting image
        while True:

            cv2.imshow('Video', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                say(face_names)



    say(classify_face('test.jpg'))


quiz =['answer a question','answer me']
if text in quiz:
    say('ask it')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        print(r.energy_threshold)
        print("Chucking rate: ", source.CHUNK)
        print("format rate :", source.format)
        print('')
        print('')
        print("ask your question!...")

        r.energy_threshold += 300
        print(r.energy_threshold)
        audio = r.listen(source)

        # Speech recognition using Google Speech Recognition

    try:
        print("Parsing ...")  # Debugging To
        # for testing purposes, we're just using the default API key
        text = r.recognize_google(audio, language='en-US')
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except sr.HTTPError as e:
        print("Couldn't connect to the websites perhaps , Hyper text transfer protocol error", e)
    time = ['what time is it']
    if text in time:
        currentDT = datetime.datetime.now()

        say("Current Year is: %d" % currentDT.year)
        say("Current Month is: %d" % currentDT.month)
        say("Current Day is: %d" % currentDT.day)
        say("Current Hour is: %d" % currentDT.hour)
        say("Current Minute is: %d" % currentDT.minute)
        say("Current Second is: %d" % currentDT.second)
        say("Current Microsecond is: %d" % currentDT.microsecond)


class Command:

    def __init__(self, message):

        self.message = message

        self.all = ['get', 'pick up', 'deliver', 'bring', 'take', 'put', 'give', 'grasp', 'place', 'go', 'navigate',
                    'tell', 'answer', 'sey', 'find', 'look for', 'locate']

        self.listt = ['manipulation', 'navigation', 'information_order', 'finding']

        self.man = ['get', 'pick up', 'deliver', 'bring', 'take', 'put', 'give', 'grasp', 'place']

        self.nav = ['go', 'navigate']

        self.inf = ['tell', 'answer', 'sey']

        self.fnd = ['find', 'look for', 'locate']

        self.obj = ['beer', 'toiletries', 'coke', 'pasta', 'it', 'drinks', 'noodles', 'food',
                    'snacks', 'tea', 'soup', 'water', 'pringles', 'cookies']

        self.per = ['me', 'rubin', 'someone', 'person', 'morgan', 'taylor', 'hayden', 'jamie', 'peyton', 'alex',
                    'jordan', 'michael', 'tracy']

        self.plc = ['bar', 'bedroom', 'bathroom', 'bidet', 'chair', 'armchair', 'desk', 'washbasin', 'counter',
                    'microwave', 'kitchen', 'sink', 'cabinet', 'sideboard', 'dresser', 'cupboard', 'shower',
                    'dining table', 'wardrobe', 'dining room', 'baby chair', 'coffee table', 'dish washer',
                    'sofa', 'bed', 'corridor', 'washing machine', 'towel rail', 'cutlery drawer', 'tv couch',
                    'fireplace', 'counter', 'bathtub', 'bookshelf', 'fridge', 'drawer', 'freezer', 'living room',
                    'night table', 'center table', 'living room', 'baby chair', 'bathroom cabinet', 'dishwasher'
                    ]

        self.pieces = ['night table', 'center table', 'living room', 'dining room', 'baby chair', 'bathroom cabinet',
                       'washing machine', 'towel rail', 'coffee table', 'cutlery drawer', 'tv couch', 'pick up',
                       'dining table', 'look for']

        self.prep = ['in', 'on', 'from', 'at', 'to']

        self.wts = ['what day is today', 'what day is tomorrow', 'the question', 'your teams name', 'the time',
                    'a joke',
                    'something about yourself', 'the day of the month', 'your teams affiliation', 'the day of the week',
                    'your teams country', 'how many']

        self.first = ['night', 'center', 'living', 'baby', 'towel', 'coffee', 'cutlery', 'tv', 'pick', 'dining',
                      'washing', 'look']

        self.destination_2 = None
        self.person = None
        self.destination = None
        self.information_question = None
        self.object = None
        self.manipulation = None
        self.navigation = None
        self.finding = None
        self.information_order = None
        self.action = None
        self.type = None
        self.action_2 = None
        self.action_3 = None

    def classify(self):
        nm = self.listt

        classifier = {}

        place = []
        person = []
        location = []
        information_question = []
        object = []
        manipulation = []
        navigation = []
        finding = []
        information_order = []

        my_list = self.message.split(' ')
        y = 0
        s = 0
        b = 0
        v = 0

        for x in self.pieces:

            if x in self.message:
                code = x.split(' ')
                n = my_list.index(code[0])

                my_list = [m for m in my_list if m not in code]
                my_list.insert(n, x)

        for x in self.wts:

            if x in self.message:
                wcode = x.split(' ')
                w = my_list.index(wcode[0])
                my_list = [y for y in my_list if y not in wcode]
                my_list.insert(w, x)
        print(my_list)

        for myitem in my_list:

            if myitem in self.all:
                y += 1

                if y == 2:
                    s = classifier.copy()

                    classifier = {}

                    self.action_2 = myitem

                if y == 3:
                    b = classifier.copy()

                    classifier = {}

                    self.action_3 = myitem

            if myitem in self.man:
                print(myitem, "is manipulation type")

                manipulation.append(myitem)


                classifier["type"] = nm[0]
                self.type = nm[0]
                classifier["action"] = myitem
                self.action = myitem

            if myitem in self.nav:
                print(myitem, "is navigaion type")

                navigation.append(myitem)

                classifier["type"] = nm[1]
                self.type = nm[1]
                classifier["action"] = myitem
                self.action = myitem

            if myitem in self.inf:
                print(myitem, "is information type")

                information_order.append(myitem)

                classifier["type"] = nm[2]

                self.type =nm[2]

                classifier["action"] = myitem

                self.action = myitem

            if myitem in self.fnd:
                print(myitem, "is find type")

                finding.append(myitem)

                classifier["type"] = nm[3]

                self.type = nm[3]

                classifier["action"] = myitem

                self.action = myitem

            if myitem in self.obj:
                print(myitem, "is an object")

                object.append(myitem)

                classifier["object"] = myitem

                self.object = myitem

            if myitem in self.per:
                print(myitem, "is person's name")

                person.append(myitem)

                classifier["person"] = myitem

                self.person = myitem

            if myitem in self.prep:
                print(myitem, "is preprestion")

                location.append(myitem)

            if myitem in self.plc:
                print(myitem, "is place's name")

                place.append(myitem)
                v += 1
                if v ==1 :
                    classifier["destination"] = myitem
                    self.destination = myitem



                if v == 2 :

                    classifier["second_destination"] = myitem
                    self.destination_2 = myitem




            if myitem in self.wts:

                print(myitem, "is information question")

                information_question.append(myitem)

                classifier["information_question"] = myitem


            else:
                continue

        print('\t'"__/\__          __/\__ ")
        print('\t'"\    /          \    / ")
        print('\t'"/_  _\          /_  _\ ")
        print('\t'"  \/              \/   ")
        print('\t'"  /               /  ")
        print('\t'" /               /   ")
        print('\t'"/____ azarakhsh /____")
        print('\t'"    /               /")
        print('\t'"   /               / ")
        print('\t'"  /               /  ")
        print('\t'" /               /   ")

        if len(manipulation) != 0:
            print('manipulation:', manipulation)

        if len(navigation) != 0:
            print('navigation:', navigation)

        if len(finding) != 0:
            print('finding:', finding)

        if len(information_order) != 0:
            print('information_order:', information_order)

        if len(location) != 0:
            print('location:', location)

        if len(place) != 0:
            print('place:', place)

        if len(person) != 0:
            print('person:', person)

        if len(information_question) != 0:
            print('information_question:', information_question)

        if len(object) != 0:
            print('object:', object)

        print("")
        print("")
        print(" /\/\/\/\/\/\/\/\/\/\/\/\ ")
        print("")
        print("")
        print("classifier dictionary : ")
        if s != 0:
            print(s)
            print(" ")
            print("and")
            print(" ")
        if b != 0:
            print(b)
            print(" ")
            print("and")
            print(" ")
        print(classifier)
        say(classifier)

        return classifier



my_object = Command(text)

my_object.classify()


say(text)
say("is that correct?")
