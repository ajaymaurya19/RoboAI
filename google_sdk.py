
# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample that implements a text client for the Google Assistant Service."""

import os
import logging
import json
import cv2
from camera import cam

from pickle import NONE

from cv2 import rotate
from nltk.util import pr

from neuralintents import GenericAssistant
import datetime
import googlesamples.assistant.grpc.pushtotalk as pushtotalk
import speech_recognition as sr
import pyttsx3
import webbrowser
#import pywhatkit
import datetime
import  os
import random
import sys
import re
import requests

from os import path
import subprocess
from gtts import gTTS





from robo_tts import take_command, talk, change_language, talk_gtts
from robo_move import *
from robo_AI import * 
import multiprocessing as mp
from threading import Thread





import click
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from playsound import playsound  
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

try:
    from googlesamples.assistant.grpc import (
        assistant_helpers,
        browser_helpers,
    )
except (SystemError, ImportError):
    import googlesamples.assistant.grpc.assistant_helpers
    import googlesamples.assistant.grpc.browser_helpers

query =""

ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING


class SampleTextAssistant(object):
    """Sample Assistant that supports text based conversations.

    Args:
      language_code: language for the conversation.
      device_model_id: identifier of the device model.
      device_id: identifier of the registered device instance.
      display: enable visual display of assistant response.
      channel: authorized gRPC channel for connection to the
        Google Assistant API.
      deadline_sec: gRPC deadline in seconds for Google Assistant API call.
    """

    def __init__(self, language_code, device_model_id, device_id,
                 display, channel, deadline_sec):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_state = None
        # Force reset of first conversation.
        self.is_new_conversation = True
        self.display = display
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False

    def assist(self, text_query):
        """Send a text request to the Assistant and playback the response.
        """
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=self.language_code,
                    conversation_state=self.conversation_state,
                    is_new_conversation=self.is_new_conversation,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            # Continue current conversation with later requests.
            self.is_new_conversation = False
            if self.display:
                config.screen_out_config.screen_mode = PLAYING
            req = embedded_assistant_pb2.AssistRequest(config=config)
            assistant_helpers.log_assist_request_without_audio(req)
            yield req

        text_response = None
        html_response = None
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        return text_response, html_response


@click.command()
@click.option('--api-endpoint', default=ASSISTANT_API_ENDPOINT,
              metavar='<api endpoint>', show_default=True,
              help='Address of Google Assistant API service.')
@click.option('--credentials',
              metavar='<credentials>', show_default=True,
              default=os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json'),
              help='Path to read OAuth2 credentials.')
@click.option('--device-model-id',default=ASSISTANT_API_ENDPOINT,
              metavar='<device model id>',
              required=True,
              help=(('Unique device model identifier, '
                     'if not specifed, it is read from --device-config')))
@click.option('--device-id',default=ASSISTANT_API_ENDPOINT,
              metavar='<device id>',
              required=True,
              help=(('Unique registered device instance identifier, '
                     'if not specified, it is read from --device-config, '
                     'if no device_config found: a new device is registered '
                     'using a unique id and a new device config is saved')))
@click.option('--lang', show_default=True,
              metavar='<language code>',
              default='en-US',
              help='Language code of the Assistant')
@click.option('--display', is_flag=True, default=False,
              help='Enable visual display of Assistant responses in HTML.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Verbose logging.')
@click.option('--grpc-deadline', default=DEFAULT_GRPC_DEADLINE,
              metavar='<grpc deadline>', show_default=True,
              help='gRPC deadline in seconds')



def main(api_endpoint, credentials,
         device_model_id, device_id, lang, display, verbose,
         grpc_deadline, *args, **kwargs):
    # Setup logging.
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    global query
    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        return

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    with SampleTextAssistant(lang, device_model_id, device_id, display,
                             grpc_channel, grpc_deadline) as assistant:
    
        #query = click.prompt('')
        #click.echo('<you> %s' % query)
        
        response_text, response_html = assistant.assist(text_query=query)
        if display and response_html:
            system_browser = browser_helpers.system_browser
            system_browser.display(response_html)
        if response_text:
            #click.echo('<@assistant> %s' % response_text)
            talk_gtts(response_text,"en")

def sdk(query):
    main()


