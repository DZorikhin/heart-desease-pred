#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# Enable strict mode.
set -euo pipefail

# Temporarily disable strict mode and activate conda:
set +euo pipefail
conda activate ds

# Re-enable strict mode:
set -euo pipefail

# exec the final command:
# exec gunicorn --bind=0.0.0.0:9696 predict:app
exec gunicorn --bind 0.0.0.0:$PORT predict:app