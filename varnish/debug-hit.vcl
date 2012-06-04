include "debug-common-begin.vcl";

std.syslog(15, "vcl_hit(" + req.xid +
                ") ttl=" + obj.ttl +
                ", grace=" + obj.grace +
                ", hits=" + obj.hits +
                ", lastuse=" + obj.lastuse);

include "debug-common-end.vcl";
