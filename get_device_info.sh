#!/bin/bash
#
# Author:      Rix Woodling
# Created:     2024-10-10
# Description: Get system device information for local and remote systems.
# Last change: 2024-10-14, added CBI function
#


# help section
if [[ "$1" == "help" || "$1" == "--help" || "$1" == "-h" ]]; then
  echo "help"
  echo "local system --> ./get_device_info.sh                   "
  echo "output specs --> ./get_device_info.sh | tee myspecs.csv "
  echo "remote specs --> ./get_device_info.sh root@10.23.15.123 "
fi

# computer model name
function modelname {
echo -n "Model name,"
output=$(lscpu 2>/dev/null | grep "^Model name" | awk -F":" '{print $2}' | sed 's/^[ \t]*//')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# total system memory
function memorytotal {
echo -n "Mem Total,"
output=$(free -mh | grep "Mem" | awk '{print $2}')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# dmidecode memory details
function memoryinfo {
echo -n "Mem Type,"
output=$(dmidecode -t memory 2>/dev/null | grep "Type: " | tail -n1 | sed 's/.*: //')
[[ -n "$output" ]] && echo "$output" || echo ""
#
echo -n "Mem Speed,"
output=$(dmidecode -t memory 2>/dev/null | grep "Speed: " | tail -n1 | sed 's/.*: //')
[[ -n "$output" ]] && echo "$output" || echo ""
#
echo -n "Mem Rank,"
output=$(dmidecode -t memory 2>/dev/null | grep "Rank: " | tail -n1 | sed 's/.*: //')
[[ -n "$output" ]] && echo "$output" || echo ""
}


# version info for OS
function versionid {
echo -n "Version ID,"
output=$(cat /etc/os-release | grep "VERSION_ID" | awk -F"=" '{print $2}' | sed 's/\"//g')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# build release for OS
function buildid {
echo -n "Build ID,"
output=$(cat /etc/os-release | grep "BUILD_ID" | awk -F"=" '{print $2}')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# kernel release info
function kernel {
echo -n "Kernel Release,"
output=$(uname -r)
[[ -n "$output" ]] && echo "$output" || echo ""
}

# crossystem fwid info
function fwid {
echo -n "Active FW ID,"
output=$(crossystem 2>/dev/null | grep "fwid" | grep "Active" | awk -F" " '{print $3}')
[[ -n "$output" ]] && echo "$output" || echo ""
echo -n "Read-Only FW ID,"
output=$(crossystem 2>/dev/null | grep "fwid" | grep "Read-only" | awk -F" " '{print $3}')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# total cpus
function cputotal {
echo -n "CPU Total,"
output=$(lscpu 2>/dev/null | grep "^CPU(s):" | awk '{print $2}')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# cpu core count for each group
function cpucores {
cputotal=$(cat /proc/cpuinfo | grep "processor" | wc -l)
cores=$(for i in {0..13}; do cat /sys/devices/system/cpu/cpufreq/policy${i}/cpuinfo_max_freq 2>/dev/null; done | uniq -c | awk '{print $1}')
#
echo -n "P-cores (Logical),"
output=$(echo $cores | tr '\n' ' ' | awk '{print $1}' )
[[ -n "$output" ]] && echo "$output" || echo "0"
#
echo -n "E-cores,"
output=$(echo $cores | tr '\n' ' ' | awk '{print $2}' )
[[ -n "$output" ]] && echo "$output" || echo "0"
#
echo -n "LP-cores,"
output=$(echo $cores | tr '\n' ' ' | awk '{print $3}' )
[[ -n "$output" ]] && echo "$output" || echo "0"
}

# cpu max freq for each core group
function coremaxfreq {
cputotal=$(cat /proc/cpuinfo | grep "processor" | wc -l)
cores=$(for i in {0..13}; do cat /sys/devices/system/cpu/cpufreq/policy${i}/cpuinfo_max_freq 2>/dev/null; done | uniq | awk '{print $1}')
#
echo -n "P-cores (Logical),"
output=$(echo $cores | tr '\n' ' ' | awk '{print $1}' | awk '{printf "%.2f GHz\n", $1 / 1000000}')
[[ -n "$output" ]] && echo "$output" || echo "0"
#
echo -n "E-cores,"
output=$(echo $cores | tr '\n' ' ' | awk '{print $2}' | awk '{printf "%.2f GHz\n", $1 / 1000000}')
[[ -n "$output" ]] && echo "$output" || echo "0"
#
echo -n "LP-cores,"
output=$(echo $cores | tr '\n' ' ' | awk '{print $3}' | awk '{printf "%.2f GHz\n", $1 / 1000000}')
[[ -n "$output" ]] && echo "$output" || echo "0"
}

# max gfx frequency
function gfxmaxfreq {
echo -n "GFX max freq,"
output=$(cat /sys/class/drm/card?/gt_max_freq_mhz 2>/dev/null | awk '{printf "%.2f GHz\n", $1 / 1000}')
[[ -n "$output" ]] && echo "$output" || echo ""
}

# TME enabled boolean
function tme {
echo -n "TME enabled,"
output=$(inteltool -t 2>/dev/null | grep enabled | awk '{print $4}')
[[ -n "$output" ]] && echo "$output" || echo "NO"
}

# cbi settings
function cbi {
echo -n "CBI 2,"
output=$(ectool cbi get 2 | grep uint | cut -d" " -f3-)
[[ -n "$output" ]] && echo "$output" || echo ""

echo -n "CBI 6,"
output=$(ectool cbi get 6 | grep uint | cut -d" " -f3-)
[[ -n "$output" ]] && echo "$output" || echo ""

}

### MAIN ###

if [ -z "$1" ]; then
  # run functions locally
  modelname
  memorytotal
  memoryinfo
  versionid
  buildid
  kernel
  fwid
  cputotal
  cpucores
  coremaxfreq
  gfxmaxfreq
  tme
  cbi

else
  # add function to declare and echo to see remote system
  ssh -T "$1" "$(\
  declare -f modelname; \
  declare -f memorytotal; \
  declare -f memoryinfo; \
  declare -f versionid; \
  declare -f buildid; \
  declare -f kernel; \
  declare -f fwid; \
  declare -f cputotal; \
  declare -f cpucores; \
  declare -f coremaxfreq; \
  declare -f gfxmaxfreq; \
  declare -f cbi; \
  echo; \
  echo 'modelname; memorytotal; memoryinfo; versionid; buildid; kernel; fwid; cputotal; cpucores; coremaxfreq; gfxmaxfreq; cbi; exit')"

fi

#


