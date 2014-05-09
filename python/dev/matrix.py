import numpy
import Queue as Q
P = numpy.array([[0,2,0,1,3],[2,0,2,0,0],[0,2,0,0,0],[1,0,0,0,4],[3,0,0,4,0]])
B = numpy.array([0,1,0,1,0])
print B
print P 

N = P.dot(B)
print N

print '--------2---------------'

#P = numpy.asmatrix(P)
print P
P = P.dot(P.T)

numpy.savetxt("O.txt",P,fmt="%d",delimiter=",",newline="\n")
print "-----------------SAVE---"
M = numpy.loadtxt("O.txt",delimiter=",",dtype="int32")
#M = numpy.asmatrix(M)
print P
print M
"""
q = Q.PriorityQueue(maxsize=5)

q.put_nowait((0,"abcdd"))
print q.get()

for i in range(0,10):
	try:
		q.put_nowait((i,"abc"))
	except:
		tmp = q.get()
		print "--",i,tmp
		if tmp[0] > i:
			q.put_nowait(tmp)
		else:
			q.put_nowait((i,"abc"))
print "----------------------------"
while(q.qsize() > 0 ):
	print q.get(),q.qsize()

print "done"
"""