let s:port = -1

function! yata#enable(port)
    let s:port = a:port
endfunction

function! yata#disable()
    let s:port = -1
endfunction

function! yata#is_enabled()
    return yata#port() != -1
endfunction

function! yata#port()
    return s:port
endfunction
