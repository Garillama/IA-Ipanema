#!/usr/bin/env python3
"""Provider-free probes for the existing Bubblewrap isolation wrapper.
Uses only an ephemeral synthetic auth canary and a loopback sentinel. Never reads
real credentials, invokes Claude/Codex, or contacts any external address.
Set IPANEMA_CANDIDATE_ROOT to the isolated candidate checkout.
"""
import json, os, pathlib, socket, tempfile, threading
from ipanema.orchestration.isolation import run_isolated
root=pathlib.Path(os.environ['IPANEMA_CANDIDATE_ROOT']).resolve()
with tempfile.TemporaryDirectory(prefix='ipanema-bootstrap-design-probe-') as td:
    tmp=pathlib.Path(td); snapshot=tmp/'snapshot'; snapshot.mkdir()
    (snapshot/'fixture.txt').write_text('synthetic readonly fixture\n')
    fake=tmp/'synthetic-codex-auth.json'
    fake.write_text('{"token":"BOOTSTRAP-DUMMY-CANARY-ONLY"}\n')
    result=run_isolated(['/bin/cat','/worker-home/.codex/auth.json'],'',snapshot,
        provider='codex',auth_files={str(fake):'.codex/auth.json'},network=False,
        timeout=8,max_output_bytes=20000)
    credential={'finished':result.get('exit_code')==0,
        'fake_secret_visible_to_child': 'BOOTSTRAP-DUMMY-CANARY-ONLY' in result.get('stdout',''),
        'real_credentials_used':False,'provider_called':False}
    server=socket.socket();server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('127.0.0.1',0));server.listen(1);server.settimeout(.6);port=server.getsockname()[1]
    accepted=[]
    def accept():
        try:
            conn,_=server.accept();accepted.append(True);conn.close()
        except (TimeoutError,socket.timeout,OSError): pass
    thread=threading.Thread(target=accept,daemon=True);thread.start()
    py='import socket\ns=socket.socket();s.settimeout(.5)\ntry:s.connect(("127.0.0.1",'+str(port)+'));print("CONNECTED")\nexcept OSError:print("BLOCKED")'
    net=run_isolated(['/usr/bin/python3','-c',py],'',snapshot,provider='qa',network=False,
        timeout=8,max_output_bytes=20000)
    thread.join(1);server.close()
    network={'local_sentinel_blocked':'BLOCKED' in net.get('stdout',''),
        'sentinel_accepted':bool(accepted),'external_address_contacted':False,'provider_called':False}
    output={'credential_mount_probe':credential,'network_namespace_probe':network,
        'interpretation':'A read-only bind prevents writes but does not hide a readable mounted secret from a child command.'}
    print(json.dumps(output,indent=2))
    if not credential['fake_secret_visible_to_child'] or not network['local_sentinel_blocked'] or accepted:
        raise SystemExit(1)
