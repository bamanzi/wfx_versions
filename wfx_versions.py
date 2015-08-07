
import os
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

def check_version(line):
    parts=line.split('|')

    if len(parts)<=5: return

    s_name = parts[0]
    s_url_home = parts[1] if len(parts)>7 else ""
    s_url_download = parts[2] if len(parts)>7 else ""
    
    s_url_check = parts[-5]
    s_anchor  = parts[-4]
    s_before  = parts[-3]
    s_after   = parts[-2]
    s_version = parts[-1].strip()

    print "%s %20s %s..." % (CL_BOLD, s_name, CL_RESET) ,
    if s_anchor=="" and s_before=="":
        print CL_RED + "error: both @start and @before are empty." + CL_RESET
        return

    if s_after=="":
        print CL_RED + "error: empty @after." + CL_RESET
        return

    o = urllib.urlopen(s_url_check)
    content = o.read()
    if s_anchor<>'':
        pos = content.find(s_anchor)
        if pos > 0:
            content = content[pos+len(s_anchor):]
        else:
            print CL_RED + "error in @start: '%s' not found" % (s_anchor) + CL_RESET
            return

    if s_before<>'':
        pos = content.find(s_before)
        if pos > 0:
            content = content[pos+len(s_before):]
        else:
            print CL_RED + "error in @before: '%s' not found" % (s_before) + CL_RESET
            return

    pos = content.find(s_after)
    if pos > 0:
        content = content[:pos].strip()
        if content != s_version:
            content = CL_GREEN + content + CL_RESET
        print "%20s => %s" % (s_version, content)
    else:
        print CL_RED + "error in @after: '%s' not found" % (s_after) + CL_RESET
        return
            


if __name__ == "__main__":
    import sys
    #line="""!bang selection|https://addons.mozilla.org/en-US/firefox/addon/bang-selection/?src=search|version item|id="version-|"|0.3"""
    #check_version(line)        
    for line in file("temp.list"):
        try:
            check_version(line)
        except:
            print CL_RED + "error: %s" % sys.exc_info()[0] + CL_RESET
