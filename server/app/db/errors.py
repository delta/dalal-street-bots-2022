"""Utility errors to check if the user"""

RecordNotFound = Exception("Record Not found")
InternalServer = Exception("Internal server error")
DuplicateKey = Exception("Duplicate key error")

# TODO: create a type of a error, eg for DuplicateKey Error,
# we shd be able to duplicate field  id
# eg, "Bot with name=ExampleBot already exists"
