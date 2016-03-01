import math
import random
import string
#from test1 import downsample

def downsample(a):
	answer_x = []
	answer_y = []
	for i in a:
		prev_ans = []
		for m in range(0,32,4):
			d = (i[m]+i[m+1]+i[m+2]+i[m+3])/4.0
			if d >= 0.5:
				prev_ans.append(1)
			else:
				prev_ans.append(0)
		answer_x.append(prev_ans)
	#print answer_x
	for i in range(len(answer_x[0])):
		prev_ans = []
		for m in range(0,32,4):
			d = (answer_x[m][i]+answer_x[m+1][i]+answer_x[m+2][i]+answer_x[m+3][i])/4.0
			if d >= 0.5:
				prev_ans.append(1)
			else:
				prev_ans.append(0)
		answer_y.append(prev_ans)
	final_answer = []
	for i in range(len(answer_y[0])):
		each = []
		for j in answer_y:
			each.append(j[i])
		final_answer.extend(each)
	
	return final_answer







class NN:
  def __init__(self, NI, NH, NO):
    # number of nodes in layers
    self.ni = NI + 1 # +1 for bias
    self.nh = NH
    self.no = NO
    
    # initialize node-activations
    self.ai, self.ah, self.ao = [],[],[]
    self.ai = [1.0]*self.ni
    self.ah = [1.0]*self.nh
    self.ao = [1.0]*self.no

    # create node weight matrices
    self.wi = makeMatrix (self.ni, self.nh)
    self.wo = makeMatrix (self.nh, self.no)

    # initialize node weights to random vals
    randomizeMatrix ( self.wi, -0.125, 0.125 )
    randomizeMatrix ( self.wo, -0.35, 0.35 )

    # create last change in weights matrices for momentum
    self.ci = makeMatrix (self.ni, self.nh)
    self.co = makeMatrix (self.nh, self.no)
    
    #print self.weights()
    
  def runNN (self, inputs):
    if len(inputs) != self.ni-1:
      print 'incorrect number of inputs'
    
    for i in range(self.ni-1):
      self.ai[i] = inputs[i]
      
    for j in range(self.nh):
      sum = 0.0
      for i in range(self.ni):
        sum +=( self.ai[i] * self.wi[i][j] )
      self.ah[j] = sigmoid (sum)
    
    for k in range(self.no):
      sum = 0.0
      for j in range(self.nh):        
        sum +=( self.ah[j] * self.wo[j][k] )
      self.ao[k] = sigmoid (sum)
      
    return self.ao
      
      
  
  def backPropagate (self, targets, N, M):
    # calc output deltas
    # we want to find the instantaneous rate of change of ( error with respect to weight from node j to node k)
    # output_delta is defined as an attribute of each ouput node. It is not the final rate we need.
    # To get the final rate we must multiply the delta by the activation of the hidden layer node in question.
    # This multiplication is done according to the chain rule as we are taking the derivative of the activation function
    # of the ouput node.
    # dE/dw[j][k] = (t[k] - ao[k]) * s'( SUM( w[j][k]*ah[j] ) ) * ah[j]
    output_deltas = [0.0] * self.no
    for k in range(self.no):
      error = targets[k] - self.ao[k]
      output_deltas[k] =  error * dsigmoid(self.ao[k]) 
   
    # update output weights
    for j in range(self.nh):
      for k in range(self.no):
        # output_deltas[k] * self.ah[j] is the full derivative of dError/dweight[j][k]
        change = output_deltas[k] * self.ah[j]
        self.wo[j][k] += N*change + M*self.co[j][k]
        self.co[j][k] = change

    # calc hidden deltas
    hidden_deltas = [0.0] * self.nh
    for j in range(self.nh):
      error = 0.0
      for k in range(self.no):
        error += output_deltas[k] * self.wo[j][k]
      hidden_deltas[j] = error * dsigmoid(self.ah[j])
    
    #update input weights
    for i in range (self.ni):
      for j in range (self.nh):
        change = hidden_deltas[j] * self.ai[i]
        #print 'activation',self.ai[i],'synapse',i,j,'change',change
        self.wi[i][j] += N*change + M*self.ci[i][j]
        self.ci[i][j] = change
        
    # calc combined error
    # 1/2 for differential convenience & **2 for modulus
    error = 0.0
    for k in range(len(targets)):
      error = 0.5 * (targets[k]-self.ao[k])**2
    return error
        
        
  def weights(self):
    print 'Input weights:'
    for i in range(self.ni):
      print self.wi[i]
    print
    print 'Output weights:'
    for j in range(self.nh):
      print self.wo[j]
    print ''
  
  def test(self, patterns):
    for p in patterns:
      inputs = p[0]
      print 'Inputs:', p[0], '-->', self.runNN(inputs), '\tTarget', p[1]
  
  def train (self, patterns, max_iterations = 1000, N=0.3, M=0.1):
    for i in range(max_iterations):
      for p in patterns:
        inputs = p[0]
        targets = p[1]
        self.runNN(inputs)
        error = self.backPropagate(targets, N, M)
      if i % 50 == 0:
        print 'Combined error', error
    self.test(patterns)
    self.weights()
    

def sigmoid (x):
  return math.tanh(x)
  
def dsigmoid (y):
  return 1 - y**2

def makeMatrix ( I, J, fill=0.0):
  m = []
  for i in range(I):
    m.append([fill]*J)
  return m
  
def randomizeMatrix ( matrix, a, b):
  for i in range ( len (matrix) ):
    for j in range ( len (matrix[0]) ):
      matrix[i][j] = random.uniform(a,b)

def main ():
  
	filename = 'filedownsample.txt'
	answer1 = []
	with open(filename, 'r+') as d:
		answer1 = d.readlines()
	d.close()
	answer2 = []
	
	for i in answer1:
		answer2.append(i.rstrip('\n'))
	
	pat = []
	count = 32
	while(1):
		if count == len(answer2)-1:
			break;
		if answer2[count] == " 0" or answer2[count] == " 7":
			a = []
			last = [0,1]
			if answer2[count] == " 0":
				last = [1,0]
			for i in range(32):
				a.append(map(int, list(answer2[count-i-1])))
			a.reverse()
        	        
			fo = []
			fo.append(downsample(a))
      			fo.append(last)
      			pat.append(fo)
		count += 33
	myNN = NN ( 64, 1, 2)
	myNN.train(pat)
  
  
if __name__ == "__main__":
    main()
