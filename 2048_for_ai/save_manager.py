import json
from defs import *
import random

#hallitsee high scoren tallentamisen, oikeastaan ei kovin olellista pelin kannalta mutta haluisn opetella miten tallennus toimisi
class Save_Manager():

    def save(score): #tallentaa scoren txt tiedostoon json muodossa
        data = {'score': score}
        with open(SAVE_DIRECT, 'w') as file: #avaa/luo tiedoston jos sitä ei vielä ole
            json.dump(data, file) #converttaa datan json formaatiin

    def load(): #palauttaa scoren tiedostosijainnista
        try: #yrittää kerätä scoren tiedostosta
            with open(SAVE_DIRECT) as file:
                data = json.load(file)
        except: #jos tiedostoa ei olemassa, niin tallentaa scoren 0 (=jatkossa on tiedosto olemassa)
            Save_Manager.save(0)
            return 0
        if data: #jos dataa on olemassa
            score = data['score']
            return score 
        return 0
