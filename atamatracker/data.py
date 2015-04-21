"""data structure module
"""

import csv


# setup csv format
csv.register_dialect('result', delimiter='\t', lineterminator='\n')


class Track(object):
    """Tracked point data struct.

    Public properties:
    point -- [Point] Tracked/clicked point position
    label -- [int] Index number
    time -- [float] Clicked time
    is_manual -- [bool] Whether the point was clicked manually
    """

    __slots__ = ['time', 'label', 'point', 'is_manual']

    def __init__(self, point, label, time, is_manual=False):
        self.point = point
        self.time = time
        self.label = label
        self.is_manual = is_manual

    def __str__(self):
        return "Track(({point.x}, {point.y}), {label}, {time})".format(
            point=self.point,
            label=self.label,
            time=self.time,
        )


class History(list):
    """List of Track objects.
    """

    def track(self, time, idenfifier):
        matches = self.trasks(time=time, label=label)

        if len(matches) > 0:
            return matches[0]
        else:
            return None

    def tracks(self, time=None, label=None):
        """Filter with given properties.
        """
        matches = []
        for track in self:
            if ((time is None or track.time == time) and
                    (label is None or track.label == label)):
                matches.append(track)

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
        for track in self:
            writer.writerow([
                '{}'.format(track.time),
                track.label,
                track.point.y,
                track.point.x
            ])
        f.close()
