from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP


class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False,
                 AC_3: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
        """
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.AC_3 = AC_3
        self.csp = csp

    def backtrack_solver(self) -> List[Tuple[str, str]]:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            List[Tuple[str, str]]: A list of variable-value assignments that satisfy all constraints.
        """
        # Add more debug output as needed

        removed = self.apply_AC3() if self.AC_3 else []

        if self.csp.is_complete():
            return list(self.csp.assignments.items())

        variable = self.select_unassigned_variable()
        for value in self.ordered_domain_value(variable):
            if self.csp.is_consistent(variable, value):
                if not self.csp.is_assigned(variable):
                    self.csp.assign(variable, value)
                    removed.extend(self.csp.remove_value(variable, value))
                    result = self.backtrack_solver()
                    if result is not None:
                        return result
                    self.csp.unassign(removed, variable)
                    removed = []

        return None

    def select_unassigned_variable(self) -> str:
        """
        Selects an unassigned variable using the MRV heuristic.

        Returns:
            str: The selected unassigned variable.
        """
        if self.variable_heuristic:
            return self.MRV()
        return self.csp.unassigned_var[0]

    def ordered_domain_value(self, variable: str) -> List[str]:
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (str): The name of the variable.

        Returns:
            List[str]: A list of domain values for the variable in a specific order.
        """
        # Function implementation goes here
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]

    def arc_reduce(self, x, y, consistent) -> List[str]:
        """
        Reduce the domain of variable x based on the constraints between x and y.

        Parameters:
        - x: The first variable.
        - y: The second variable.
        - consistent: A function that checks the consistency between two values.

        Returns:
        - The reduced domain of variable x if the domain is reduced, None otherwise.
        """
        removed_values = []


        for x_value in self.csp.variables[x]:
            if all(not consistent(x_value, y_value) for y_value in self.csp.variables[y]):
                self.csp.variables[x].remove(x_value)
                removed_values.append(x_value)
                if len(self.csp.variables[x]) == 0:
                    return removed_values
        return removed_values

    def apply_AC3(self) -> List[Tuple[str, str]]:
        """
        Applies the AC3 algorithm to reduce the domains of variables in the CSP.

        Returns:
            A list of tuples representing the removed values from the domain of variables.
        """
        removed_values = []
        queue = deque(self.csp.constraints)

        while queue:
            constraint, variables = queue.popleft()
            x, y = variables[0], variables[1]

            # Ensure x and y are valid variables (not lists or tuples)
            if not isinstance(x, str) or not isinstance(y, str):
                continue

            removed = self.arc_reduce(x, y, constraint)
            if removed is not None:
                for x_value in removed:
                    removed_values.append((x, x_value))
                if len(self.csp.variables[x]) == 0:
                    return removed_values

        return removed_values

    def MRV(self) -> str:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            str: The variable with the fewest remaining values.
        """
        # max_var = None
        # max_constraint_size = -1
        # for var in self.csp.unassigned_var:
        #     if len(self.csp.var_constraints[var]) > max_constraint_size:
        #         max_constraint_size = len(self.csp.var_constraints[var])
        #         max_var = var
        # return max_var
        min_size = float('inf')
        minVariable = None
        for var in self.csp.unassigned_var:
            if len(self.csp.variables[var]) < min_size:
                minVariable = var
                min_size = len(self.csp.variables[var])
        return minVariable

    def LCV(self, variable: str) -> List[str]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (str): The variable for which to order the values.

        Returns:
            List[str]: A list of values sorted based on the number of constraints they impose.
        """

        def count_constraints(value):
            count = 0
            if variable in self.csp.var_constraints:
                for constraint_func, related_vars in self.csp.var_constraints[variable]:
                    var = related_vars[1]
                    if var and not self.csp.is_assigned(var) and value in self.csp.variables[var]:
                        count += 1
            return count

        return sorted(self.csp.variables[variable], key=count_constraints)
        # domain_values = []
        # for value in ["#AD6456", "#12BC57", "#123458", "#CD3459", "#1EF45A", "#12345B", "#12345C", "#12345D",
        #                   "#12345E", "#223459", "#22345A", "#22345B", "#22345C", "#33345B", "#33345C"]:
        #     count = 0
        #     for constraint_fuc, neighbor in self.csp.var_constraints[variable]:
        #         if neighbor[1] and self.csp.is_assigned(neighbor[1]):
        #             if value in self.csp.variables[neighbor[1]]:
        #                 count += 1
        #     domain_values.append((value, count))
        # domain_values.sort(key=lambda x: x[1])
        # return [x[0] for x in domain_values]


