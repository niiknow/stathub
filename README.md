# stathub
High performance, flat-file stats collection that support multi-tenancy with python and nginx

# strategy
> For high performance, live tracking of hit/counter, we put nginx in front because nginx is popular and battle tested.

![Market Share](https://blog.logrocket.com/wp-content/uploads/2021/10/w3-web-server-popularity-by-ranking.png)

NGINX docker container in docker-compose with config to log file as json: tenant-key-yyyy-MM-dd-hh-mm.json

```nginx
# placeholder
server {
  # stuff goes here

  if ($time_iso8601 ~ "^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})") {
    set $year $1;
    set $month $2;
    set $day $3;
    set $hour $4;
    set $minutes $5;
    set $seconds $6;
  }

  # this is reference to what all we can log 
  log_format main_json escape=json '{'
    '"msec": "$msec", ' # request unixtime in seconds with a milliseconds resolution
    '"connection": "$connection", ' # connection serial number
    '"connection_requests": "$connection_requests", ' # number of requests made in connection
    '"pid": "$pid", ' # process pid
    '"request_id": "$request_id", ' # the unique request id
    '"request_length": "$request_length", ' # request length (including headers and body)
    '"remote_addr": "$remote_addr", ' # client IP
    '"remote_user": "$remote_user", ' # client HTTP username
    '"remote_port": "$remote_port", ' # client port
    '"time_local": "$time_local", '
    '"time_iso8601": "$time_iso8601", ' # local time in the ISO 8601 standard format
    '"request": "$request", ' # full path no arguments if the request
    '"request_uri": "$request_uri", ' # full path and arguments if the request
    '"args": "$args", ' # args
    '"status": "$status", ' # response status code
    '"body_bytes_sent": "$body_bytes_sent", ' # the number of body bytes exclude headers sent to a client
    '"bytes_sent": "$bytes_sent", ' # the number of bytes sent to a client
    '"http_referer": "$http_referer", ' # HTTP referer
    '"http_user_agent": "$http_user_agent", ' # user agent
    '"http_x_forwarded_for": "$http_x_forwarded_for", ' # http_x_forwarded_for
    '"http_host": "$http_host", ' # the request Host: header
    '"server_name": "$server_name", ' # the name of the vhost serving the request
    '"request_time": "$request_time", ' # request processing time in seconds with msec resolution
    '"upstream": "$upstream_addr", ' # upstream backend server for proxied requests
    '"upstream_connect_time": "$upstream_connect_time", ' # upstream handshake time incl. TLS
    '"upstream_header_time": "$upstream_header_time", ' # time spent receiving upstream headers
    '"upstream_response_time": "$upstream_response_time", ' # time spend receiving upstream body
    '"upstream_response_length": "$upstream_response_length", ' # upstream response length
    '"upstream_cache_status": "$upstream_cache_status", ' # cache HIT/MISS where applicable
    '"ssl_protocol": "$ssl_protocol", ' # TLS protocol
    '"ssl_cipher": "$ssl_cipher", ' # TLS cipher
    '"scheme": "$scheme", ' # http or https
    '"request_method": "$request_method", ' # request method
    '"server_protocol": "$server_protocol", ' # request protocol, like HTTP/1.1 or HTTP/2.0
    '"pipe": "$pipe", ' # “p” if request was pipelined, “.” otherwise
    '"gzip_ratio": "$gzip_ratio", '
    '"http_cf_ray": "$http_cf_ray"'
  '}';

  # this is what we'll use
  log_format stathub_json escape=json '{'
    '"request": "$request", ' # full path no arguments if the request
    '"status": "$status", ' # response status code
    '"remote_addr": "$remote_addr", ' # client IP
    '"remote_user": "$remote_user", ' # client HTTP username
    '"time_iso8601": "$time_iso8601", ' # local time in the ISO 8601 standard format
    '"http_referer": "$http_referer", ' # HTTP referer
    '"http_user_agent": "$http_user_agent", ' # user agent
    '"http_x_forwarded_for": "$http_x_forwarded_for", ' # http_x_forwarded_for
    '"connection": "$connection", ' # connection serial number
    '"connection_requests": "$connection_requests", ' # number of requests made in connection
    '"request_time": "$request_time", ' # request processing time in seconds with msec resolution
    '"args": "$args", ' # args
  '}';
  # disable access log by default
  access_log off;

  # prevent good bot from scanning
  location = /robots.txt {
    add_header Content-Type text/plain;
    return 200 "User-agent: *\nDisallow: /\n";
  }

  # Replace 'prefix' with anything here
  # this act like buffer to prevent catching bad bot scan 
  location ~ ^/prefix/([a-z0-9]+)/([^/]+)$ {
    set $tenant    $1;
    set $key       $2;

    access_log /var/log/nginx/$tenant-$key-$year-$month-$day-$hour-$minutes.log stathub_json;

    return empty_gif;
  }
}
```

Python3 docker image with application access to docker sock.  This allow us to send `nginx -s reload` so we can get the latest summation of a count stat.

# Why Python?  Also, why JSON and not CSV or TSV?
> Why Python and not NodeJS or any other language?

So we can experiment with newest Python framework: FastAPI and hypercorn.  Also, python has great CSV parser.  If you want smaller file to save storage, you can store as TSV instead and parse the file.  We store as JSON to make it faster to return raw log data. Simply read in the file, replace all `}\n` with `},` and wrap it around `[]` to make it return array of json.

# MIT
