from playsound import playsound  
#playsound('/media/nvidi/nvidia/robo_AI/hello.mp3', True)
import os
import logging
import json
import cv2

from camera import cam
from pickle import NONE
from cv2 import rotate
from nltk.util import pr

#from neuralintents import GenericAssistant
import datetime
import googlesamples.assistant.grpc.pushtotalk as pushtotalk
import speech_recognition as sr

import datetime
import  os
import random


from os import path
import subprocess
from gtts import gTTS

from robo_tts import take_command, talk, change_language, talk_gtts
from robo_move3 import *
#from robo_AI import * 
import multiprocessing as mp
from threading import Thread

import click
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials


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
    
    angle(90, 70)
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
            angle(90, 45)
            time.sleep(1)
            angle(90, 70)
            left_dis = dis.getDistance()

            angle(90, 120)
            time.sleep(1)
            right_dis = dis.getDistance()
            angle(90, 70)

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


if __name__ == "__main__":
    q = mp.Queue() 
    #t3 = mp.Process(target= thred, args=(q,))
    t1 = mp.Process(target= cam,args=(q,))
    
    t2 = mp.Process(target=main_roboAI2, args=(q,))
    t1.start()
    #t3.start()
    path_of_startup ='/media/nvidi/nvidia/robo_AI/startup.txt'
    path_of_json = '/media/nvidi/nvidia/robo_AI/Intent1.json'
    path_of_model = '/media/nvidi/nvidia/robo_AI/neuralintents/test_model.h5'


    mappings = {'greeting' : function_for_greetings, 
                'stocks' : function_for_stocks,
                'TimeQuery' : time_now,
                'move_cam' : move_cam,
                "WhoAmI" : recogni,
                "detect_comm" : detect_cam,
                "detect_stop" : detect_stop,
                "follow"  : follow
                }

    #assistant = GenericAssistant(path_of_json, intent_methods=mappings ,model_name=path_of_model)
    #assistant.train_model()
    #assistant.save_model()
    #assistant.load_model(path_of_model)
    angle(100, 70)
    leftMotor = Motor(22, 24)
    rightMotor = Motor(13, 16)
  
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
                angle(90, 45)
            elif "look left" in massage:
                angle(100, 120)
            elif "look front" in massage:
                angle(100, 70)
            elif "detect this" in massage:
                #what is this
                print("detecting")
                q.put('detect')
            elif "detect stop" in massage:
                print("detect stop")
                q.put('detect stop')
            elif "follow this" in massage:
                q.put("follow")
                print("follow")
            elif "follow this" in massage:
                q.put("follow_line")
                print("follow")
            elif "ultra" in massage:
                #move_ar = move_ret(1)  
                t2.start()
            elif "stop code" in massage:
                q.put("END")
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

   
    
   
    

 
