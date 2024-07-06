local lspconfig = require 'lspconfig'

local capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

lspconfig.custom_lsp.setup{
  capabilities = capabilities,
  handlers = {
    ["textDocument/completion"] = function(err, result, ctx, config)
      print("custom completion handler")
      print(vim.inspect(result))
      print(vim.inspect(ctx))
    end,
}
}


