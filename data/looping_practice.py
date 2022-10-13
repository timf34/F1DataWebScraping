from copy import deepcopy
from typing import Dict

import itertools

# TODO: note that this isn't getting anywhere. I need to change things up. A normal for loop wouldn't work as far as I
#  can see. I should have realized this sooner.
#  I should also have a look at the itertools module
#  For now, move on and just get something working.



class LoopingPractice:
    def __init__(self):
        self.samp_dict: Dict = {"A": {"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]},
                                "B": {"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]}}

        self.numbered_samp_dict = {"1": deepcopy(self.samp_dict), "2": deepcopy(self.samp_dict)}

    def iterate_through_nums(self):
        """
           We want to iterate through self.numbered_samp_dict such that we get the first next value from each list for
           A and B. And then the 2nd next value, and then the 3rd, and so on. So we want to get:
           The output would look like this: 1 A x 1, 1 A y 4, 1 A z 7, 2 A x 1, 2 A y 4, 2 A z 7, 1 A x 2, 1 A y 5, 1 A z 8, 2 A x 2, 2 A y 5, 2 A z 8, 1 A x 3, 1 A y 6, 1 A z 9, 2 A x 3, 2 A y 6, 2 A z 9, 1 B x 1, 1 B y 4, 1 B z 7, 2 B x 1, 2 B y 4, 2 B z 7, 1 B x 2, 1 B y 5, 1 B z 8, 2 B x 2, 2 B y 5, 2 B z 8, 1 B x 3, 1 B y 6, 1 B z 9, 2 B x 3, 2 B y 6, 2 B z 9

            We are essentially iterating across the lists, rather than through them - breadth wise
        """
        # for num in self.numbered_samp_dict.keys():
        #     for sector in self.samp_dict.keys():
        #         for action in self.samp_dict[sector].keys():
        #             for i in range(len(self.samp_dict[sector][action])):
        #                 print(num, sector, action, self.samp_dict[sector][action][i])

        # Now lets rewrite the above loop, so that the output looks like this:
        # > 1 A x 1, 1 A y 4, 1 A z 7, 2 A x 1, 2 A y 4, 2 A z 7, 1 A x 2, 1 A y 5, 1 A z 8, 2 A x 2, 2 A y 5, 2 A z 8, 1 A x 3, 1 A y 6, 1 A z 9, 2 A x 3, 2 A y 6, 2 A z 9, 1 B x 1, 1 B y 4, 1 B z 7, 2 B x 1, 2 B y 4, 2 B z 7, 1 B x 2, 1 B y 5, 1 B z 8, 2 B x 2, 2 B y 5, 2 B z 8, 1 B x 3, 1 B y 6, 1 B z 9, 2 B x 3, 2 B y 6, 2 B z 9
        # Use itertools to do this














def main():
    loop = LoopingPractice()
    loop.iterate_through_nums()


if __name__ == '__main__':
    main()

