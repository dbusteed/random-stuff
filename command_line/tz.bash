#!/bin/bash
#
# view /usr/share/zoneinfo
#

echo "Mountain: $(TZ=":US/Mountain" date +"%D %R")"
echo "   Tokyo: $(TZ=":Asia/Tokyo" date +"%D %R")"
echo "  Sydney: $(TZ=":Australia/Sydney" date +"%D %R")"
