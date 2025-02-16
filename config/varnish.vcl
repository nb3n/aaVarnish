vcl 4.1;

backend default {
    .host = "127.0.0.1";
    .port = "8080";
}

sub vcl_backend_response {
    set beresp.ttl = {TTL}m; # Will be replaced by PHP
}