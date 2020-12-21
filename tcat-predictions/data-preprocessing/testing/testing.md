* test01: 2nd JSON is complete duplicate of 1st JSON
    - expected: 1 JSON
* test02: only 'StartDate' field is modified, so 2nd JSON is NOT duplicate of 1st
    - expected: 2 JSONs
* test03: change 'Time' of first 'Arrival' in 'stop_time_updates' of 1st JSON
    - expected: 2 JSONs