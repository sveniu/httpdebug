include "debug-common-begin.vcl";

std.syslog(15, "vcl_fetch(" + req.xid + ") " + 
                "Backend response complete: " + beresp.backend.name + " (" +
                beresp.backend.ip + ":" + beresp.backend.port + "): " +
                beresp.status + " " + beresp.response + ", ttl=" + beresp.ttl +
                ", grace=" + beresp.grace);

include "debug-common-end.vcl";
