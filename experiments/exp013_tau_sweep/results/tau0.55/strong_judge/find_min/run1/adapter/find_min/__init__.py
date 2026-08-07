# file: find_min/__init__.py
from candidate import make_bounded_finder as make_min
from candidate import min_any as get_min_with_many_arguments
from candidate import min_any_at_least_one as get_min_with_one_or_more_arguments
from candidate import min_no_argument as get_min_without_arguments
from candidate import min_single as get_min_with_one_argument
from candidate import min_two as get_min
from candidate import min_within_bounds as get_min_bounded
