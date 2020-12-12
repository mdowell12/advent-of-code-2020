from solutions.get_inputs import read_inputs


class Ship(object):

    HEADING_TO_DIRECTION = {
        0: "E",
        90: "N",
        180: "W",
        270: "S"
    }

    def __init__(self):
        self.heading = 0  # Degrees, zero representing east
        self.position = [0, 0]
        self.starting_position = [0, 0]
        self.waypoint = [10, 1]

    def go(self, inputs):
        for line in inputs:
            direction = line.strip()[0]
            increment = int(line.strip()[1:])
            self.move(direction, increment)
            # print(direction, increment, self.position, self.heading)
        return self.distance_traveled()

    def go2(self, inputs):
        for line in inputs:
            direction = line.strip()[0]
            increment = int(line.strip()[1:])
            self.move2(direction, increment)
            # print(direction, increment, self.position, self.waypoint)
        return self.distance_traveled()

    def move(self, direction, increment):
        if direction in set(["N", "E", "S", "W"]):
            self.position = self.get_new_position(self.position, direction, increment)
        elif direction == "F":
            compass_direction = self.HEADING_TO_DIRECTION[self.heading % 360]
            self.position = self.get_new_position(self.position, compass_direction, increment)
        elif direction == "L":
            self.heading += increment
        elif direction == "R":
            self.heading -= increment

    def move2(self, direction, increment):
        if direction in set(["N", "E", "S", "W"]):
            self.waypoint = self.get_new_position(self.waypoint, direction, increment)
        elif direction == "F":
            x, y = self.position
            waypoint_x, waypoint_y = self.waypoint
            x_inc = (waypoint_x - x) * increment
            y_inc = (waypoint_y - y) * increment
            self.waypoint = [waypoint_x + x_inc, waypoint_y + y_inc]
            self.position = [x + x_inc, y + y_inc]
        elif direction == "L" or direction == "R":
            self.rotate_waypoint_around_ship(direction, increment)

    def rotate_waypoint_around_ship(self, direction, increment):
        effective_increment = increment % 360

        if effective_increment == 0:
            # Nothing to do
            pass
        elif effective_increment == 180:
            # All 180s are two 90 rights
            self.rotate_waypoint_90_right()
            self.rotate_waypoint_90_right()
        elif effective_increment == 90:
            if direction == "R":
                self.rotate_waypoint_90_right()
            elif direction == "L":
                # 90 degree left is same as three rights
                self.rotate_waypoint_90_right()
                self.rotate_waypoint_90_right()
                self.rotate_waypoint_90_right()
        elif effective_increment == 270:
            # 270 right is three 90 rights
            if direction == "R":
                self.rotate_waypoint_90_right()
                self.rotate_waypoint_90_right()
                self.rotate_waypoint_90_right()
            elif direction == "L":
                # 270 left is 90 right
                self.rotate_waypoint_90_right()

    def rotate_waypoint_90_right(self):
        waypoint_x, waypoint_y = self.waypoint
        boat_x, boat_y = self.position
        # Normalize as if boat is at [0,0]
        diff_x, diff_y = waypoint_x - boat_x, waypoint_y - boat_y
        new_diff_x, new_diff_y = diff_y, -1 * diff_x
        self.waypoint = [boat_x + new_diff_x, boat_y + new_diff_y]

    @staticmethod
    def get_new_position(position, compass_direction, increment):
        x, y = position
        if compass_direction == "E":
            return [x + increment, y]
        if compass_direction == "W":
            return [x - increment, y]
        if compass_direction == "N":
            return [x, y + increment]
        if compass_direction == "S":
            return [x, y - increment]
        raise Exception()

    def distance_traveled(self):
        horizontal = abs(self.position[0] - self.starting_position[0])
        vertical = abs(self.position[1] - self.starting_position[1])
        return horizontal + vertical


def run_1(inputs):
    return Ship().go(inputs)


def run_2(inputs):
    return Ship().go2(inputs)


def run_tests():
    test_inputs = """
    F10
    N3
    F7
    R90
    F11
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 25:
        raise Exception(f"Test 1 did not past, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 286:
        raise Exception(f"Test 2 did not past, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(12)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
