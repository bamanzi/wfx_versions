
import os
import sys
import urllib

CL_BOLD  = "\033[1m"
CL_RESET = "\033[0m"
CL_RED   = "\033[31m"
CL_BLUE  = "\033[34m"
CL_GREEN = "\033[32m"

# spec:
#   name|url_home|url_download|url_check|anchor_str|before_str|after_str|version
# or
#   name|url_check|anchor_str|before_str|after_str|version

def print_error(msg):
    print CL_RED + msg + CL_RESET
    
def check_version(line):
    parts=line.split('|')

    if len(parts)<=5:
        if line[0]=="#":
            print "%s %s %s" % (CL_BOLD, line, CL_RESET)
        return

    s_name = parts[0]
    s_url_home = parts[1] if len(parts)>7 else ""
    s_url_download = parts[2] if len(parts)>7 else ""
    
    s_url_check = parts[-5]
    s_anchor  = parts[-4]
    s_before  = parts[-3]
    s_after   = parts[-2]
    s_version = parts[-1].strip()

    print "%s %30s %s..." % (CL_BLUE, s_name, CL_RESET) ,
    sys.stdout.flush()
    if s_url_check.strip() == "":
        print_error("@url_check is empty.")
        return
    
    if s_anchor=="" and s_before=="":
        print_error("both @start and @before are empty." )
        return

    if s_after=="":
        print_error("empty @after." )
        return

    o = urllib.urlopen(s_url_check)
    content = o.read()
    if s_anchor<>'':
        pos = content.find(s_anchor)
        if pos > 0:
            content = content[pos+len(s_anchor):]
        else:
            print_error("@start: '%s' not found" % (s_anchor) )
            return

    if s_before<>'':
        pos = content.find(s_before)
        if pos > 0:
            content = content[pos+len(s_before):]
        else:
            print_error("@before: '%s' not found" % (s_before) )
            return

    pos = content.find(s_after)
    if pos > 0:
        content = content[:pos].strip()
        if content != s_version:
            content = CL_GREEN + content + CL_RESET
        print "%20s => %s" % (s_version, content)
    else:
        print_error("@after: '%s' not found" % (s_after) )
        return
            


if __name__ == "__main__":
    #line="""!bang selection|https://addons.mozilla.org/en-US/firefox/addon/bang-selection/?src=search|version item|id="version-|"|0.3"""
    #check_version(line)        
    for line in file("temp.list"):
        try:
            check_version(line)
        except Exception as e:
            #print_error("%s" % sys.exc_info()[0])
            print_error("%s" % e)
