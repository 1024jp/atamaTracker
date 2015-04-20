"""data structure module
"""

import csv


# setup csv format
csv.register_dialect('result', delimiter='\t', lineterminator='\n')


class TrackPoint(object):
    """Tracked point data struct.

    Public properties:
    position -- [Point] Tracked/clicked position
    label -- [int] Index number
    time -- [float] Clicked time
    is_manual -- [bool] Whether the point was clicked manually
    """

    __slots__ = ['time', 'label', 'position', 'is_manual']

    def __init__(self, position, label, time, is_manual=False):
        self.position = position
        self.time = time
        self.label = label
        self.is_manual = is_manual

    def __str__(self):
        return "TrackPoint(({pos.x}, {pos.y}), {label}, {time})".format(
            pos=self.position,
            label=self.label,
            time=self.time,
        )


class History(list):
    """List of TrackPoint objects.
    """

    def point(self, time, idenfifier):
        matches = self.points(time=time, label=label)

        if len(matches) > 0:
            return matches[0]
        else:
            return None

    def points(self, time=None, label=None):
        """Filter with given properties.
        """
        matches = []
        for point in self:
            if ((time is None or point.time == time) and
                    (label is None or point.label == label)):
                matches.append(point)

        return matches

    def sort(self, **kwargs):
        # override default sort key
        if not ('key' in kwargs):
            kwargs['key'] = lambda p: (p.time, p.label)

        super(History, self).sort(**kwargs)

    def dump(self, file_path):
        """Create a result CSV file at the given path.

        file_path -- [str] Path to result file
        """
        f = open(file_path, 'wb')
        writer = csv.writer(f, dialect='result')
        for point in self:
            writer.writerow([
                '{}'.format(point.time),
                point.label,
                point.position.y,
                point.position.x
            ])
        f.close()
