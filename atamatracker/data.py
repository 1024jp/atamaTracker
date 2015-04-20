"""data structure module
"""

import csv


# setup csv format
csv.register_dialect('result', delimiter='\t', lineterminator='\n')


class TrackPoint(object):
    """Tracked point data struct.

    Public properties:
    position -- [Point] Tracked/clicked position
    identifier -- [int] Index number
    time -- [float] Clicked time
    is_manual -- [bool] Whether the point was clicked manually
    """

    __slots__ = ['time', 'identifier', 'position', 'is_manual']

    def __init__(self, position, identifier, time, is_manual=False):
        self.position = position
        self.time = time
        self.identifier = identifier
        self.is_manual = is_manual


class History(list):
    """List of TrackPoint objects.
    """

    def dump(self, file_path):
        """Create a result CSV file at the given path.

        file_path -- [str] Path to result file
        """
        f = open(file_path, 'wb')
        writer = csv.writer(f, dialect='result')
        for point in self:
            writer.writerow([
                '{}'.format(point.time),
                point.identifier,
                point.position.y,
                point.position.x
            ])
        f.close()
