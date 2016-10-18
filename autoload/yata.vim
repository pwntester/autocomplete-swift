function! yata#run_if_needed()
    let l:result = _yata__run_if_needed()
    if has_key(l:result, 'error')
        :echoerr l:result.error.message
    endif
endfunction
