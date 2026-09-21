"""
Publisher start-up/shutdown and RPC calls, called explicitly by jukebox.daemon (no plugin system).

This is the first component started and the last stopped: Hello/Goodbye publish messages live here.
"""

import logging
import jukebox
import jukebox.registry as registry
import jukebox.publishing as pub

logger = logging.getLogger('jb.pub')


def republish(topic=None):
    """Re-publish the topic tree 'topic' to all subscribers

    :param topic: Topic tree to republish. None = resend all"""
    pub.get_publisher().resend(topic)


def register():
    registry.register(republish, name='republish', package='publishing')


def start():
    pub.get_publisher().send('core.welcome', 'Welcome! Let the sound begin')
    pub.get_publisher().send('core.version', jukebox.version())


def stop(**ignored_kwargs):
    logger.debug("Closing publisher")
    pub.get_publisher().send('core.welcome', 'Goodbye. Hear you later!')
