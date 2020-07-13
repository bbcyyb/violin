import logging

_log = logging.getLogger('di')


def _get_fqdn(cls):
    '''
    Returns a fully-qualified name of the fiven class
    '''
    return cls.__module__ + '.' + cls.__name__


_ctx = None


def get_ctx():
    global _ctx
    if _ctx is None:
        _ctx = Context()
    return _ctx


class Context(object):
    '''
    An IoC container for :func:`interface` s, :func:`service` s and :func:`component` s
    '''

    def __init__(self):
        self.service_instances = {}
        self.component_instances = {}

    def __repr__(self):
        return '[Context %s]' % id(self)

    def get_service(self, cls):
        fqdn = _get_fqdn(cls)
        if fqdn not in self.service_instances:
            self.service_instances[fqdn] = cls(self)
        return self.service_instances[fqdn]

    def get_component(self, cls):
        fqdn = _get_fqdn(cls)
        if fqdn not in self.component_instances:
            self.component_instances[fqdn] = cls(self)
        return self.component_instances[fqdn]

    def get_components(self, cls, ignore_exceptions=False):
        for comp in cls.implementations:
            try:
                instance = self.get_component(comp)
                yield instance
            except Exception as e:
                if ignore_exceptions:
                    _log.error('Could not instantiate %s: %s', cls, e)
                else:
                    raise


def service(cls):
    '''
    Marks the decorated class as a singleton ``service``.
    Injects following classmethods:
        .. py:method:: .get(context)
            Returns a singleton instance of the class for given ``context``
            :param context: context to look in
            :type context: :class:`Context`
            :returns: ``cls``
    '''

    if not cls:
        return None

    # Inject methods
    def _get(cls, context):
        return context.get_service(cls)

    cls.get = _get.__get__(cls)

    _log.debug('Registering [%s] (service)', _get_fqdn(cls))

    return cls


class NoImplementationError(Exception):
    def __init__(self, cls):
        self.cls = cls

    def __str__(self):
        return u'No implementation for [%s] is available' % self.cls.__name__

    def __repr__(self):
        return str(self)


def interface(cls):
    '''
    Marks the decorated class as an abstract interface.
    Injects following classmethods:
        .. py:method:: .all(context) 
            Returns a list of instances of each component in the ``context`` implementing this ``@interface``
            :param context: context to look in
            :type context: :class:`Context`
            :returns: list(``cls``)
        .. py:method:: .any(context)
            Returns the first suitable instance implementing this ``@interface`` or raises :exc:`NoImplementationError` if none is available.
            :param context: context to look in
            :type context: :class:`Context`
            :returns: ``cls``
        .. py:method:: .classes()
            Returns a list of classes implementing this ``@interface``
            :returns: list(class)
    '''

    if not cls:
        return None

    cls.implementations = []

    # Inject methods
    def _all(cls, context, ignore_exceptions=False):
        return list(context.get_components(cls, ignore_exceptions=ignore_exceptions))
    cls.all = _all.__get__(cls)

    def _any(cls, context):
        instances = cls.all(context)
        if instances:
            return instances[0]
        raise NoImplementationError(cls)
    cls.any = _any.__get__(cls)

    def _classes(cls):
        return list(cls.implementations)
    cls.classes = _classes.__get__(cls)

    _log.debug('Registering [%s] (interface)', _get_fqdn(cls))

    return cls


def component(iface):
    '''
    Marks the decorated class as a component implementing the given ``iface``
    :param iface: the interface to implement
    :type iface: :func:`interface`
    '''

    def decorator(cls):
        if not cls:
            return None

        # Run custom verificator if any
        if hasattr(cls, '__verify__'):
            if not cls.__verify__():
                return None

        if not hasattr(iface, 'implementations'):
            _log.error('%s is not an @interface', iface)

        _log.debug(
            'Registering [%s] (implementation of [%s])' % (
                _get_fqdn(cls),
                _get_fqdn(iface)
            )
        )
        iface.implementations.append(cls)

        def _get(cls, context):
            return context.get_component(cls)
        cls.get = _get.__get__(cls)

        return cls

    return decorator