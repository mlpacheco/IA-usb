import optparse
import random
import math

class NeuralNetwork(object):
	"""Clase que define la estructura de red neuronal"""
	def __init__(self,  num_inputs,  num_hidden,  num_outputs):
		#pesos de la red
		self.num_inputs = num_inputs
		self.num_hidden = num_hidden
		self.num_outputs = num_outputs
		
		self.wih = random_matrix(num_inputs, num_hidden, -1, 1)
		self.who = random_matrix(num_hidden, num_outputs, -1, 1)
		#vectores de activacion de las capaz hidden y output
		self.ah = [0.0]*num_hidden
		self.ao = [0.0]*num_outputs
		#los valores de 
		#self.A_wih = [[0.0]*num_hidden]*num_inputs
		#self.A_who = [[0.0]*num_outputs]*num_hidden

	def propagate_forward(self, inputs):

		for h in range(self.num_hidden):
			sum = 0.0
			for i in range(self.num_inputs):
				sum += inputs[i]*self.wih[i][h]
			self.ah[h] = sigmoid(sum)

		for o in range(self.num_outputs):
			sum = 0.0
			for h in range(self.num_hidden):
				sum+= self.ah[h]*self.who[h][o]
			self.ao[o] = sigmoid(sum)
		return self.ao

	def propagate_backward(self, targets, learning_rate):
		error_out = [0.0]*self.num_outputs
		for o in range(self.num_outputs):
			error_out[o] = self.ao[o]*(1 - self.ao[o])*(targets[o] - self.ao[o])

		error_hid = [0.0]*self.num_hidden

		for h in range(self.num_hidden):
			sum = 0.0
			for o in range(self.num_outputs):
				sum += self.who[h][o]*error_out[o]
			error_hid[h] = self.ah[h]*(1 - self.ah[h])*sum

		#actualizacion
		for i in range(self.num_inputs):
			for h in range(self.num_hidden):
				A_wih = learning_rate*error_hid[h]*self.ah[h]
				self.wih[i][h] = self.wih[i][h] + A_wih

		for h in range(self.num_hidden):
			for o in range(self.num_outputs):
				A_who = learning_rate*error_out[o]*self.ao[o]
				self.who[h][o] = self.who[h][o] + A_who

	def train(self, examples, learning_rate, max_iterations = 1000):

		for it in range(max_iterations):
			for e in examples:
				inputs = e[0]
				targets = e[1]
				self.propagate_forward(inputs)
				self.propagate_backward(targets,learning_rate)
		self.test(examples)

	def test(self,examples):
		for p in examples:
			print 'Inputs:', p[0], '-->', self.propagate_forward(p[0]), '\tTarget', p[1]




def sigmoid(x):
	return 1 / (1 + math.exp(-x))

def random_matrix(I,  J,  a,  b):
	matrix = []
	for i in range(I):
		fila = []
		for j in range(J):
			#inserta un elementos a la fila a insertar
			fila.append(random.uniform(a, b))
		#se inserta la fila en la matriz,  dandole la altura
		matrix.append(fila)
	return matrix

def main():
	# parse input options
	parser = optparse.OptionParser()
	parser.add_option('-n', help='number of hidden layer neurons', type='int', dest='num_hidden')
	parser.add_option('-l', help='learning rate', type='float', dest='learning_rate')	
	(opts, args) = parser.parse_args()
	mandatories = ['num_hidden', 'learning_rate']
	for m in mandatories:
		if not opts.__dict__[m]:
			print "Mandatory option missing"
			parser.print_help()
			exit(-1)

	xor = [
		[[0,0], [1]],
		[[0,1], [1]], 
		[[1,0], [1]],
		[[1,1], [0]]
	]
	network = NeuralNetwork(2,opts.num_hidden,1)
	network.train(xor, opts.learning_rate)

if __name__ == "__main__":
	main()