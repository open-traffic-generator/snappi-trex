class Link(object):

    def __init__(self, trexclient):
        self._client = trexclient
        self._link_states = {}


    def set_link(self, payload, port_ids):
        ports = list(range(len(port_ids)))
        if payload.port_names is not None and len(payload.port_names) > 0:
            ports = []
            for p_name in payload.port_names:
                ports.append(port_ids.index(p_name))

        if payload.state == 'up':
            self._client.set_port_attr(ports=ports, link_up=True)
        elif payload.state == 'down':
            self._client.set_port_attr(ports=ports, link_up=False)
        
        for p in ports:
            self._link_states[p] = payload.state


    def is_up(self, port_id):
        return port_id not in self._link_states or self._link_states[port_id] == 'up'