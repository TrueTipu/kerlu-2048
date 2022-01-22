import json
from data.defs import *
import random

#hallitsee high scoren tallentamisen, oikeastaan ei kovin olellista pelin kannalta mutta haluisn opetella miten tallennus toimisi
class Save_Manager():

    def save(score): #tallentaa scoren txt tiedostoon json muodossa
        data = {'score': Save_Manager.secret(score)} #salaa scoren ettei sitä voi huijata niin helposti
        with open(SAVE_DIRECT, 'w') as file: #avaa/luo tiedoston jos sitä ei vielä ole
            json.dump(data, file) #converttaa datan json formaatiin

    def secret(score): #pidin hauskaa tämän koodin kanssa, sen idea on olla sekava ettei kukaan huijaa pisteitä
        #loppujen lopuksi ei tätä edes ole vaikea purkaa mutta olkoon se tarpeeksi hyvä
        a = [random.randint(0, 1000000) for i in range(0, 10000)]
        a[KEY] = random.randint(0, 10000) 
        if a[KEY] == KEY:
            a[KEY] = a[KEY] // 2 *random.randint(5,18)
        a[a[KEY]] = (score + abs(a[KEY // 2 + 6] - 1000))
        return a

    def load(): #palauttaa scoren tiedostosijainnista
        try: #yrittää kerätä scoren tiedostosta
            with open(SAVE_DIRECT) as file:
                data = json.load(file)
                data = data['score']
        except: #jos tiedostoa ei olemassa, niin tallentaa scoren 0 (=jatkossa on tiedosto olemassa)
            Save_Manager.save(0)
            return 0
        if data: #jos dataa on olemassa
            score = data[data[KEY]] - abs(data[KEY // 2 + 6] - 1000) #poistaa salauksen
            return score 
        return 0
