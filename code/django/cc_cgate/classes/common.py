from common.classes import *
from cc_cgate.classes import *
from cc_cgate.models import *

class Event:

  def Track(self, table_name, table_id, event_data):

    # adds a record to track events
    o = {}
    o['table_name'] = table_name;
    o['table_id'] =  table_id;
    o['event_data'] = event_data;

    event = TrackedEvent(**o)
    event.save()

    return 'tracked:'



