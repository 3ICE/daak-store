from textwrap import wrap
class BogusSMTPConnection(object):
  """Instead of sending emails, print them to the console."""

  def __init__(*args, **kwargs):
    print("Initialized bogus SMTP connection")

  def open(self):
    print("Open bogus SMTP connection")

  def close(self):
    print("Close bogus SMTP connection")

  def send_messages(self, messages):
    print("Sending through bogus SMTP connection:")
    for message in messages:
      print("tFrom: %s" % message.from_email)
      print("tTo: %s" % ", ".join(message.to))
      print("tSubject: %s" % message.subject)
      print("t%s" % "nt".join(wrap(message.body)))
      print(messages)
      return len(messages)