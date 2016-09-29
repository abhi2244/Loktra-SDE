'''
Created on 28-Sep-2016

@author: abhishek
'''
import re

def get_domain(url):
    re_3986_enhanced = re.compile(r"""
        ^                                    # anchor to beginning of string
        (?:  (?P<scheme>    [^:/?#\s]+): )?  # capture optional scheme
        (?://(?P<authority>  [^/?#\s]*)  )?  # capture optional authority
             (?P<path>        [^?#\s]*)      # capture required path
        (?:\?(?P<query>        [^#\s]*)  )?  # capture optional query
        (?:\#(?P<fragment>      [^\s]*)  )?  # capture optional fragment
        $                                    # anchor to end of string
        """, re.MULTILINE | re.VERBOSE)
    re_domain =  re.compile(r"""
        # Pick out top two levels of DNS domain from authority.
        (?P<domain>[^.]+\.[A-Za-z]{2,6})  # $domain: top two domain levels.
        (?::(?P<port>[0-9]*))?                      # port number.
        $                                 # Anchor to end of string.
        """, 
        re.MULTILINE | re.VERBOSE)
    domain = ""
    query=""
    path=""
    scheme=""
    auth=""
    fragment=""
    port=""
    m_uri = re_3986_enhanced.match(url)
    if m_uri and m_uri.group("fragment"):
        fragment=m_uri.group("fragment") 
    else:
        fragment="No Fragment" 
    if m_uri and m_uri.group("scheme"):
        scheme=m_uri.group("scheme")
    else:
        scheme="No scheme"  
    if m_uri and m_uri.group("path"):
        path=m_uri.group("path") 
    else:
        path="No Path" 
    if m_uri and m_uri.group("query"):
        query=m_uri.group("query") 
    else:
        query="No Query"
    if m_uri and m_uri.group("authority"):
        auth = m_uri.group("authority")
        m_domain = re_domain.search(auth)
        if m_domain and m_domain.group("domain"):
            domain = m_domain.group("domain");
        else:
            domain="No Domain"
        if m_domain and m_domain.group("port"):
            port = m_domain.group("port");
        else:
            port="Default port 80"

    print "Scheme: "+scheme        
    print "Authority: "+auth
    print "Domain: "+domain
    print "Port: "+port
    print "Fragment: "+fragment
    print "Query: "+query
    print "Path: "+path
    print ""
    
url=raw_input()  
get_domain(url)