def main_roboAI2(conn):
    
    setServoAngle(90)
    rightMotor = Motor(32, 13, 16)
    leftMotor = Motor(32, 22, 24)
    #rightMotor = Motor(32, 13, 16)
    speed = 25
    leftMotor.setSpeed(speed)
    rightMotor.setSpeed(speed)
    angle = 90
    dis = DistanceSensor()
    
    while True:        
        data = dis.getDistance()
            #print(data)
        
        if data == -1:
            continue
        if data < 20:
            print('stop')
            leftMotor.stop()
            rightMotor.stop()
        if data >20:
                #print(data)
            print("goForward")
            leftMotor.goForward()
            rightMotor.goForward()
        elif data < 20: 
            print("stop")
            setServoAngle(0)
            time.sleep(1)
            setServoAngle(90)
            left_dis = dis.getDistance()

            setServoAngle(180)
            time.sleep(1)
            right_dis = dis.getDistance()
            setServoAngle(90)

            if left_dis and right_dis< 10:
                print("gobackword")
                leftMotor.goBackward()
                rightMotor.goBackward()
                time.sleep(2)
            elif left_dis > right_dis:
                print("goleft")
                leftMotor.stop()
                rightMotor.goForward()
                time.sleep(2)
            elif left_dis < right_dis:
                print('goright')
                leftMotor.goForward()
                rightMotor.stop()
                time.sleep(2)
        dae = conn.recv()
        if isinstance(dae, str) and dae == "END":
            print('Last message received')
            break


def camera(conn):
    cap = cv2.VideoCapture(0)
    cap.set(3,640.0) #set the size
    cap.set(4,480.0)  #set the size
    print("cap")

    

    detect = False
    line_follower = False
    #myModel = mnSSD("ssd-mobilenet-v2", 0.5)
    while True:
        #data =  conn.recv()
        _, img = cap.read()
        if data =="detect":
            objects = myModel.detect(img,  True)
            if len(objects)!=0:
                print(objects[0][0])
                if objects[0][0]=="person":
                        #print(objects[0][0])
                    print(objects[0][0],img_reco(img, True))
        if line_follower:
            linefollow()
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key ==27:
            break
       
       
     
            
        data =  conn.recv()
        print(data) 
        if isinstance(data, str) and data == "END":
            print('Last message received')
            break
      
            
     
      

    cap.release()
    cv2.destroyAllWindows()

datas = []
def thred(conn):
    while True:
        if len(datas)>0:
            for da in datas:
                conn.send(da)
            datas.clear()  
        else:
            
            conn.send(0)   
        time.sleep(0.001)
n=2
if __name__ == "__main__":
    parent_conn, child_conn = mp.Pipe() 
    t3 = Thread(target= thred, args=(parent_conn,))
    t1 = mp.Process(target= cam,args=(parent_conn,))
    
    t2 = mp.Process(target=main_roboAI2, args=(child_conn,))
    t1.start()
    path_of_startup ='/media/nvidi/nvidia/robo_AI/startup.txt'
    path_of_json = '/media/nvidi/nvidia/robo_AI/Intent1.json'
    path_of_model = '/media/nvidi/nvidia/robo_AI/neuralintents/test_model.h5'


    mappings = {'greeting' : function_for_greetings, 'stocks' : function_for_stocks, 'TimeQuery' : time_now}

    assistant = GenericAssistant(path_of_json, intent_methods=mappings ,model_name=path_of_model)
    #assistant.train_model()
    #assistant.save_model()
    assistant.load_model(path_of_model)
    setServoAngle(90)
    leftMotor = Motor(32, 22, 24)
    rightMotor = Motor(32, 13, 16)
    speed = 25
    leftMotor.setSpeed(speed)
    rightMotor.setSpeed(speed)
    with open(path_of_startup, "r") as m:
        sents = m.read().split("\n\n")
        se = random.choice(sents)
    print(se)
    talk_gtts(se,'en')
    n=1
    while True:
        try:
            #parent_conn.send(['0'])
            messag = take_command()           
            massage = messag[0]
            language = messag[1]
            print(massage)
            if "look right"in massage:
                print("looking right")
                setServoAngle(0)
            elif "look left" in massage:
                setServoAngle(180)
            elif "look front" in massage:
                setServoAngle(90)
            elif "detect this" in massage:
                print("detecting")
                datas.append("detect")
            elif "follow this" in massage:
                print("follow")
            elif "ultra" in massage:
                #move_ar = move_ret(1)
                if n==1:
                    t3.start()
                    t2.start()
                    n=n+1
                else:
                    t2.start()
            
            elif "camera" in massage:
                
              
                #t3.start()
                t1.start()
                #camera(1)
                print("cam started")
                   
            
            elif "camera Stop" in massage:
                datas.append("stop")
            elif "follow line" in massage:
                linefollow()
            elif "stop all" in massage:
                datas.append("END")
                #parent_conn.close()
                #break
            elif "stop code" in massage:
                datas.append("stop")
                datas.append("END")
                parent_conn.close()
                break
                         
            else:
                print(massage)
                mess = assistant.request(massage)
                print(mess)
                if len(mess)<1:
                    sdk(massage)
            
        
                else:
                    talk_gtts(mess,'en')

        except:
            pass
       
    print("close All connection")
    #sys.exit()

   
    
   
    

 