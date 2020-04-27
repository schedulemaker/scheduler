# scheduler
Generates schedules based on class times, avoiding conflicts

Sample test event JSON for use in the Lambda console:
```
{
  "courses": [
    "SCTC-1001",
    "CIS-1001",
    "CIS-1051"
  ],
  "campuses": [
    "MN",
    "AMB"
  ]
}
```
## Unit testing 

* Create a file "api_keys.json" in unittests folder and add the following keys with your values.

    - aws_access_key_id
    - aws_secret_access_key
    - aws_function_name

* CD to unittests folder and run "test.py"
