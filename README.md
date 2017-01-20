# trac-slack-plugin

Plugin to announce Trac changes in [Slack](https://slack.com/) service.


## Installation

Requirements:

    Requests library: https://pypi.python.org/pypi/requests
    $ pip install requests

Deploy to a specific Trac environment:

    $ cd /path/to/pluginsource
    $ python setup.py bdist_egg
    $ cp dist/*.egg /path/to/projenv/plugins

Enable plugin in trac.ini:

    [components]
    slack_notification.* = enabled

Configuration in trac.ini for ticket notificaitons:

    [slack]
    webhook = <Your Webhook Address>
    channel = #Trac
    username = Trac-Bot
    fields = type,component,resolution

Configuration in trac.ini for wiki notifications:

    [slack]
    wiki-webhook = <Your Webhook Address>
    wiki-channel = #TracWiki
    wiki-username = Trac-Bot
    wikiadd = 1           ; 0 = off, 1 = on; defaults to 1
    wikidel = 1           ; 0 = off, 1 = on; defaults to 1
    wikichange = 0        ; 0 = off, 1 = on; defaults to 0
    wikipages = .*        ; when wikichange is on, regex to use to see if we should notify on the change; defaults to everything (.*)


Thanks to Sebastian Southen for his work with the Irker Notification!


## License

Copyright (c) 2014, Sebastian Southen  
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in
   the documentation and/or other materials provided with the
   distribution.
3. The name of the author may not be used to endorse or promote
   products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR `AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
