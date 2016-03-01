filename = 'filedownsample.txt'
answer1 = []
with open(filename, 'r+') as d:
	answer1 = d.readlines()
d.close()
answer2 = []

for i in answer1:
	answer2.append(i.rstrip('\n'))

pat = []


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

count = 32
t = 0
while(1):
	if count == len(answer2)-1:
		break;
	if answer2[count] == " 0" or answer2[count] == " 7":
                t = t + 1
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

print t

