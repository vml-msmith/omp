import unittest
from omush.notifier import Notifier

class ListenerObject(object):
    def __init__(self):
        self.listener_calls = 0
        self.arg1 = None
        self.arg2 = None

    def listener_method(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.listener_calls = self.listener_calls + 1

class NotifierTest(unittest.TestCase):
    def test_notifier_can_subscribe_and_notify(self):
        notifier = Notifier()
        my_object = ListenerObject()
        notifier.subscribe(method=my_object.listener_method,
                           topic='listenerTopic')
        self.assertEquals(my_object.listener_calls, 0)
        notifier.notify(topic='listenerTopic',
                        arg1='a1',
                        arg2='a2')
        self.assertEquals(my_object.listener_calls, 1)
        self.assertEquals(my_object.arg1, 'a1')
        self.assertEquals(my_object.arg2, 'a2')

    def test_notifier_does_not_add_to_reference_count(self):
        notifier = Notifier()
        my_object = ListenerObject()
        import gc
        notifier.subscribe(method=my_object.listener_method,
                           topic='listenerTopic')
        self.assertEquals(len(gc.get_referrers(my_object)), 1)

        my_object = None
        notifier.notify(topic='listenerTopic',
                        arg1='a1',
                        arg2='a2')

    def test_notifier_does_not_break_with_dead_objects(self):
        notifier = Notifier()
        my_object = ListenerObject()
        notifier.subscribe(method=my_object.listener_method,
                           topic='listenerTopic')
        my_object = None
        notifier.notify(topic='listenerTopic',
                        arg1='a1',
                        arg2='a2')

    def test_multiple_notifiers_dont_collide(self):
        notifier_1 = Notifier()
        notifier_2 = Notifier()
        my_object = ListenerObject()

        notifier_1.subscribe(method=my_object.listener_method,
                             topic='listenerTopic')
        self.assertEquals(my_object.listener_calls, 0)
        notifier_1.notify(topic='listenerTopic',
                        arg1='a1',
                        arg2='a2')
        notifier_2.notify(topic='listenerTopic',
                          arg1='a1',
                          arg2='a2')
        self.assertEquals(my_object.listener_calls, 1)


if __name__ == '__main__':
    unittest.main()
