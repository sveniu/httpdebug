include "debug-common-begin.vcl";

if (req.http.host) {
    std.syslog(15, "vcl_pass(" + req.xid + ") Backend (" +
                    req.backend + ") req: " + bereq.request +
                    " http://" + bereq.http.host + bereq.url +
                    " " + bereq.proto);
} else {
    std.syslog(15, "vcl_pass(" + req.xid + ") Backend (" +
                    req.backend + ") req: " + bereq.request +
                    " http://<backend>" + bereq.url +
                    " " + bereq.proto);
}

include "debug-common-end.vcl";
