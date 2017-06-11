import copy
import logging

from geometry_utils import Point3D
from src.Exceptions import BinTooSmallException


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
        self.space_left = self.get_size()
        self._zigzag_marker = copy.copy(self.anchor_point)  # bottom
        self._cuboid_marker_y = self.anchor_point.y + size_y - 1  # top
        self.layer_size = size_x * size_z
        self._cuboid_space_left_in_last_layer = 0
        self._cuboid_marker_x = self.anchor_point.x

    def __eq__(self, other):
        return self.anchor_point == other.anchor_point and self.size_x == other.size_x and self.size_y == other.size_y and self.size_z == other.size_z

    def __cmp__(self, other):
        return self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

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

    def fill_in(self, job_queue, cluster):
        """
        puts the first job from the list into the cluster
        :raises BinTooSmallException: when the job is too big
        :param job_queue: JobQueue
        :return: None
        """
        logging.info('FILLING BIN: {} size: {}'.format(self, self.get_size()))
        while True:
            next_job = job_queue.peek_at_first_job()
            job_size = next_job.nodes_needed
            if job_size > self.space_left:
                raise BinTooSmallException
            strategy = self._get_filling_strategy(next_job)
            strategy(next_job, cluster)
            job_queue.pop_first()

    def _move_zig_zag_marker(self):
        if self._zigzag_marker.x >= self.anchor_point.x + self.size_x - 1:  # already at the border along x axis
                                                                            # will try to move along z axis
            self._zigzag_marker = Point3D(self.anchor_point.x,  # need to return caret along x axis
                                          self._zigzag_marker.y,
                                          self._zigzag_marker.z)
            if self._zigzag_marker.z >= self.anchor_point.z + self.size_z - 1:  # already at the border along z axis
                                                                                # will try to move along y axis
                self._zigzag_marker = Point3D(self._zigzag_marker.x,  # need to return caret along z axis
                                              self._zigzag_marker.y,
                                              self.anchor_point.z)
                if self._zigzag_marker.y >= self.anchor_point.y + self.size_y - 1 \
                        or self._zigzag_marker.y >= self._cuboid_marker_y - 1:  # already at the border along y axis
                                                                                # or colliding with cuboid marker
                    raise BinTooSmallException
                else:
                    self._zigzag_marker = Point3D(self._zigzag_marker.x,
                                                  self._zigzag_marker.y + 1,  # can be moved.
                                                  self._zigzag_marker.z)
            else:
                self._zigzag_marker = Point3D(self._zigzag_marker.x,
                                              self._zigzag_marker.y,
                                              self._zigzag_marker.z + 1)  # can be moved.
        else:
            self._zigzag_marker = Point3D(self._zigzag_marker.x + 1,  # can be moved.
                                          self._zigzag_marker.y,
                                          self._zigzag_marker.z)

    def _get_filling_strategy(self, job_to_fill):
        """
        chooses the right strategy for the given job, and runs it.
        :return: None
        """
        if job_to_fill.comm_sensitive:
            return self._zig_zag_strategy
        else:
            return self._cuboid_strategy

    def _zig_zag_strategy(self, job, cluster):
        node_list = []
        for nodes_needed in xrange(job.nodes_needed):
            node_list.append(copy.copy(self._zigzag_marker))
            self.space_left -= 1
            self._move_zig_zag_marker()

        job.posess_nodes(node_list, self)

    def _cuboid_strategy(self, job, cluster):
        node_list = []

        if job.nodes_needed <= self._cuboid_space_left_in_last_layer:  # use the layer which was splitted last
            columns_needed = (job.nodes_needed / self.size_z) + 1
            for x in xrange(self._cuboid_marker_x, self._cuboid_marker_x + columns_needed):
                for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                    node_list.append(Point3D(x, self._cuboid_marker_y, z))

            self._cuboid_space_left_in_last_layer -= columns_needed * self.size_z
            self._cuboid_marker_x += columns_needed
            if self._cuboid_space_left_in_last_layer <= 0:
                self._cuboid_marker_x = self.anchor_point.x
                self._cuboid_space_left_in_last_layer = 0
                self._cuboid_marker_y -= 1

        else:

            height_needed = int(job.nodes_needed / self.layer_size) + 1
            height_available = self._cuboid_marker_y - self._zigzag_marker.y

            if height_needed > height_available:
                raise BinTooSmallException

            if height_needed == 1:  # chance to split layer between multiple communication sensitive jobs
                if self._cuboid_space_left_in_last_layer != 0:  # abandon splitted layer, was too small apparently
                    self._cuboid_marker_x = self.anchor_point.x
                    self._cuboid_space_left_in_last_layer = 0
                    self._cuboid_marker_y -= 1

                columns_needed = (job.nodes_needed / self.size_z) + 1
                for x in xrange(self.anchor_point.x, self.anchor_point.x + columns_needed):
                    for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                        node_list.append(Point3D(x, self._cuboid_marker_y, z))

                self._cuboid_marker_x = self.anchor_point.x
                self._cuboid_marker_x += columns_needed
                self._cuboid_space_left_in_last_layer = self.layer_size - columns_needed * self.size_z
                if self._cuboid_space_left_in_last_layer <= 0:
                    self._cuboid_marker_x = self.anchor_point.x
                    self._cuboid_space_left_in_last_layer = 0
                    self._cuboid_marker_y -= 1

            else:
                if self._cuboid_space_left_in_last_layer != 0:  # abandon splitted layer, will be found as bin.
                    self._cuboid_marker_x = self.anchor_point.x
                    self._cuboid_space_left_in_last_layer = 0
                    self._cuboid_marker_y -= 1

                for x in xrange(self.anchor_point.x, self.anchor_point.x + self.size_x):
                    for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                        for y in xrange(self._cuboid_marker_y - height_needed + 1, self._cuboid_marker_y + 1):
                            node_list.append(Point3D(x, y, z))

                self._cuboid_marker_y -= height_needed
                self._cuboid_marker_x = self.anchor_point.x
                self._cuboid_space_left_in_last_layer = 0

        job.posess_nodes(node_list, self)
