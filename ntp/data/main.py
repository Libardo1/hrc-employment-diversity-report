import time
from pprint import pprint
from ntp.data.init_db import rdb_timestamps, r, rdb_static
from ntp.data import etl, api


def create_timestamps(new_timestamp):
    """
    Insert a new timestamp value into rethinkdb
    """
    rdb_timestamps.insert(dict(id=new_timestamp)).run(r.connect())
    return True


def retrieve_data_for_insert(ntp_last_updated):
    """
    Handles all required data manipulations for importing open data portal data

    Takes in an epoch time value representing the last time the open data portal
    data was retrieved.
    """
   
    
    odp_last_updated = api.check_for_update()
   
    # 0 is the initial condition. See ntp.data.api.ntp_last_update()
    if ntp_last_updated == 0 or api.should_update(ntp_last_updated, odp_last_updated):

        if not ntp_last_updated:
            ntp_last_updated = int(time.time())

        # Raw data acquisition and cleaning
        raw_data = api.retrieve_data()
        sanitized_data = etl.return_sanitized(raw_data)
        
        # Actual data transformations needed for front end
        static_data = etl.prepare_static_data(sanitized_data)

        for out in static_data:
            out["date"] = ntp_last_updated

        temporal_data = etl.prepare_temporal_data(sanitized_data)
        out_bool = create_timestamps(ntp_last_updated) 
        assert out_bool
        return dict(static=static_data, temporal=temporal_data)

    return False


def run():
    """
    Primary entry point for data.main
    """
   
    last_updated = api.ntp_last_update() 

    pprint("Checking for new data...")  
    out = retrieve_data_for_insert(last_updated)

    if out:
        pprint("New data found")
        static = out.get("static")
        temporal = out.get("temporal")

        if static:
            pprint("Inserting static data")
            rdb_static.insert(static).run(r.connect())
            
    else:
        pprint("Up-to-date")

if __name__ == "__main__":
    run()
