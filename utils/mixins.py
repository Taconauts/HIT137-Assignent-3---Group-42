# Small mixin used for multiple inheritance demo.
# Adds a simple timestamp method for provenance/debug.

class TimestampMixin:
    def stamp(self ):
        import datetime
        return datetime.datetime.now().isoformat(" ", "seconds" )
