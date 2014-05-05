import numpy

P = numpy.array([[0]*3]*3)

Pt = P.T
P[0][0] = 1
P[0][1] = 1
print P 
print '------------------------'
print Pt

print '--------1---------------'
L = numpy.dot(P,Pt)
M = P.dot(Pt)
print L
print M

print '--------2---------------'
L = numpy.dot(L,L.T)
M = M*M.T
print L
print M

print '--------3---------------'
L = numpy.dot(L,L.T)
M = M*M.T
print L
print M

print '--------4---------------'
L = numpy.dot(L,L.T)
M = M*M.T
print L
print M