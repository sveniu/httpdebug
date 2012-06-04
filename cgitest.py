#!/usr/bin/python

# Simple proof of concept cgi script to demonstrate selective request
# debugging based on environment variables. In this case we have
# Apache's mod_rewrite map client HTTP headers to environment
# variables, which are then used to determine debug output to syslog:
#
#   X-Debug-Level (\d+) -> XDEBUGLEVEL=$1
#   X-Debug-Key (\S+)   -> XDEBUGKEY=$1
#   X-Varnish (\d+)     -> XDEBUGXID=$1
#   X-Debug-Xid (\d+)   -> XDEBUGXID=$1
#
# Notes:
# * XDEBUGLEVEL corresponds to the syslog severity/level (0 to 7).
# * We trust Apache to unset the env vars if the key doesn't match.
# * This example uses some PostgreSQL-specific 'EXPLAIN ANALYZE'
# * This example uses Linux-specific grandparent pid code.
# * There's currently no discerning of debug levels.

import os
import sys
import time
import syslog
import resource
import psycopg2

t_start = time.time()

XID = os.getenv('XDEBUGXID')
if not XID:
    XID = '-'

try:
    DEBUGLEVEL = int(os.getenv('XDEBUGLEVEL'))
except TypeError:
    DEBUGLEVEL = -1

sys.stdout.write('Content-type: text/html\n\n')

# On each request, Apache does a fork and then runs the input filter
# as a child process of that forked process. To point back to the
# origin Apache pid, we need the grand parent of our own pid.
# Unfortunately, this needs Linux-specific code.
# Source: http://stackoverflow.com/a/1732073
def pnid(pid=None, N=1):
    "Get parent (if N==1), grandparent (if N==2), ... of pid (or self if not given)"
    if pid is None:
        pid= "self"
    while N > 0:
        filename= "/proc/%s/status" % pid
        with open(filename, "r") as fp:
            for line in fp:
                if line.startswith("PPid:"):
                    _, _, pid= line.rpartition("\t")
                    pid= pid.rstrip() # drop the '\n' at end
                    break
            else:
                raise RuntimeError, "can't locate PPid line in %r" % filename
        N-= 1
    return int(pid) # let it fail through

def dbgopen():
    if DEBUGLEVEL >= 0:
        syslog.openlog('cgi', logoption=syslog.LOG_PID,
                facility=syslog.LOG_USER)
def dbgclose():
    if DEBUGLEVEL >= 0:
        syslog.closelog()
def dbg(level, msg):
    if level <= DEBUGLEVEL:
        syslog.syslog(level, msg)

dbgopen()

dbg(7, 'req(%s): %s:%s -> %s:%s, debuglevel=%s, pppid=%d' % \
        (
            XID,
            os.getenv('REMOTE_ADDR'),
            os.getenv('REMOTE_PORT'),
            os.getenv('SERVER_ADDR'),
            os.getenv('SERVER_PORT'),
            os.getenv('XDEBUGLEVEL'),
            pnid(N=2),
        ))

dbg(7, 'req(%s): %s %s://%s%s%s %s, script_filename=%s' % \
        (
            XID,
            os.getenv('REQUEST_METHOD'),
            'https' if os.getenv('HTTPS') else 'http',
            os.getenv('REMOTE_USER')+'@' if os.getenv('REMOTE_USER') else '',
            os.getenv('SERVER_NAME'),
            os.getenv('REQUEST_URI'),
            os.getenv('SERVER_PROTOCOL'),
            os.getenv('SCRIPT_FILENAME'),
        ))

# Some simple Postgres-specific SQL.
def runquery(q):
    dbg(7, 'req(%s): SQL query: %s' % (XID, q))
    cur.execute('explain analyze ' + query)
    for r in cur.fetchall():
        dbg(7, 'req(%s): SQL analyze: %s' % (XID, r[0]))
    cur.execute(query)

dbname='cgi'
dbuser='cgi'
dbpass='mydbpass'
dbg(7, 'req(%s): Connecting to db, dbname=%s, dbuser=%s' % \
        (
            XID,
            dbname,
            dbuser,
        ))
conn = psycopg2.connect("dbname=%s user=%s password=%s" % \
        (dbname, dbuser, dbpass))
cur = conn.cursor()
query = 'select * from hits'
runquery(query)
cur.fetchall()
cur.close()
conn.close()

t_end = time.time()

dbg(7, 'req(%s): Wall clock elapsed: %.6f' % (XID, t_end-t_start))
dbg(7, 'req(%s): %s' % (XID, resource.getrusage(resource.RUSAGE_SELF)))

dbgclose()
