#!/usr/bin/python

import os
import sys
import urllib

CL_BOLD  = "\033[1m"
CL_RESET = "\033[0m"
CL_RED   = "\033[31m"
CL_BLUE  = "\033[33m"
CL_GREEN = "\033[32m"

# spec:
#   name|url_home|url_download|url_check|anchor_str|before_str|after_str|version
# or
#   name|url_check|anchor_str|before_str|after_str|version

# reverse spec
#   |name|url_home|url_download|url_check|anchor_str|before_str|after_str|version
# 1. search backward for anchor_str
# 2. continue search backward for after_str (result=>pos_end)
# 3. continue search backward for before_str (result=>pos_start)
# 4. slice content between pos_start:pos_end

def print_error(msg):
    print CL_RED + msg + CL_RESET
    
def check_version(line):
    parts=line.split('|')

    if len(parts)<=5:
        if line[0]=="#":
            print "%s %s %s" % (CL_BOLD, line, CL_RESET)
        return

    if line[0]=='|':
        b_reverse = True
        s_name = parts[1]
    else:
        b_reverse = False
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

    #print("reading %s" % s_url_check)
    o = urllib.urlopen(s_url_check)
    content = o.read()

    if not b_reverse:
        #import pdbpp
        #pdbpp.set_trace()
        if s_anchor<>'':
            pos = content.find(s_anchor)
            if pos > 0:
                content = content[pos+len(s_anchor):]
            else:
                print_error("@anchor: '%s' not found" % (s_anchor) )
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
    else:
        if s_anchor<>'':
            pos = content.rfind(s_anchor)
            if pos > 0:
                content = content[0:pos]
            else:
                print_error("@anchor: '%s' not found" % (s_anchor) )
                return
        
        if s_after<>'':
            pos = content.rfind(s_after)
            if pos > 0:
                content = content[0:pos]
            else:
                print_error("@after: '%s' not found" % (s_after) )
                return

        pos = content.rfind(s_before)
        if pos > 0:
            content = content[pos+len(s_before):].strip()
            if content != s_version:
                content = CL_GREEN + content + CL_RESET
            print "%20s => %s" % (s_version, content)
        else:
            print_error("@before: '%s' not found" % (s_before) )
            return
        


if __name__ == "__main__":
    #line="""!bang selection|https://addons.mozilla.org/en-US/firefox/addon/bang-selection/?src=search|version item|id="version-|"|0.3"""
    #line="""|PaleMoon raspi|http://raspi.palemoon.org/||http://raspi.palemoon.org/latest/|application|filedesc">|</TD><TD>|10/01/2016 14:06:30"""
    #check_version(line)

    # usage
    #    ./wfx_versions.py
    #          check new version of softwares listed in data/temp.list
    #    ./wfx_version.py regexp
    #          check new version of softwares (in data/*.list) whose name match /regexp/
    if len(sys.argv)==1:
        print "%s %s %s" % (CL_BOLD, "checking list in temp.list", CL_RESET)
        for line in file("data/temp.list"):
            try:
                check_version(line)
            except Exception as e:
                #print_error("%s" % sys.exc_info()[0])
                print_error("%s" % e)
    
    else:
        import re
        re1 = re.compile(sys.argv[1], re.I)
        from glob import glob
        for fn in glob("data/*.list"):
            for line in file(fn):
                parts=line.split('|')
                if (len(parts)>2) and (re1.search(parts[0]) or re1.search(parts[1])):
                    try:
                        print "%s === %s === %s" % (CL_BOLD, fn, CL_RESET)
                        check_version(line)
                    except Exception as e:
                        #print_error("%s" % sys.exc_info()[0])
                        print_error("%s" % e)   
