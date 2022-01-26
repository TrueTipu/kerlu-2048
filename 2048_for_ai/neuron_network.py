import random
import numpy as np
import scipy.special as sc_s
from defs import *



class NNet():
    def __init__(self, size_input, size_layer1, size_output, brains = None):
        self.size_output = size_output
        self.size_layer1 = size_layer1
        self.size_input = size_input
        if not(brains):
            self.layer1_w = np.random.uniform(-0.5, 0.5, (self.size_input + 1, self.size_layer1)) 
            #huom ei käytetä nyt bias lol
            #huom2 tehdään eripäin ku videos koska lol
            self.o_layer_w = np.random.uniform(-0.5, 0.5, (self.size_layer1 + 1, self.size_output)) 
            #eddellee eripäin koska niin opin ja imo selkeenpää laittaa inputit selkeästi

        else:
            self.layer1_w = np.array(brains[0])
            self.o_layer_w = np.array(brains[1])
        self.activation_func_sigmoid = lambda x : sc_s.expit(x) #katso sieppaaa.png kansiosta
        #huom scipy.special.expit() on suoraan sigmoid meidän puolesta

    #vastaa get outputtia
    def neural_net(self, inputs, layers, activation_function):
        outputs = inputs #ekat outputit ovvat inputit tottakai koska niistä lähdetään
        for layer in layers: #käydään joka kerros läpi aina muokaten outputtia
            inputs = np.hstack([np.ones((outputs.shape[0],1)), outputs]) #lisätään 1 eteen että bias toimii
            print(inputs, layer)
            outputs = activation_function(inputs @ layer) #perus neuronin toiminta eli otetaan activation functio matriisiyhtälöstä
        
        return outputs
    
    def get_max_value(self, inputs):
        #suurin activaatio 
        outputs = self.neural_net(
            np.array([inputs]), 
            [self.layer1_w, self.o_layer_w], 
            self.activation_func_sigmoid)
        return np.max(outputs), outputs


    #modifointifunktiot alkaa

    def modify_weights(self): #mutate molemmat layerit käskettäessä
        NNet.mutate_array(self.layer1_w)
        NNet.mutate_array(self.o_layer_w)
        #huom palautuksia ei tarvia koska noiden sisällä annetaan readwrite lupa muokata listoja

    def create_mixed_weights(self, net1, net2):#mixaa netit tarvittaessa
        self.layer1_w = NNet.get_mix_from_arrays(net1.layer1_w, net2.layer1_w)
        self.o_layer_w = NNet.get_mix_from_arrays(net1.o_layer_w, net2.o_layer_w)


    #def mutate_array(a):
     #   for x in np.nditer(a, op_flags=['readwrite']): #käy läpi jokaisen painon arrayssa
      #      if random.random() < MUTATION_W_CHANGE: #jos luku 0-1 on pienempi kuin 0.2
       #         x[...] = np.random.random_sample() - 0.5 #muokataan sitä kai jotenkin en nyt ihan ymmär, tulos jotain -0.5 ja 0-5 väliltä
   
  #  def get_mix_from_arrays(ar1: np.matrix, ar2: np.matrix) -> np.matrix:
   #     total_entries = ar1.size #otetaan yhteinen koko ekast
    #    #yhteinen muoto ekasta
     #   num_rows = ar1.shape[0]
      #  num_cols = ar1.shape[1]

       # num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX) #otetaan puolet(eli puolet miinus puolet)
      #  idx = np.random.choice(np.arange(total_entries), num_to_take, False) #ottaa luodusta arange listasta num to take määrän indexejä

        #res = np.random.rand(num_rows, num_cols) #luodaan satunnainen tyhjä array oikeaa kokoa

        #for row in range(0, num_rows):
         #   for col in range(0, num_cols):
          #      index = row * num_cols + col #lasketaan index jos matriisi olisi flättättynä

           #     res[row][col] = ar1[row][col] if index in idx else ar2[row][col] #jos flättätty arvo arvotuissa arvoissa ota ekasta, muuten tokasta

        #return res #palauta mixi

    def print_weights(self):
        print('Tassa', self.layer1_w, self.o_layer_w, sep='\n')


def tests():
    nnet = NNet(16, 5, 2)
    print('layer1', nnet.layer1_w)
    print('outputlayer', nnet.o_layer_w)

    inputs = [0.2, 1, 2,5,3,6,3,2,66,10,22,1,21,12,53,21]
    output = nnet.get_max_value(inputs)
    print('output',output)

if __name__ == '__main__':
    tests()
