local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)
local ghost_text = require 'ghost_text'

lspconfig.custom_lsp.setup{
  capabilities = capabilities,
  handlers = {
    ["textDocument/completion"] = function(err, result, ctx, config)
      print("custom completion handler")
      print(vim.inspect(result))
      print(vim.inspect(ctx['params']['position']))
      line = ctx['params']['position']['line']
      col = ctx['params']['position']['character']
      local opts = ghost_text.build_opts_from_text(result[1]['insertText'])
      ghost_text.add_extmark(line, col, opts)
    end,
}
}


