from geometry_utils import Point3D


class Bin(object):
    def __init__(self, anchor_point, size_x, size_y, size_z):
        """
        :param anchor_point: Point3D
        :param size_x: Int
        :param size_y: Int
        :param size_z: Int
        :return: Bin
        """
        self.anchor_point = anchor_point
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return 'Bin: anchor point: {}, size_x: {}, size_y: {}, size_z: {}'.format(self.anchor_point,
                                                                                  self.size_x,
                                                                                  self.size_y,
                                                                                  self.size_z)

    def __repr__(self):
        return self.__str__()

    def get_size(self):
        """
        returns the cubic size of given bin
        :return: Int
        """
        return self.size_x * self.size_y * self.size_z

    def generate_point_nodes(self):
        """
        generates a list of all of the 3D points inside of this bin.
        :return: [3DPoint]
        """
        point_nodes = []
        for x in xrange(self.size_x):
            for y in xrange(self.size_y):
                for z in xrange(self.size_z):
                    point_nodes.append(Point3D(self.anchor_point.x + x,
                                               self.anchor_point.y + y,
                                               self.anchor_point.z + z))

        return point_nodes

    def fill_in(self, job_queue):
        pass  # TODO

