import json
import requests
import re
from trac.core import *
from trac.config import Option, IntOption
from trac.wiki.api import IWikiChangeListener

#def wiki_page_added(self, page):
#def wiki_page_changed(self, page, version, t, comment, author, ipnr):
#def wiki_page_deleted(self, page):
#def wiki_page_version_deleted(self, page):

def prepare_wiki_values(page, action=None):
    values = dict([('project', page.env.project_name.encode('utf-8').strip()), 
                   ('action', action), ('pagename', page.name),
                   ('url', page.env.abs_href.wiki(page.name))]) 
    #values['project'] = page.env.project_name.encode('utf-8').strip()
    #values['action'] = 'changed'
    #values['pagename'] = page.name
    #values['url'] = page.env.abs_href.wiki(page.name)
    return values

class SlackWikiNotificationPlugin(Component):
    implements(IWikiChangeListener)
    webhook = Option('slack', 'wiki-webhook', 'https://hooks.slack.com/services/', doc="Incoming webhook for Slack")
    channel = Option('slack', 'wiki-channel', '#TracWiki', doc="Channel name on Slack")
    username = Option('slack', 'wiki-username', 'Trac-Bot', doc="Username of the bot on Slack notify")
    wikiadd = IntOption('slack', 'wikiadd', '1', doc=" Turn add notification on or off (defaults on)")
    wikidel = IntOption('slack', 'wikidel', '1', doc="Turn delete notification on or off (defaults on)")
    wikichange = IntOption('slack', 'wikichange', '0', doc="Turn change notification on or off (defaults off)")
    wikipages = Option('slack', 'wikipages', '.*', doc="Regex of wiki pages to notify on change of")
 
    def notify(self, values):
        template = '_%(project)s_ :incoming_envelope:\n%(pagename)s[%(url)s] was *%(action)s* by @%(author)s'

        if (values['action'] == 'deleted'):
            template = '_%(project)s_ :X:\n%(pagename)s[%(url)s] was *%(action)s*'

        # make sure author formatting is correct...
        if (values['author'])
            values['author'] = re.sub(r' <.*', '', values['author'])

        # format the message
        message = template % values

        # set type-specific attachements as needed
        attachments = []

        if (values['action'] == 'changed' and values['comment']):
            attachments.append( { ':pushpin: title': 'Comment', 'text': values['comment'] } )

        # send it all out
        data = { 
            "channel": self.channel,
            "username": self.username,
            "text": message.encode('utf-8').strip(),
            "attachments": attachments
        }

        try:
            r = requests.post(self.webhook, data={"payload":json.dumps(data)})
        except requests.exceptions.RequestException as e:
            self.log.exception("Failed to post slack notification: %s" % (e))
            return False
        return True

    def wiki_page_added(self, page):
        if (self.wikiadd != 1):
            pass

        # otherwise we're enabled so move forward with notification...
        values = prepare_wiki_values(page, 'added')
        values['author'] = page.author
        values['comment'] = page.comment
        self.notify(values)

    def wiki_page_deleted(self, page):
        if (self.wikidel != 1):
            pass

        # otherwise we're enabled so move forward with notification...
        values = prepare_wiki_values(page, 'deleted')
        values['url'] = page.env.abs_href.wiki(page.name)
        values['author'] = page.author  # this is usually going to be blank here...
        self.notify(values)

    def wiki_page_changed(self, page, version, t, comment, author, ipnr):
        if (self.wikichange != 1):
            pass

        # otherwise we're enabled so move forward with notification...
        #wikipagelist = self.wikipages.split(',')
        #for wikipage in wikipagelist:
            #wikipage.strip()
        if (re.match(self.wikipages, page.name)):
            # setup the values and notify!
            values = prepare_wiki_values(page, 'changed')
            values['author'] = author
            values['comment'] = comment
            self.notify(values)
                #break # we're done here

    def wiki_page_version_deleted(self, page):
        pass
 
