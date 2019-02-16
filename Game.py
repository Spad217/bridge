import Deck
import encrypt
from requests import get
from getpass import getpass

id_bot = '527389225'
crypt_token = b'S9SW2ZpC1afoRdJtA9awB4iSqqc1rNjj+pIUQQp06KZopelcV/DcIINVXB+a3iU='


@encrypt.decrypt(getpass('write secret code> '), crypt_token)
def req(method, params, *argv, token=None):
    url = 'https://api.telegram.org/bot' + id_bot + ':' + token + '/' + method
    return get(url, params).json()


def check_good_cards(last_card, deck, isTake):
    good_cards = []
    for card in deck:
        if last_card[0] == card[0] or last_card[1] == card[1]:
            good_cards.append(card)
        elif card[0] == 'J':
            good_cards.append(card)
    good_cards.append('Pass' if isTake else 'Take')
    text = '{"inline_keyboard": [['
    for card in good_cards:
        if (not good_cards.index(card) % 5) and good_cards.index(card) != 0:
            text += '],['
        text += '{"text": {text}, "callback_data": {text}},'.format(text=card)
    return text + ']]'


def send(who, deck_in_hand, deck, isMove, isTake=False, id_message=None):
    '''
    opponent's move
    deck: 6♠ 6♦ T♦ T♣ J♥
    you cards: J♦ 7♠
    (wait)
    '''
    text = 'you turn\n' if isMove else 'opponent\'s move\n'
    text += 'deck: ' + ' '.join(deck) + '\n'
    text += 'you cards:' + ' '.join(deck_in_hand) + '\n'
    params = {'text': text, 'chat_id': who,
              'reply_markup': check_good_cards(deck[-1], deck_in_hand, isTake)}
    if id_message is None:
        return req('sendMessage', params)
    else:
        return req('editMessageText', params + {'message_id': id_message})


print(send())


def wait_requst():
    pass

def start(sender, receiver):
    main_deck = Deck.Deck()
    second_deck = Deck.Deck([main_deck.pop()])
    p1 = [main_deck.pop() for i in range(4)]
    p2 = [main_deck.pop() for i in range(5)]
