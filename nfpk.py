import sys, argparse
import re, csv
import time
from math import log
import numpy as np
import pprint

np.set_printoptions(precision=6)

p = argparse.ArgumentParser(description = 'compute similarity of records across 2 files')
p.add_argument('db', type=argparse.FileType('r'), help='database CSV')
p.add_argument('aux', type=argparse.FileType('r'), help='auxiliary info CSV')

args = p.parse_args()
print args

def filter_comments(stream):
    '''filter #-marked comments to end of line'''
    for l in stream:
	l = re.sub(r'\s*#.*$', '', l)
	if len(l):
	    yield l

r_db = csv.DictReader(filter_comments(args.db))
r_aux = csv.DictReader(filter_comments(args.aux))

#
# Map comparable columns to each other
#
db_to_aux = {
    'age': 'dob'
    , 'home town': 'home town'
}

aux_to_db = {}
for _ in db_to_aux:
    aux_to_db[db_to_aux[_]] = _

# A list of the comparable columns, for convenient iteration...
cmp_cols = db_to_aux.keys()
n_cmp_cols = len(cmp_cols)
# ...plus a map from comparable aux columns back to indices
aux_cmp_cols = {}
for i in range(n_cmp_cols):
    aux_cmp_cols[db_to_aux[cmp_cols[i]]] = i


def not_null(a):
    return a not in ('', None)

# Map a db col to the fn that can compare it with an aux col
sim_cols = {
    'age': lambda a, b: int(not_null(a) and not_null(b) and
                            int(a) == int((time.time()
                                           - time.mktime(time.strptime(b, '%d %b %Y')))
                                          /60/60/24/365))
    , 'home town': lambda a, b: int(a == b)
}
rows = {}
for which, csv_r in (('db', r_db), ('aux', r_aux)):
    rows[which] = []
    for row in csv_r:
        print which + ':',
        for f in row:
            print f + '=' + row[f] + "\t",
        print ''
        rows[which].append(row)

print ''
pp = pprint.PrettyPrinter()
pp.pprint(rows)

print ''
pp.pprint(sim_cols)

def supp(r):
    return [_ for _ in r if not_null(r[_])]

def supp_(r_):
    return [_ for _ in db_to_aux.values() if not_null(r_[_])]

r = {1: 1, 2: 2, 3: None}
print 'supp(' + str(r) + ') -', supp(r)

print ''
for r_ in rows['aux']:
    print r_, supp_(r_)
print ''

def r_i(r, i):
    '''
    Return i_th comparable column in r,
    as a tuple of (column-name, column-value).

    r is assumed to be a row from db.
    '''
    col_r = cmp_cols[i]
    return (col_r, r[col_r])

def r__i(r_, i):
    '''
    Return i_th comparable column in r_,
    as a tuple of (column-name, column-value).

    r is assumed to be a row from aux.
    '''
    col_r = cmp_cols[i]
    col_r_ = db_to_aux[col_r]
    return (col_r_, r_[col_r_])

def sim_i(r, r_, i):
    r = r_i(r, i)
    r_ = r__i(r_, i)
    #print "sim_i(" + str(r) + ",", str(r_) + "):", sim_cols[r[0]](r[1], r_[1])
    return sim_cols[r[0]](r[1], r_[1])

def min_sim_i(r, r_):
    #return min([sim_i(r, r_, i) for i in range(n_cmp_cols)])
    return min([sim_i(r, r_, aux_cmp_cols[_]) for _ in supp_(r_)])

#def supp(r):
#    return [_ for _ in r if not_null(r[_])]

def sim(r, r_):
    sum = 0.0
    for i in range(n_cmp_cols):
        sum += sim_i(r, r_, i)

    supp_r = supp(r)
    supp_r_ = [aux_to_db[_] for _ in supp_(r_)]
    mag_u = len(set(supp_r) | set(supp_r_))
    return sum / mag_u

## From http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
def memoize(f):
    '''Memoization decorator for a function taking a single argument'''
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

@memoize
def mag_supp_db_i(i):
    '''return magnitude of the support of the ith column in db'''
    return float(len([_ for _ in rows['db'] if not_null(r_i(_, i)[1])]))

print ''
for i in range(n_cmp_cols):
    print "supp(" + str(i) + "=" + cmp_cols[i] + ") =", mag_supp_db_i(i)

def de_anon(db, aux, score, match = lambda s: s >= 0.5, dist = lambda D_: [1.0/len(D_) for _ in D_]):
    '''De-anonimize r, a row in db, wrt all rows in aux'''
    D_ = [(r, score(r, aux)) for r in db if match(score(r, aux))]
    pdf = dist(D_) if len(D_) > 0 else []
    return [D_[i] + (pdf[i],) for i in range(len(D_))]

def alg_1a(db, aux, alpha = .7):
    return [de_anon(db, r_, min_sim_i, lambda s: s >= alpha) for r_ in aux]

def alg_1b(db, aux, phi=.2):
    @memoize
    def wt(i):
	return 1 / np.log(mag_supp_db_i(i))
    def score(r, aux):
	supp_aux_i = [aux_cmp_cols[_] for _ in supp_(aux)]	# determine supp(aux) as indices
	return sum([wt(i)*sim_i(r, aux, i) for i in supp_aux_i])

    m = []
    for r_ in aux:
	S = np.array([score(r, r_) for r in db])
	max2, max = np.argsort(S)[-2:]
	print S
	if (S[max] - S[max2])/np.std(S) > phi:
	    m.append((db[max],))
	else:
	    m.append(())
    return m

print ''
first = True
for row_db in rows['db']:
    if not first: print ''
    for row_aux in rows['aux']:
        print 'sim(' + str(row_db)
        print '    , ' + str(row_aux) + ') -', sim(row_db, row_aux), min_sim_i(row_db, row_aux)

alg_1a.name = 'Algorithm 1A'
alg_1b.name = 'Algorithm 1B'
for a in (alg_1a, alg_1b):
    print "\n---", a.name, '---'
    identified = zip(rows['aux'], a(rows['db'], rows['aux']))
    first = True
    for r_, m in identified:
	if not first:
	    print ''
	print r_
	for _ in m:
	    print "\t", _
	first = False
