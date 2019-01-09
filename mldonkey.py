import sys
import re
import urllib
from telnetlib import Telnet


class MLDonkeyException(Exception):
    pass


class MLDonkeyError(Exception):
    pass


class MLDonkey:
    "Inteface to Mldonkey server"

    def __init__(self, mlIp, mlPort, mlUser, mlPass):
        self.ip = mlIp
        self.port = mlPort
        self.user = mlUser
        self.passw = mlPass
        try:
            self._start_session()
        except Exception as e:
            self.quit()
            raise

    def __enter__(self):
        self.clean_searches()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.clean_searches()
        self.quit()

    def _start_session(self):
        self.session = Telnet(self.ip, self.port, 2)
        self.session.read_until("MLdonkey command-line", 2)
        self._run_command("auth {} {} \n".format(self.user, self.passw))

    def _run_command(self, command):
        self.session.write(command)
        out = self.session.read_until("MLdonkey command-line")
        if "Command not authorized" in out or "No such command" in out \
           or "Bad login/password" in out:
            raise MLDonkeyException("MLDonkeyException: {}".format(out))
        return out

    def quit(self):
        if hasattr(self, 'session'):
            self.session.write('quit')
            self.session.close()

    def add_link(self, link):
        """
        Add a ed2k link to mldonkey server
        """
        output = self._run_command("dllink {} \n".format(urllib.unquote(link)))

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
            raise MLDonkeyError("Unexpected error: {}".format(sys.exc_info()[0]))

        return result

    def clean_searches(self):
        searches = self.get_searches()
        for s in searches:
            self._run_command(" forget {} \n".format(s[0]))

    def run_search(self, links):
        """
        Search for a strings in mldonkey server
        """
        for s in links:
            self._run_command(" s \"{}\" \n".format(s))

    def download_search(self, search_index):
        """
        Add a ed2k link to mldonkey server
        """
        if search_index:
            res = 0
            try:
                page = self._run_command(" vr {} \n".format(int(search_index)))
                page = page.replace("\r", '')
            except Exception as e:
                raise MLDonkeyError("Unexpected error: {}".format(sys.exc_info()[0]))

            regexp = re.compile("\[[ ]*(\d*)\].*")
            result = regexp.findall(page)
            if len(result) == 0:
                res = "No results"
            else:
                for file_index in result:
                    page = self._run_command(" d {} \n".format(int(file_index)))
        else:
            res = "No search_index param"

        return res
