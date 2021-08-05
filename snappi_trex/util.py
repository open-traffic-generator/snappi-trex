class Util:
    """
    This class contains miscellaneous utility functions
    """

    @staticmethod
    def get_mask(bits):
        """
        returns a mask of 1's of size bits
        """
        result = (1 << bits) - 1
        return result

    
    @staticmethod
    def uint_to_int(uint, size):
        """
        converts an unsigned int of size n to a signed int of size n
        """
        result = uint & Util.get_mask(size)
        if result >= (1 << (size-1)):
            result -= (1 << size)
        return result


    @staticmethod
    def convert_to_long(value, layer_type):
        """
        Parses address values into a long int
        args:
            - value: A string or long representing the address
            - layer_type: A string representing the layer type
        """
        if isinstance(value, int): 
            return value

        if layer_type == 'IP':
            elements = value.split('.')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e)
            return result

        if layer_type == 'Ethernet':
            elements = value.split(':')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e, 16)
            return result

        if layer_type == 'IPv6':
            elements = value.split(':')
            result = 0
            for e in elements:
                result = result << 16
                if len(e) == 0:
                    continue
                result += int(e, 16)
            return result

        if layer_type == 'ARP':
            if len(value.split('.')) == 4:
                return Util.convert_to_long(value, 'IP')
            elif len(value.split(':')) == 6:
                return Util.convert_to_long(value, 'Ethernet')
            else:
                raise SyntaxError()
        
        return value

    
    @staticmethod
    def long_to_MAC(value):
        return ':'.join(['{}{}'.format(a,b)
            for a, b in zip(*[iter('{:012x}'.format(value))] * 2)
        ])


    @staticmethod
    def list_not_empty(key, obj):
        return key in obj and obj[key] is not None and len(obj[key]) > 0