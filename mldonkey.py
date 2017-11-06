
import commands
import sys
import re
import time
import urllib
from telnetlib import Telnet
DEBUG = True

class MLDonkey:
    "Inteface to Mldonkey server"

    def __init__(self, mlIp, mlPort, mlUser, mlPass):
        self.ip = mlIp
        self.port = mlPort
        self.user = mlUser
        self.passw = mlPass
        try:
            self.session = Telnet(mlIp, mlPort,2)
            self.session.read_until("MLdonkey command-line",2)
            self.run_command("auth admin add95c \n")
        except:
            raise

    def run_command(self, command):
        self.session.write(command)
        return self.session.read_until("MLdonkey command-line")

    def quit(self):
        self.session.write('quit')

    def add_link(self, link):
        """
        Add a ed2k link to mldonkey server
        """
        global DEBUG
        if not DEBUG:
        	print "Fake call to mldonkey server ==> %s " % link
        else:
       	    command = "printf \"auth admin add95c \\n dllink %s \\n q \\n\" | nc -i1 %s %s" % (urllib.unquote(link), self.ip, self.port)
            output = commands.getstatusoutput(command)
            print output
    	    if 'Added link' in  output:
	        return "Link added"
       	    elif 'File is already shared in incoming/files' in output:
	        return "Link is already shared in incoming/files"
	    elif 'File is already in download queue of' in output:
	        return "File is already in download queue"
	    else:
	        return output

    def get_searches(self):
	self.session.write("vs \n")
	try:
	    page = self.session.read_until("MLdonkey command-line",1)
	    #[27   ]CONTAINS[Desperate.housewives.8x04.School.of.hard.knocks.HDTV.Xvid.V.O.Subtitulos.Integrados.avi]  -2 (found 1)
	    regexp = re.compile("\[(\d*)[ ]*\][\(*]*CONTAINS\[(.*?)\].*\(found (\d*)\)")
            page = page.replace("\r",'')

	    result = regexp.findall(page)

        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        return result

    def clean_searches(self):
        searches = self.get_searches()
        for s in searches:
            self.run_command(" forget %s \n" % (s[0]))

    def run_search(self, links):
        """
        Add a ed2k link to mldonkey server
        """
        for s in links:
            self.run_command(" s \"%s\" \n" % s)
            time.sleep(32)

    def download_search(self, search_index):
        """
        Add a ed2k link to mldonkey server
        """
	if search_index:
		res = 0
		try:
			page = self.run_command(" vr %d \n" % int(search_index))
			page = page.replace("\r",'')
	        except:
        		print "Unexpected error:", sys.exc_info()[0]
		    	raise
		regexp = re.compile("\[[ ]*(\d*)\].*")
		result = regexp.findall(page)
		if len(result) == 0:
			res = "No results"
		else:
			for file_index in result:
				page = self.run_command(" d %d \n" % int(file_index))
	else: 
		res = "No search_index param"

	return res

