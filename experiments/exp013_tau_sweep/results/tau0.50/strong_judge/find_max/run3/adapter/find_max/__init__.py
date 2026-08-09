# file: find_max/__init__.py
from candidate import always_refuses as get_max_without_arguments
from candidate import make_bounded_finder as make_max
from candidate import max_of_any as get_max_with_many_arguments
from candidate import max_of_at_least_one as get_max_with_one_or_more_arguments
from candidate import max_of_one as get_max_with_one_argument
from candidate import max_of_two as get_max
from candidate import max_within_bounds as get_max_bounded
