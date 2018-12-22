import commands
import sys
import re
import time
import urllib
from telnetlib import Telnet


class MLDonkey:
    "Inteface to Mldonkey server"

    def __init__(self, mlIp, mlPort, mlUser, mlPass):
        self.ip = mlIp
        self.port = mlPort
        self.user = mlUser
        self.passw = mlPass
        self._start_session()

    def _start_session(self):
        try:
            self.session = Telnet(self.ip, self.port, 2)
            self.session.read_until("MLdonkey command-line", 2)
            self._run_command("auth %s %s \n" % (self.user, self.passw))
        except Exception as e:
            raise

    def _run_command(self, command):
        self.session.write(command)
        return self.session.read_until("MLdonkey command-line")

    def quit(self):
        self.session.write('quit')

    def add_link(self, link):
        """
        Add a ed2k link to mldonkey server
        """
        command = "printf \"auth %s %s \\n dllink %s \\n q \\n\" | nc -i1 %s %s" % (self.user,
                                                                                    self.passw,
                                                                                    urllib.unquote(link),
                                                                                    self.ip,
                                                                                    self.port)
        output = commands.getstatusoutput(command)
        print(output)
        if 'Added link' in output:
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
            page = self.session.read_until("MLdonkey command-line", 1)
            # [27   ]CONTAINS[Desperate.housewives.8x04.School.of.hard.knocks.HDTV.Xvid.V.O.Subtitulos.Integrados.avi]
            # -2 (found 1)
            page = page.replace("\r", '')
            regexp = re.compile("\[(\d*)[ ]*\][\(*]*CONTAINS\[(.*?)\].*\(found (\d*)\)")
            result = regexp.findall(page)

        except Exception as e:
            print("Unexpected error: {}".format(sys.exc_info()[0]))
            raise
        return result

    def clean_searches(self):
        searches = self.get_searches()
        for s in searches:
            self._run_command(" forget %s \n" % (s[0]))

    def run_search(self, links):
        """
        Add a ed2k link to mldonkey server
        """
        for s in links:
            self._run_command(" s \"%s\" \n" % s)
            time.sleep(32)

    def download_search(self, search_index):
        """
        Add a ed2k link to mldonkey server
        """
        if search_index:
            res = 0
            try:
                page = self._run_command(" vr %d \n" % int(search_index))
                page = page.replace("\r", '')
            except Exception as e:
                print("Unexpected error: {}".format(sys.exc_info()[0]))
                raise
            regexp = re.compile("\[[ ]*(\d*)\].*")
            result = regexp.findall(page)
            if len(result) == 0:
                res = "No results"
            else:
                for file_index in result:
                    page = self._run_command(" d %d \n" % int(file_index))
        else:
            res = "No search_index param"

        return res
