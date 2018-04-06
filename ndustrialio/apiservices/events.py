from ndustrialio.apiservices import *

class EventsService(Service):

    def __init__(self, client_id, client_secret=None):
        super(EventsService, self).__init__(client_id, client_secret)

    def baseURL(self):
        return 'https://events.api.ndustrial.io'

    def audience(self):
        return '7jzwfE20O2XZ4aq3cO1wmk63G9GzNc8j'


    '''
    Event Types
    '''

    '''
    getEventTypesForClient

    - client_id -- client id of the event type owner

    Retrieve event types for a certain client_id (usually the client_id of the worker that's using this function)

    Returns collection of event types
    '''
    def getEventTypesForClient(self, client_id, limit=1000, offset=0, execute=True):

        assert isinstance(client_id, str)

        params = {'limit': limit,
                  'offset': offset}

        return PagedResponse(self.execute(GET(uri='clients/{}/types'.format(client_id)).params(params), execute=execute))

    '''
    getEventTypes

    No parameters

    Retrieve all event types across all client owners.

    Returns collection of event types
    '''
    def getEventTypes(self, execute=True):

        return PagedResponse(self.execute(GET('types'), execute=execute))

    '''
    createEventType

    - name - Pretty name of the event type
    - description - Short description of the event type
    - client_id - client_id of the owner of this event type
    - slug - unique string for this event type
    - is_realtime_enabled (optional) - will this event type leverage realtime checking? If so, a definition will be used
    - level (optional) - Priority level of this event type

    Create a new event type. An event type is needed in order to create events and trigger those events

    Returns the created object
    '''
    def createEventType(self, name, description, client_id, slug, is_realtime_enabled=False, level=None, execute=True):

        assert isinstance(name, str)
        assert isinstance(description, str)
        assert isinstance(client_id, str)
        assert isinstance(slug, str)
        assert isinstance(is_realtime_enabled, bool)
        if level:
            assert isinstance(level, int)

        event_type_obj = {'name': name,
                          'description': description,
                          'client_id': client_id,
                          'slug': slug,
                          'is_realtime_enabled': is_realtime_enabled
                        }
        if level:
            event_type_obj['level'] = level

        return self.execute(POST(uri='types').body(event_type_obj)
                            .content_type(ApiRequest.URLENCODED_CONTENT_TYPE), execute=execute)


    '''
    Event Objects
    '''

    '''
    getEventsForType

    - event_type_id - ID of the event type

    Retrieve all event objects for an event type

    Returns collection of event objects
    '''
    def getEventsForType(self, event_type_id, limit=1000, offset=0, execute=True):

        assert isinstance(event_type_id, str)

        params = {'limit': limit,
                  'offset': offset}

        return PagedResponse(self.execute(GET(uri='types/{}/events'.format(event_type_id)).params(params), execute=execute))

    '''
    getEventsForClient

    - client_id - ID of the client to get event types for

    Retrieve all event objects for a particular client (based on the client_id from the event_type parent)

    Returns collection of event objects
    '''
    def getEventsForClient(self, client_id, execute=True):

        assert isinstance(client_id, str)

        return PagedResponse(self.execute(GET(uri='clients/{}/events'.format(client_id)), execute=execute))


    '''
    createEvent

    - event_type_id -- ID of the parent event_type object
    - organization_id - ID of the organization this event object belongs to
    - name - Pretty name of the event
    - facility_id (optional) - ID of the facility this event object belongs to

    Create an event object for an event type

    Returns created event object
    '''
    def createEvent(self, event_type_id, organization_id, name, is_public, allow_others_to_trigger=True, facility_id=None, execute=True):

        assert isinstance(event_type_id, str)
        assert isinstance(organization_id, str)
        assert isinstance(name, str)
        assert isinstance(is_public, bool)
        assert isinstance(allow_others_to_trigger, bool)
        if facility_id:
            assert isinstance(facility_id, int)

        event_obj = {'event_type_id': event_type_id,
                     'organization_id': organization_id,
                     'name': name,
                     'is_public': is_public,
                     'allow_others_to_trigger': allow_others_to_trigger
                     }

        if facility_id:
            event_obj['facility_id'] = facility_id

        return self.execute(POST(uri='events').body(event_obj)
                            .content_type(ApiRequest.URLENCODED_CONTENT_TYPE), execute=execute)

    '''
    getEvent

    - event_id - ID of the event

    Retrieve a particular event object

    Returns an event object
    '''
    def getEvent(self, event_id, execute=True):

        assert isinstance(event_id, str)

        return self.execute(GET(uri='events/{}'.format(event_id)), execute=execute)

    '''
    updateEvent

    - event_id - ID of the event

    Update an event object

    Returns nothing
    '''
    def updateEvent(self, event_id, execute=True):

        assert isinstance(event_id, str)

        return self.execute(PUT(uri='events/{}'.format(event_id)), execute=execute)

    '''
    deleteEvent

    - event_id - ID of the event

    Delete an event object

    Returns nothing
    '''
    def deleteEvent(self, event_id, execute=True):

        assert isinstance(event_id, str)

        return self.execute(DELETE(uri='events/{}'.format(event_id)), execute=True)


    '''
    Triggered Events
    '''

    '''
    triggerEvent

    - event_id - ID of the event
    - trigger_start_at -- Start of the triggered event
    - trigger_end_at (optional) -- End of the triggered event
    - data (dict, optional) -- Extra information to add to this trigger
    - fields (list, optional) -- Associated fields with this triggered event

    Create a triggered event for an event object. This is the basic mechanism to say that something happened and
    record the time range that it happened.

    Returns the created triggered event object
    '''

    def triggerEvent(self, event_id, trigger_start_at, trigger_end_at=None, data=None, fields=None, execute=True):

        assert isinstance(event_id, str)
        assert isinstance(trigger_start_at, datetime)

        body = {'trigger_start_at': str(trigger_start_at)}

        if trigger_end_at:
            assert isinstance(trigger_end_at, datetime)
            body['trigger_end_at'] = str(trigger_end_at)
        if data:
            assert isinstance(data, dict)
            body['data'] = data

        if fields:
            assert isinstance(fields, list)
            body['fields'] = fields

        return self.execute(POST(uri='/events/{}/trigger'.format(event_id)).body(body), execute=execute)

    '''
    getTriggeredEvents

    - event_id - ID of the event object

    Get a list of triggered events for a particular event object

    Returns a list of triggered events
    '''
    def getTriggeredEvents(self, event_id, limit=1000, offset=0, orderBy=None, reverseOrder=None, execute=True):

        assert isinstance(event_id, str)

        params = {'limit': limit,
                  'offset': offset}

        if orderBy:
            assert isinstance(orderBy, str)
            params['orderBy'] = orderBy

        if reverseOrder:
            assert isinstance(reverseOrder, bool)
            params['reverseOrder'] = reverseOrder

        return PagedResponse(self.execute(GET(uri='/events/{}/triggered'.format(event_id)).params(params), execute=execute))


    '''
    getTriggeredEvent

    - triggered_event_id - ID of the triggered event

    Get a particular triggered event

    Returns a single triggered event
    '''
    def getTriggeredEvent(self, triggered_event_id, execute=True):

        assert isinstance(triggered_event_id, str)

        return self.execute(GET(uri='triggered/{}'.format(triggered_event_id)), execute=execute)

    '''
    updateTriggeredEvent

    - triggered_event_id - ID of the triggered event
    - trigger_start_at -- Start of the triggered event
    - trigger_end_at (optional) -- End of the triggered event
    - data (dict, optional) -- Extra information to add to this trigger

    Update a particular triggered_event

    Returns nothing
    '''
    def updateTriggeredEvent(self, triggered_event_id, trigger_start_at=None, trigger_end_at=None, data=None, execute=True):

        assert isinstance(triggered_event_id, str)

        body = {}
        if trigger_start_at:
            assert isinstance(trigger_start_at, datetime)
            body['trigger_start_at'] = str(trigger_start_at)

        if trigger_end_at:
            assert isinstance(trigger_end_at, datetime)
            body['trigger_end_at'] = str(trigger_end_at)
        if data:
            assert isinstance(data, dict)
            body['data'] = data

        return self.execute(PUT(uri='triggered/{}'.format(triggered_event_id)).body(body), execute=execute)

    '''
    deleteTriggeredEvent

    - triggered_event_id - ID of the triggered event

    Delete a particular triggered_event
    '''
    def deleteTriggeredEvent(self, triggered_event_id, execute=True):

        assert isinstance(triggered_event_id, str)

        return self.execute(DELETE(uri='triggered/{}'.format(triggered_event_id)), execute=execute)


    '''
    getTriggeredEventsForField

    - field_id

    Get triggered events that are associated with a field

    Returns list of triggered events
    '''
    def getTriggeredEventsForField(self, field_id, execute=True):

        assert isinstance(field_id, int)

        return self.execute(GET(uri='fields/{}/triggered'.format(field_id)), execute=execute)

    '''
    TODO

    :: Subscriptions
    getEventSubscriptions
    createUserMobileNumber
    deleteUserMobileNumber
    subscribeUserToEvent
    unsubscribeUserFromEvent
    getUserSubscriptionInfo

    :: Definitions
    createEventDefinition
    getEventDefinition
    deleteEventDefinition

    :: Notifications
    createNotificationTemplate
    getNotificationTemplate
    addNotificationTemplateVariable
    createNotificationTemplateType

    '''


