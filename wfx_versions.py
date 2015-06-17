
import os
import urllib


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
    s_version = parts[-1]

    if s_anchor=="" and s_before=="":
        print "%20s: error: both @start and @before are empty." % (s_name)
        return

    if s_after=="":
        print "%20s: error: empty @after." % (s_name)
        return

    o = urllib.urlopen(s_url_check)
    content = o.read()
    if s_anchor<>'':
        pos = content.find(s_anchor)
        if pos > 0:
            content = content[pos+len(s_anchor):]
        else:
            print "%20s: error in @start: '%s' not found" % (s_name, s_anchor)
            return

    if s_before<>'':
        pos = content.find(s_before)
        if pos > 0:
            content = content[pos+len(s_before):]
        else:
            print "%20s: error in @before: '%s' not found" % (s_name, s_before)
            return

    pos = content.find(s_after)
    if pos > 0:
        content = content[:pos]
        print "%20s: %20s => %20s" % (s_name, s_version, content)
    else:
        print "%20s: error in @after: '%s' not found" % (s_name, s_after)
        return
            


if __name__ == "__main__":
    #line="""!bang selection|https://addons.mozilla.org/en-US/firefox/addon/bang-selection/?src=search|version item|id="version-|"|0.3"""
    #check_version(line)        
    for line in file("firefox.list"):
        check_version(line)
