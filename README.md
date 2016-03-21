# autocomplete-swift

[![License][license-badge]][license]
[![Release][release-badge]][release]

Autocompletion for Swift in Vim, especially with [neocomplete][github-neocomplete].

![completion-gif](/_images/completion.gif)


## Installation

Autocomplete-swift uses [SourceKitten][github-sourcekitten] as its back-end.
Therefore this plugin supports OS X only.
SourceKitten can be installed with [Homebrew][github-homebrew].
Please execute the following coomand:

```bash
$ brew install sourcekitten
```

To install autocomplete-swift,
it is recommended to use plugin managers for Vim such as [NeoBundle][github-neobundle].
You can use autocomplete-swift via Vim's omni-completion,
but I recommend to use with [neocomplete][github-neocomplete] to enable autocompletion.

In the case of NeoBundle, please add the following codes into `.vimrc`:

```vim
NeoBundle 'mitsuse/autocomplete-swift'
NeoBundle 'Shougo/neocomplete.vim' " Optional, but recommended.
```

This plugin also supports jumping to placeholders in arguments of method.
The following configuration is required:

```vim
" Jump to the first placeholder by typing `<C-k>`.
autocmd FileType swift imap <buffer> <C-k> <Plug>(autocomplete_swift_jump_to_placeholder)
```

If you use [neosnippet][github-neosnippet],
you should enable [key-mappings of neosnippets][github-neosnippet-config] instead of using the above code.
Autocomplete-swift gets along with neosnippet by converting placeholders into its ones.


## Features

### Completion

The completion feature is available via several ways:

- Vim's omni-completion (typing `<C-x><C-o>` near `.`, `:`, `->` etc).
- Autocompletion with [neocomplete][github-neocomplete].

Autocomplete-swift supports types of completion as follow:

- Type name
- Type/Instance member
- Function/method parameter
- Top-level function/constant/variable
- Keyword such as `protocol`, `extension` etc.

This plugin provides completion in single file.
Frameworks/SDKs are not supported currently.


### Placeholder

This plugin supports jumping to placeholders in arguments of method.
Please add the following code into `.vimrc`:

```vim
" Jump to the first placeholder by typing `<C-k>`.
autocmd FileType swift imap <buffer> <C-k> <Plug>(autocomplete_swift_jump_to_placeholder)
```

If you use [neosnippet][github-neosnippet],
you should enable [key-mappings of neosnippets][github-neosnippet-config] instead of using the above code.
Autocomplete-swift gets along with neosnippet by converting placeholders into its ones.


## TODO

- Display more information of candidate (For example, the kind of candidate etc).
- Add support for framework/SDK by communicating with [SourceKittenDaemon][github-sourcekittendaemon].
- Add support for [neovim][web-neovim].


## Related project

In the GIF on the beginning,
I use snippets for Swift contained in [neosnippet-snippets][github-neosnippet-snippets]
in addition to autocomplete-swift.


## License

Please read [LICENSE][license].

[license-badge]: https://img.shields.io/badge/license-MIT-yellowgreen.svg?style=flat-square
[license]: LICENSE
[release-badge]: https://img.shields.io/github/tag/mitsuse/neocomplete-swift.svg?style=flat-square
[release]: https://github.com/mitsuse/neocomplete-swift/releases
[github-sourcekitten]: https://github.com/jpsim/SourceKitten
[github-sourcekittendaemon]: https://github.com/terhechte/SourceKittenDaemon
[github-homebrew]: https://github.com/Homebrew/homebrew
[github-neobundle]: https://github.com/Shougo/neobundle.vim
[github-neocomplete]: https://github.com/Shougo/neocomplete.vim
[github-neosnippet]: https://github.com/Shougo/neosnippet.vim
[github-neosnippet-config]: https://github.com/Shougo/neosnippet.vim#configuration
[github-neosnippet-snippets]: https://github.com/Shougo/neosnippet-snippets
[web-neovim]: https://neovim.io/
