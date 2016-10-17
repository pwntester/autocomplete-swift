inoremap <silent><expr> <Plug>(autocomplete_swift_jump_to_placeholder) autocomplete_swift#jump_to_placeholder()

autocmd! FileType swift :call yata#run_if_needed()
