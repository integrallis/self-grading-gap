# file: find_max/__init__.py
from candidate import find_max as get_max
from candidate import find_max_in_bounds as get_max_bounded
from candidate import find_max_any_count as get_max_with_many_arguments
from candidate import find_max_single as get_max_with_one_argument
from candidate import find_max_at_least_one as get_max_with_one_or_more_arguments
from candidate import find_max_no_args as get_max_without_arguments
from candidate import make_bounded_finder as make_max
