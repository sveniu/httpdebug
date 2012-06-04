include "debug-common-begin.vcl";

std.syslog(15, "vcl_miss(" + req.xid + ") Cache miss: " + bereq.url);
if (req.http.x-forwarded-for) {
    std.syslog(15, "vcl_miss(" + req.xid + ") " + 
                    "Backend will see X-Forwarded-For: " +
                    req.http.x-forwarded-for);
}

include "debug-common-end.vcl";
