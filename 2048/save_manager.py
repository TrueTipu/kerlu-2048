import json
import secrets
from defs import *
import random

class Save_Manager():
    def save(score):
        data = {'score': Save_Manager.secret(score)}
        with open(SAVE_DIRECT, 'w') as file:
            json.dump(data, file)

    def secret(score):
        a = [random.randint(0, 1000000) for i in range(0, 10000)]
        a[KEY] = random.randint(0, 10000) 
        if a[KEY] == KEY:
            a[KEY] = a[KEY] // 2 *random.randint(5,18)
        a[a[KEY]] = (score + abs(a[KEY // 2 + 6] - 1000))
        return a


    def load():
        try:
            with open(SAVE_DIRECT) as file:
                data = json.load(file)
                data = data['score']
        except:
            Save_Manager.save(0)
            return 0
        if data:
            score = data[data[KEY]] - abs(data[KEY // 2 + 6] - 1000)
            return score 
        return 0
