ISSUES
- In schemas.py, the created_at for all schemas was set to a string, rather than a datetime object itself. Caused the request to fail (500 internal server error) because I was doing .datetime.today() on a field that required a string.

Logging issues and notes elsewhere