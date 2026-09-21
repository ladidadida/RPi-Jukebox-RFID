"""
Publisher start-up/shutdown and RPC calls, called explicitly by jukebox.daemon (no plugin system).

This is the first component started and the last stopped: Hello/Goodbye publish messages live here.
"""

import logging
import jukebox
import jukebox.cfghandler
import jukebox.registry as registry
import jukebox.publishing as pub

logger = logging.getLogger('jb.pub')
cfg = jukebox.cfghandler.get_handler('jukebox')

# Create the one global proxy server instance that handles client connections and Last-Value-Caching
_PUBLISH_SERVER_THREAD: pub.server.PublishServer


def republish(topic=None):
    """Re-publish the topic tree 'topic' to all subscribers

    :param topic: Topic tree to republish. None = resend all"""
    pub.get_publisher().resend(topic)


def register():
    registry.register(republish, name='republish', package='publishing')


def start():
    global _PUBLISH_SERVER_THREAD
    tcp_port = cfg.setndefault('publishing', 'tcp_port', value=5558)
    _PUBLISH_SERVER_THREAD = pub.server.PublishServer(tcp_port=tcp_port)
    _PUBLISH_SERVER_THREAD.start()
    pub.get_publisher().send('core.welcome', 'Welcome! Let the sound begin')
    pub.get_publisher().send('core.version', jukebox.version())


def stop(**ignored_kwargs):
    global _PUBLISH_SERVER_THREAD
    logger.debug("Closing publish server connection")
    pub.get_publisher().send('core.welcome', 'Goodbye. Hear you later!')
    pub.get_publisher().close_server()
    return _PUBLISH_SERVER_THREAD
