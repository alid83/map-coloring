import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw
import random


class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"

    def __str__(self):
        return self.value


def main():
    parser = argparse.ArgumentParser(
        prog="Map Coloring",
        description="Utilizing CSP to solve map coloring problem",
    )

    parser.add_argument(
        "-m",
        "--map",
        type=Continent,
        choices=list(Continent),
        help="Map must be: [Asia, Africa, America, Europe]",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-ac3",
        "--arc-consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )
    parser.add_argument(
        "-ND",
        "--Neighborhood-distance",
        type=int,
        default=1,
        help="The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors."
    )

    args = parser.parse_args()
    continent_str = str(args.map)
    neighborhood_dist = args.Neighborhood_distance

    # Generate borders for the specified continent
    borders = generate_borders_by_continent(continent=continent_str)
    # Create a CSP instance
    csp = CSP()

    # Add variables (regions) and their domains
    for region in borders:
        if neighborhood_dist == 1:
            csp.add_variable(region,
                             ["Red", "Yellow", "Blue", "Green"])
        else:
            csp.add_variable(region,
                             ["Red", "Yellow", "Blue", "Green", "Brown", "Khaki", "Silver", "Olive",
                              "White", "Cyan", "Orange", "Pink", "Magenta", "Lavender", "Black", "Teal", "Purple"])

    # Add constraints (borders between regions)
    for region, neighbors in borders.items():
        if not len(neighbors):
            csp.add_constraint(lambda x, y: x != y, [region, None])
            continue
        ND_neighbors = []
        for i in range(0, neighborhood_dist):
            for neighbor in neighbors:
                if neighbor in csp.variables and neighbor != region:
                    csp.add_constraint(lambda x, y: x != y, [region, neighbor])
                if neighbor in borders:
                    for x in borders[neighbor]:
                        if x not in ND_neighbors:
                            ND_neighbors.append(x)
            neighbors = ND_neighbors.copy()
    # Initialize the Solver
    solver = Solver(csp, domain_heuristics=args.lcv, variable_heuristics=args.mrv, AC_3=args.arc_consistency)

    solver.backtrack_solver()

    colors = []
    for color in csp.assignments.values():
        if color not in colors:
            colors.append(color)
    print(len(colors))
    draw(solution=csp.assignments, continent=str(args.map), assignments_number=csp.assignments_number)


if __name__ == '__main__':
    main()
