import re
def strip_prefix(text, prefix): return re.sub(r'^{0}'.format(re.escape(prefix)), '', text)