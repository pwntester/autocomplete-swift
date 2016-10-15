let s:host = 'localhost'
let s:port = -1

function! sourcekitten_daemon#enable(port)
    let s:port = a:port
    let s:address = 'http://' . s:host . ':' . s:port
endfunction

function! sourcekitten_daemon#disable()
    let s:port = -1
endfunction

function! sourcekitten_daemon#is_enabled()
    return sourcekitten_daemon#port() != -1
endfunction

function! sourcekitten_daemon#port()
    return s:port
endfunction
