import random

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hi!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == 'secret':
        return '`Tuguldur is in love with Misheel!`'
    
    if p_message == 'fact':
        return '`Misheel is the best!`'

