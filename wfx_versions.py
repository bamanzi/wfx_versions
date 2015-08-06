
import os
import urllib

# spec:
#   name|url_check|url_home|url_download|anchor_str|before_str|after_str|version
# or
#   name|url_check|anchor_str|before_str|after_str|version

def check_version(line):
    parts=line.split('|')

    if len(parts)<=5: return

    s_name = parts[0]
    s_url_check = parts[1]
    s_url_home = parts[2] if len(parts)>7 else ""
    s_url_download = parts[3] if len(parts)>7 else ""
    s_anchor  = parts[-4]
    s_before  = parts[-3]
    s_after   = parts[-2]
    s_version = parts[-1].strip()

    print "%20s..." % s_name ,
    if s_anchor=="" and s_before=="":
        print "error: both @start and @before are empty."
        return

    if s_after=="":
        print "error: empty @after."
        return

    o = urllib.urlopen(s_url_check)
    content = o.read()
    if s_anchor<>'':
        pos = content.find(s_anchor)
        if pos > 0:
            content = content[pos+len(s_anchor):]
        else:
            print "error in @start: '%s' not found" % (s_anchor)
            return

    if s_before<>'':
        pos = content.find(s_before)
        if pos > 0:
            content = content[pos+len(s_before):]
        else:
            print "error in @before: '%s' not found" % (s_before)
            return

    pos = content.find(s_after)
    if pos > 0:
        content = content[:pos]
        print "%20s => %s" % (s_version, content)
    else:
        print "error in @after: '%s' not found" % (s_after)
        return
            


if __name__ == "__main__":
    import sys
    #line="""!bang selection|https://addons.mozilla.org/en-US/firefox/addon/bang-selection/?src=search|version item|id="version-|"|0.3"""
    #check_version(line)        
    for line in file("temp.list"):
        try:
            check_version(line)
        except:
            print "error: %s" % sys.exc_info()[0]
