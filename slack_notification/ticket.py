import json
import requests
import re
from trac.core import *
from trac.config import Option, IntOption
from trac.ticket.api import ITicketChangeListener
#from trac.versioncontrol.api import IRepositoryChangeListener

def prepare_ticket_values(ticket, action=None):
        values = ticket.values.copy()
        values['id'] = "#" + str(ticket.id)
        values['action'] = action
        values['url'] = ticket.env.abs_href.ticket(ticket.id)
        values['project'] = ticket.env.project_name.strip()
        values['attrib'] = ''
        values['changes'] = ''
        return values

class SlackNotifcationPlugin(Component):
        implements(ITicketChangeListener)
        webhook = Option('slack', 'webhook', 'https://hooks.slack.com/services/',
                doc="Incoming webhook for Slack")
        channel = Option('slack', 'channel', '#Trac',
                doc="Channel name on Slack")
        username = Option('slack', 'username', 'Trac-Bot',
                doc="Username of the bot on Slack notify")
        fields = Option('slack', 'fields', 'type,component,resolution',
                doc="Fields to include in Slack notification")

        def notify(self, type, values):
                # values['type'] = type
                values['author'] = re.sub(r' <.*', '', values['author'])
                #template = u'%(project)s/%(branch)s %(rev)s %(author)s: %(logmsg)s'
                #template = u'%(project)s %(rev)s %(author)s: %(logmsg)s'
                template = '_%(project)s_ :incoming_envelope: \n%(type)s <%(url)s|%(id)s>: %(summary)s [*%(action)s* by @%(author)s]'

                attachments = []

                if values['action'] == 'closed':
                        template += ' :white_check_mark:'

                if values['action'] == 'created':
                        template += ' :pushpin:'

                if values['attrib']:
                        attachments.append({
                                'title': 'Attributes',
                                'text': values['attrib']
                        })

                if values.get('changes', False):
                        attachments.append({
                                'title': ':small_red_triangle: Changes',
                                'text': values['changes']
                        })

                # For comment and description, strip the {{{, }}} markers. They add nothing
                # of value in Slack, and replacing them with ` or ``` doesn't help as these
                # end up being formatted as blockquotes anyway.

                if values['description']:
                        attachments.append({
                                'title': 'Description',
                                'text': re.sub(r'({{{|}}})', '', values['description'])
                        })

                if values['comment']:
                        attachments.append({
                                'title': 'Comment:',
                                'text': re.sub(r'({{{|}}})', '', values['comment'])
                        })

                message = template % values

                data = {
                        "channel": self.channel,
                        "username": self.username,
                        "text": message.encode('utf-8').strip(),
                        "attachments": attachments
                }
                try:
                        r = requests.post(self.webhook, data={"payload":json.dumps(data)})
                except requests.exceptions.RequestException as e:
                        return False
                return True

        def ticket_created(self, ticket):
                values = prepare_ticket_values(ticket, 'created')
                values['author'] = values['reporter']
                values['comment'] = ''
                fields = self.fields.split(',')
                attrib = []

                for field in fields:
                        if ticket[field] != '':
                                attrib.append('\u2022 %s: %s' % (field, ticket[field]))

                values['attrib'] = "\n".join(attrib) or ''

                self.notify('ticket', values)

        def ticket_changed(self, ticket, comment, author, old_values):
                action = 'changed'
                if 'status' in old_values:
                        if 'status' in ticket.values:
                                if ticket.values['status'] != old_values['status']:
                                        action = ticket.values['status']
                values = prepare_ticket_values(ticket, action)
                values.update({
                        'comment': comment or '',
                        'author': author or '',
                        'old_values': old_values
                })

                if 'description' not in list(old_values.keys()):
                        values['description'] = ''

                fields = self.fields.split(',')
                changes = []
                attrib = []

                for field in fields:
                        if ticket[field] != '':
                                attrib.append('\u2022 %s: %s' % (field, ticket[field]))

                        if field in list(old_values.keys()):
                                changes.append('\u2022 %s: %s \u2192 %s' % (field, old_values[field], ticket[field]))

                values['attrib'] = "\n".join(attrib) or ''
                values['changes'] = "\n".join(changes) or ''

                self.notify('ticket', values)

        def ticket_deleted(self, ticket):
                pass

