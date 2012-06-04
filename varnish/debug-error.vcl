include "debug-common-begin.vcl";

std.syslog(15, "vcl_error(" + req.xid + ") " + obj.status + " " + obj.response);

include "debug-common-end.vcl";
