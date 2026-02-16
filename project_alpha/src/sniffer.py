import threading
from scapy.all import sniff, conf
import logging

# Suppress verbose Scapy output
conf.verb = 0

logger = logging.getLogger(__name__)

class PacketSniffer:
    """
    threaded Packet Sniffer wrapper around Scapy.
    """
    def __init__(self, interface, callback=None):
        self.interface = interface
        self.callback = callback
        self.stop_event = threading.Event()
        self.thread = None

    def start(self):
        """Start sniffing in a background thread."""
        logger.info(f"Starting capturing on interface {self.interface}...")
        self.thread = threading.Thread(target=self._sniff_loop)
        self.thread.daemon = True
        self.thread.start()

    def _sniff_loop(self):
        try:
            # simple filter to avoid too much noise for this demo
            sniff(
                iface=self.interface,
                prn=self.callback,
                store=False,
                stop_filter=lambda x: self.stop_event.is_set()
            )
        except Exception as e:
            logger.error(f"Sniffing failed: {e}")

    def stop(self):
        """Stop the sniffer thread."""
        logger.info("Stopping capture...")
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=2.0)
