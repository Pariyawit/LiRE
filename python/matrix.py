import numpy

P = numpy.array([[1,1,0,0],
	[0,1,1,0],
	[0,0,1,1],
	[0,0,0,1]])

Pt = P.T

print P 
print '------------------------'
print Pt
print '------------------------'
L = numpy.dot(P,Pt)
print L
print '------------------------'
L = numpy.dot(L,L.T)
print L
print '------------------------'
L = numpy.dot(L,L.T)
print L