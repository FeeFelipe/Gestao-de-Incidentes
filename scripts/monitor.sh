#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8080/health}"
echo "Monitoring ${URL} (Ctrl+C to stop)"
downtime_start=""
while true; do
  ts=$(date +'%Y-%m-%d %H:%M:%S')
  code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")
  if [[ "$code" != "200" ]]; then
    if [[ -z "$downtime_start" ]] ; then
      downtime_start="$ts"
      echo "[${ts}] DOWN (http ${code})"
    fi
  else
    if [[ -n "$downtime_start" ]]; then
      end_ts="$ts"
      echo "[${end_ts}] UP again"
      # GNU date (Linux) or gdate (macOS coreutils) for seconds
      if date -d "$downtime_start" +%s >/dev/null 2>&1; then
        start_sec=$(date -d "$downtime_start" +%s)
        end_sec=$(date -d "$end_ts" +%s)
      else
        start_sec=$(gdate -d "$downtime_start" +%s)
        end_sec=$(gdate -d "$end_ts" +%s)
      fi
      dur=$(( end_sec - start_sec ))
      echo "Downtime window: ${downtime_start} -> ${end_ts} (≈ ${dur}s)"
      downtime_start=""
    else
      echo "[${ts}] OK"
    fi
  fi
  sleep 1
done
