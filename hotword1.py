#!/usr/bin/env python

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


from __future__ import print_function

import argparse
import os.path
import json
import time
from bluezero import microbit

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

x = None
exit_commands  = ['quit', 'cancel', 'exit']

def process_event(event, assistant, ubit):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
    """
    #if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        

    #if (event.type == EventType.ON_RESPONDING_STARTED and event.args and not event.args['is_error_response']):
  

    #print('FD:',event)
    
    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        print(event.args['text'])

        if event.args['text'].lower() == 'talk to my test app':
        	global x 
        	x = 1
        	

        if event.args['text'].lower() in exit_commands:
        	x = 0
        	ubit.heart_animate_stop()
        	print('*exit*')

        if (x == 1):
        	if 'led on' in event.args['text'].lower():
        		print('*turn LED on*')
        		ubit.heart_animate_start()

        		

        	if 'led off' in event.args['text'].lower():
        		print('*turn LED off*')
        		ubit.heart_animate_stop()
        		



    #if event.type == EventType.ON_RESPONDING_FINISHED:
        


    #if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
    #        event.args and not event.args['with_follow_on_turn']):

def main():
	ubit = microbit.Microbit(name='gavag')
	ubit.connect()
	print('connected to micro:bit')
	ubit.event_config()

	parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
	args = parser.parse_args()
	with open(args.credentials, 'r') as f:
		credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))


	with Assistant(credentials) as assistant:
		for event in assistant.start():
			process_event(event, assistant, ubit)

	ubit.disconnect()

if __name__ == '__main__':
    main()
