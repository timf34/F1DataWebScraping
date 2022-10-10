from typing import Generator, Dict, List

from itertools import zip_longest
import itertools

class WorkingWithGenerators:
    def __init__(self):
        self.dict_of_generators: Dict[str, Generator] = {"a": self.yield_increasing_list("a"),
                                                         "b": self.yield_increasing_list("b")}

    def yield_increasing_list(self, string) -> Generator[List, None, None]:
        """
        Yields a list of increasing numbers
        """
        if string == "a":
            for i in range(10):
                yield i
        if string == "b":
            for i in range(10, 25):
                yield i

    def example(self):
        for i in self.dict_of_generators:
            print(i)
            for j in self.dict_of_generators[i]:
                print(j)

    def example_using_next(self):
        # Loop through each value in a generator once at a time (i.e. 1, 11, 2, 12, etc.)
        gens = []
        for i in self.dict_of_generators:
            gens.append(self.dict_of_generators[i])

        # Use next on the iterators, and finish when all iterators are exhausted (i.e. StopIteration), but note that
        # this will only work if all generators are the same length
        # while True:
        #     try:
        #         for gen in gens:
        #             print(next(gen))
        #     except StopIteration:
        #         break

        # In the case where the generators are not the same length, we can use a try/except block to catch the
        # StopIteration error, and then continue on to the next generator
        # while True:
        #     try:
        #         for gen in gens:
        #             print(next(gen))
        #     except StopIteration:
        #         continue

        # This is the only method that works for generators of different lengths
        # Another way to do this is to use zip_longest, which will fill in the missing values with None
        for i in zip_longest(*gens):
            print(i)


def main():
    working_with_generators = WorkingWithGenerators()
    working_with_generators.example_using_next()


if __name__ == "__main__":
    main()
