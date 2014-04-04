import subprocess as s
import argparse as a
import sys

parser = a.ArgumentParser(description='Migrate a Xen instance from one host to another.')
parser.add_argument('diskpath', metavar='disk path', help='path to the domU\'s disk image')
parser.add_argument('swappath', metavar='swap path', help='path to the domU\'s swap image')
parser.add_argument('configpath', metavar='config path', help='path to the xen config file')
parser.add_argument('targetuser', metavar='user', help='username on target system')
parser.add_argument('targetip', metavar='ip', help='ip or hostname of target system')
parser.add_argument('targetdir', metavar='dir', help='target directory')

args = parser.parse_args()

diskpath = args.diskpath
swappath = args.swappath
configpath = args.configpath
targetuser = args.targetuser
targetip = args.targetip
targetdir = args.targetdir

# Attempts to copy the xen config from arg specified location
# to /tmp/config.xen

print "copying config from %s to /tmp" % configpath
string = "cp %s /tmp/config.xen" % configpath

try:
	s.check_output(string,shell=True)
except Exception, e:
	print "Couldn't do it: %s" % e
	sys.exit(0)

# Attempts to DD the disk image from specified loc to /tmp

string = "dd if=%s of=/tmp/tempdisk.xen" % diskpath
print "dd from %s to /tmp, please wait" % diskpath

try:
	print s.check_output(string,shell=True)
except Exception, e:
	print "Couldn't do it: %s" % e
	sys.exit(0)

string = "dd if=%s of=/tmp/swapdisk.xen" % swappath
print "dd from %s to /tmp, please wait" % swappath

try:
	print s.check_output(string,shell=True)
except Exception, e:
	print "Couldn't do it: %s" % e
	sys.exit(0)

# Initiates SCP to other host and copies as per the stuff you input

string = "scp /tmp/*.xen %s@%s:%s" % (targetuser, targetip, targetdir)
print "scping data from /tmp to %s please wait" % targetip

try:
	print s.check_output(string,shell=True)
except Exception, e:
	print "Couldn't do it: %s" % e
	sys.exit(0)

# Clean up that mess!

print "success, deleting temporary images"

try:
	s.check_output("rm /tmp/*.xen",shell=True)
except Exception, e:
	print "Couldn't do it: %s" % e
	sys.exit(0)

	print "removed, done."

