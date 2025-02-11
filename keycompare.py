#!/usr/bin/env python3

import sys
import re
from collections import OrderedDict
from pprint import pprint

def main():
    log_line = 'github-unicorn.log:Feb 11 00:30:33 gm3dmo-056883d8cfdebc99a-qaboot-net github-unicorn[3615]: Timestamp="2025-02-11T00:30:33.370224Z" InstrumentationScope="GitHub" SeverityText="INFO" TraceId="bb7c696093880952a762c552abd87eeb" SpanId="f9f82fa02c36a5c0" ParentSpanId="0000000000000000" TraceFlags="01" time_zone="UTC" controller="SessionsController" action="new" now="2025-02-11T00:30:33+00:00" request_id="dc1ac59c-daf1-4d31-b0ad-789fc0258980" datacenter="default" server_id="486ea51b-de44-45e4-813d-2ec08db92223" remote_address="20.105.137.134" request_method="get" request_host="gm3dmo-056883d8cfdebc99a.qaboot.net" path_info="/login" content_length="0" content_type="text/html; charset=utf-8" user_agent="curl/8.6.0" accept="*/*" referer="https://gm3dmo-056883d8cfdebc99a.qaboot.net/" status="200" elapsed="0.07165982100195833" url="https://gm3dmo-056883d8cfdebc99a.qaboot.net/login" worker_request_count="11776" worker_pid="138" worker_number="0" request_category="other" allocations="22679" minor_gc_count="0" major_gc_count="0" gh.request_id="dc1ac59c-daf1-4d31-b0ad-789fc0258980" gh.actor.is_robot="false" http.host="gm3dmo-056883d8cfdebc99a.qaboot.net" http.scheme="https" http.method="get" http.target="/login" http.url="https://gm3dmo-056883d8cfdebc99a.qaboot.net/login" http.status_code="200" http.client_ip="20.105.137.134" http.server_name="486ea51b-de44-45e4-813d-2ec08db92223" http.request.header.referer="https://gm3dmo-056883d8cfdebc99a.qaboot.net/" http.request.header.accept="*/*" http.user_agent="curl/8.6.0" http.response.header.content_type="text/html; charset=utf-8" gh.sdk.name="github-telemetry-ruby" gh.sdk.version="0.49.8" service.name="github-unicorn" service.version="4a74a0f88570f0571aad9e2befe81fcb2763c2be" deployment.environment="production" host.name="gm3dmo-056883d8cfdebc99a-qaboot-net"'
    #log_line = 'one="1" two="2" zwei="2" three="3" drei="3" trois="3" four="4"'
    
    # Extract key-value pairs into an OrderedDict
    log_kv = OrderedDict()
    pattern = r'(\w+(?:\.\w+)*?)="(.*?)"'
    matches = re.findall(pattern, log_line)

    for key, value in matches:
        log_kv[key] = value

    # Create a dictionary where the keys are the values from log_kv
    # Each entry stores [count, [list_of_keys_that_share_this_value]]
    value_dict = {}
    for k, v in log_kv.items():
        if v not in value_dict:
            value_dict[v] = [0, []]
        value_dict[v][0] += 1
        value_dict[v][1].append(k)

    # Use pprint for readable output of value_dict
    pprint(value_dict)

    print("\nDuplicate values:")
    for val, (count, keys) in value_dict.items():
        if count > 1:
            print(f"Value: {val}, Count: {count}, Keys: {keys}")

if __name__ == "__main__":
    main()