import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, PrivateRoom, Notification
from .models import User
from .function import get_messages
from datetime import datetime

class ChatConsumer(WebsocketConsumer):

    def get_all_messages(self, data):
        messages = get_messages(data['room_name'])
        if messages == 'нет сообщений':
            content ={
            'type': 'messages',
            'messages': messages
            }
        else:
            content ={
                'type': 'messages',
                'messages': self.messages_to_json(messages)
            }
        self.send(text_data=json.dumps(content))



    def new_message(self, data):
        print(data['author'])
        print(data['recipient_id'])
        print(type(data['recipient_id']))
        message = Message(author=User.objects.get(username=data['author']),content=data['content'],private_room=PrivateRoom.objects.get(room_name=data['room_name']))
        message.save()
        notification = Notification(Message=message,user=User.objects.get(id = data['recipient_id']))
        notification.save()
        content = self.message_to_json(message)
        print(message.author.username+ message.content)  
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'img': message.author.profile_pic.url,
            'content': message.content,
            'timestamp': message.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        }

    
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    commands = {
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        if text_data_json['command']=='new_message':
            print('new_message')
            self.new_message(text_data_json)
        elif text_data_json['command']=='get_all_messages':
            print('get_all_messages')
            self.get_all_messages(text_data_json)
        # self.commands[text_data_json['command']](self, text_data)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message
        }))