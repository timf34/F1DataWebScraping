import numpy as np


class NPLinspacePractice:
    def __init__(self):
        self._list = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75, 14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75, 16.0, 16.25, 16.5, 16.75, 17.0, 31.198]
        self._other_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.interval = 0.25

    def convert_interval_of_list(self):
        first_value = 0
        last_value = self._list[-1]
        last_value = round(last_value / self.interval) * self.interval
        new_list = np.arange(first_value, last_value + self.interval, self.interval)
        print("len(new_list):", len(new_list))
        return new_list.tolist()

    def change_num_elements(self, num_elements):
        new_list = np.interp(np.linspace(0, len(self._list) - 1, num_elements), np.arange(len(self._list)), self._list)
        print(len(new_list))
        return new_list.tolist()

    def my_other_fun(self, difference, x, y):
        interval = 0.25
        # Add the difference (in time) to the last value of x.
        difference = 10

        x[-1] += difference
        last_value = x[-1]
        first_value = x[0]

        # Create a new list of x values with this new interval
        x = np.arange(first_value, last_value + interval, interval)

        # Change the number of elements in y to match the number of elements in x
        y = np.interp(np.linspace(0, len(y) - 1, len(x)), np.arange(len(y)), y)

        # Interpolate the y values, so that they're the same length as the new x values
        # new_y = np.interp(x, x, y)

        print(x)
        print(y)
        print(len(x))
        print(len(y))

    def run(self):
        # print(self.convert_interval_of_list())
        # print(self.change_num_elements(len(self.convert_interval_of_list())))
        self.my_other_fun(10, self._list, self._other_list)


if __name__ == "__main__":
    NPLinspacePractice().run()

