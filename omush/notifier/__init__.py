"""Provide a PubSub type object called Notifier.

Notifier is an object that must be instantiated instead of just using a global
pubsub. The reason is that we may want to have multiple notifiers or multiple
instances of the same game running on the same server. This will allow us to
keep them seperate.

A Notifier instance should be kept on the Game object.
"""
from pubsub import pub


class Notifier(object):
    """PubSub wrapper class that will allow containered pubsub.

    PubSub is used beneath this wrapp. We simply take the "topic" passed in
    to subscribe and notify, and add the id() of this instance as a prefix,
    and then pass through to pub.

    Notifier.subscrube(someMethod, "myTopic") will call
    pub.subscrube(someMethod, "22142154-myTopic").

    Where 22142154 is the id() of this instance.
    """

    def _transcribe_topic(self, topic):
        """Transcribe topic to a unique topic for this instance."""
        topic = "-".join([str(id(self)), topic])
        return topic

    def subscribe(self,
                  method=None,
                  topic=None):
        """Subscribe a method to a topic for notifications."""
        topic = self._transcribe_topic(topic)
        pub.subscribe(method, topic)

    def notify(self, topic, **kwargs):
        """Notify all listening methods of a specific topic."""
        topic = self._transcribe_topic(topic)
        pub.sendMessage(topic, **kwargs)
