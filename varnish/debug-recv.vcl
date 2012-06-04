include "debug-common-begin.vcl";

std.syslog(15, "vcl_recv(" + req.xid + ") " +
                "Debugging request " + client.ip + " -> " +
                server.ip + ":" + server.port + ", debuglevel=" +
                req.http.x-debug-level);
if (req.http.host) {
    std.syslog(15, "vcl_recv(" + req.xid + ") Req: " +
                    req.request + " http://" + req.http.host +
                    req.url + " " + req.proto);
} else {
    std.syslog(15, "vcl_recv(" + req.xid + ") Req: " +
                    req.request + " http://" + server.hostname +
                    req.url + " " + req.proto);
}
if (req.http.user-agent) {
    std.syslog(15, "vcl_recv(" + req.xid + ") User-Agent: " +
                    req.http.user-agent);
}
if (req.http.x-forwarded-for) {
    std.syslog(15, "vcl_recv(" + req.xid + ") X-Forwarded-For: " +
                    req.http.x-forwarded-for);
}
std.syslog(15, "vcl_recv(" + req.xid + ") Backend: " +
                req.backend + " (healthy=" + req.backend.healthy +
                ")");

include "debug-common-end.vcl";
