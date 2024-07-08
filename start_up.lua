local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)
local ghost_text = require 'ghost_text'
local ollama_client = require 'lsp_client' 

function on_complete(err, result, ctx, config)
  local line = ctx['params']['position']['line']
  local col = ctx['params']['position']['character']
  local opts = ghost_text.build_opts_from_text(result[1]['inserttext'])
  ghost_text.add_extmark(line, col, opts)
end

lspconfig.ollama_lsp.setup{
  capabilities = capabilities,
  on_attach = function(client, bufnr)
    vim.api.nvim_create_user_command("OllamaSuggestion", ollama_client.request_completions, {desc = "Will get a suggestion for the current cursor position and display it as ghost text"})    
  end,
  handlers = {
    ["textDocument/completion"] = function(err, result, ctx, config)
      print("custom completion handler")
      vim.inspect(err)
      print(vim.inspect(result))
      print(vim.inspect(ctx['params']['position']))
      local line = ctx['params']['position']['line']
      local col = ctx['params']['position']['character']
      local opts = ghost_text.build_opts_from_text(result[1]['insertText'])
      print('opts')
      print(vim.inspect(opts))
      ghost_text.add_extmark(line, col, opts)
    end,
}
}


vim.api.nvim_set_keymap('n', '<leader>o', '<Cmd>OllamaSuggestion<CR>', { noremap = true })
