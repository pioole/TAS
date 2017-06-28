import copy
import logging

from math import ceil

from geometry_utils import Point3D
from src.Exceptions import BinTooSmallException, BinNotEmptyException, BackfillJobPriorityException


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
        self._cuboid_marker_y = self.anchor_point.y + size_y  # top
        self.layer_size = size_x * size_z
        self._cuboid_space_left_in_last_layer = 0
        self._cuboid_marker_x = self.anchor_point.x
        self._cuboid_splitting = False
        self._zigzag_started = False
        self.small_job_spaces = []
        self.mid_job_spaces = []

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

    def check_if_empty(self, cluster):
        """
        debug function used to check if given bin is empty
        :param cluster:
        :return:
        """
        nodes = self.generate_point_nodes()
        for node in nodes:
            if cluster._node_matrix[node.x][node.y][node.z] != 0:
                logging.error('bin was not empty!')
                raise BinNotEmptyException

    def fill_in(self, job, cluster, max_length=0, no_cluster=False):
        """
        puts the job into the bin if possible
        :raises BinTooSmallException: when the job is too big
        :param job: Job
        :return: None
        """
        if job.work_time > max_length != -1:
            raise BackfillJobPriorityException

        job_size = job.nodes_needed
        if job_size > self.space_left:
            raise BinTooSmallException

        strategy = self._get_filling_strategy(job)
        strategy(job, cluster, no_cluster)

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
                        or (self._zigzag_marker.y >= self._cuboid_marker_y - 1):  # already at the border along y axis
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

    def _zig_zag_strategy(self, job, cluster, no_cluster):
        node_list = []
        if self._zigzag_marker.y >= self._cuboid_marker_y:
            raise BinTooSmallException

        if self._zigzag_started:
            self._move_zig_zag_marker()
        node_list.append(copy.copy(self._zigzag_marker))
        self._zigzag_started = True
        self.space_left -= 1
        for nodes_needed in xrange(job.nodes_needed - 1):
            self._move_zig_zag_marker()
            node_list.append(copy.copy(self._zigzag_marker))
            self.space_left -= 1

        if not no_cluster:
            job.posess_nodes(node_list)

    def count_internal_fragmentation(self, job_size):
        """
        only for cuboid allocation!
        :param job_size:
        :return:
        """
        best_small = self._get_best_fit_for_small_space(job_size)
        best_mid = self._get_best_fit_for_medium_space(job_size)

        if best_small is not None:
            return len(best_small) - job_size
        elif best_mid is not None:
            return len(best_mid) * self.size_z - job_size
        else:
            return job_size % self.layer_size

    def _get_best_fit_for_small_space(self, nodes_needed):
        fitting = [small_space for small_space in self.small_job_spaces if len(small_space) >= nodes_needed]
        try:
            return min(fitting, key=lambda space: len(space))
        except ValueError:
            return None

    def _get_best_fit_for_medium_space(self, nodes_needed):
        fitting = [medium_space for medium_space in self.mid_job_spaces if len(medium_space) * self.size_z >= nodes_needed]
        fitting2 = [len(medium_space) * self.size_x for medium_space in self.mid_job_spaces if len(medium_space) * self.size_x >= nodes_needed]
        try:
            return min(fitting, key=lambda space: len(space))
        except ValueError:
            return None

    def _cuboid_strategy(self, job, cluster, no_cluster):
        node_list = []

        best_small = self._get_best_fit_for_small_space(job.nodes_needed)
        best_mid = self._get_best_fit_for_medium_space(job.nodes_needed)
        if best_small is not None:
            for x in xrange(job.nodes_needed):
                node_list.append(best_small.pop(0))
            if len(best_small) == 0:
                self.small_job_spaces.remove(best_small)

        elif best_mid is not None:
            columns_needed = int(ceil(1.0 * job.nodes_needed / self.size_z))

            if columns_needed == 1:
                for x in xrange(job.nodes_needed):
                    node_list.append(best_mid[0].pop(0))

                column_rest = best_mid.pop(0)
                if len(column_rest) > 0:
                    self.small_job_spaces.append(column_rest)

            else:
                for x in xrange(columns_needed):
                    node_list.extend(best_mid.pop(0))

            if len(best_mid) == 0:
                self.mid_job_spaces.remove(best_mid)


        else:
            self._cuboid_marker_y -= 1  # move to next whole layer

            height_needed = int(ceil(1.0 * job.nodes_needed / self.layer_size))
            height_available = self._cuboid_marker_y - self._zigzag_marker.y + int(not self._zigzag_started)

            if height_needed > height_available:
                raise BinTooSmallException
            if height_needed == 1:  # chance to split layer between multiple communication sensitive jobs
                columns_needed = int(ceil(1.0 * job.nodes_needed / self.size_z))

                if columns_needed == 1:
                    # create small job spaces
                    for z in xrange(self.anchor_point.z, self.anchor_point.z + job.nodes_needed):
                        node_list.append(Point3D(self.anchor_point.x, self._cuboid_marker_y, z))

                    small_job_space = []
                    for z in xrange(self.anchor_point.z + job.nodes_needed, self.anchor_point.z + self.size_z):
                        small_job_space.append(Point3D(self.anchor_point.x, self._cuboid_marker_y, z))
                    if small_job_space:
                        self.small_job_spaces.append(small_job_space)

                    mid_job_space = []
                    for x in xrange(self.anchor_point.x + columns_needed, self.anchor_point.x + self.size_x):
                        column = []
                        for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                            column.append(Point3D(x, self._cuboid_marker_y, z))
                        mid_job_space.append(column)
                    self.mid_job_spaces.append(mid_job_space)

                else:
                    # create mid job spaces
                    for x in xrange(self.anchor_point.x, self.anchor_point.x + columns_needed):
                        for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                            node = Point3D(x, self._cuboid_marker_y, z)
                            node_list.append(node)

                    mid_job_space = []
                    for x in xrange(self.anchor_point.x + columns_needed, self.anchor_point.x + self.size_x):
                        column = []
                        for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                            column.append(Point3D(x, self._cuboid_marker_y, z))
                        mid_job_space.append(column)
                    self.mid_job_spaces.append(mid_job_space)

            else:
                for x in xrange(self.anchor_point.x, self.anchor_point.x + self.size_x):
                    for z in xrange(self.anchor_point.z, self.anchor_point.z + self.size_z):
                        for y in xrange(self._cuboid_marker_y - height_needed + 1, self._cuboid_marker_y + 1):
                            node = Point3D(x, y, z)
                            node_list.append(node)

                self._cuboid_marker_y -= height_needed - 1

        if not no_cluster:
            job.posess_nodes(node_list)
