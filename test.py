from pprint import pprint

{
    'delete_chat_photo': False,
    'new_chat_photo': [],
    'from': {
        'username': u'Pollquinbot',
        'first_name': u'CheesePoll',
        'is_bot': True,
        'id': 325958539
    },
    'text': u"Let's <b>create</b> a new poll. First, send me the question.",
    'caption_entities': [],
    'entities': [],
    'channel_chat_created': False,
    'new_chat_members': [],
    'supergroup_chat_created': False,
    'chat': {
        'username': u'Zujiry',
        'first_name': u'Panda',
        'last_name': u'Baer',
        'type': u'private',
        'id': 195708628
    },
    'photo': [],
    'date': 1520516751,
    'group_chat_created': False,
    'message_id': 318
}

pprint(
    {'Processing Update': {'update_id': 203435914, 'callback_query': {
        'from': {'username': u'Zujiry', 'first_name': u'Panda', 'last_name': u'Baer', 'is_bot': False,
                 'language_code': u'en-GB', 'id': 195708628}, 'chat_instance': u'-7941871470526536410',
        'message': {'delete_chat_photo': False, 'new_chat_photo': [],
                    'from': {'username': u'Pollquinbot', 'first_name': u'CheesePoll', 'is_bot': True, 'id': 325958539},
                    'text': u'Question', 'caption_entities': [], 'entities': [], 'channel_chat_created': False,
                    'new_chat_members': [], 'supergroup_chat_created': False,
                    'chat': {'username': u'Zujiry', 'first_name': u'Panda', 'last_name': u'Baer', 'type': u'private',
                             'id': 195708628}, 'photo': [], 'date': 1520521519, 'group_chat_created': False,
                    'message_id': 402}, 'data': u'Opt1', 'id': u'840562158470637317'}}}
)
