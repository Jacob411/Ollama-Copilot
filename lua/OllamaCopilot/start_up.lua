local lspconfig = require 'lspconfig'
local capabilities = require('cmp_nvim_lsp').default_capabilities()
--local capabilities = vim.lsp.protocol.make_client_capabilities()
local ghost_text = require 'lua.OllamaCopilot.ghost_text'
local ollama_client = require 'lua.OllamaCopilot.lsp_client' 

local configs = require 'lspconfig.configs'
-- Check if the config is already defined (useful when reloading this file)
if not configs.ollama_lsp then
  configs.ollama_lsp = {
    default_config = {
      cmd = {'python3', "python/ollama_lsp.py" },
      filetypes = {'python', 'lua'},
      root_dir = function(fname)
        return lspconfig.util.find_git_ancestor(fname)
      end,
      settings = {},
      init_options = {
        config = {"TESTING THIS OUT"},
      },
    },
  }
end
function on_complete(err, result, ctx, config)
  local line = ctx['params']['position']['line']
  local col = ctx['params']['position']['character']
  local opts = ghost_text.build_opts_from_text(result[1]['inserttext'])
  ghost_text.add_extmark(line, col, opts) 
end


lspconfig.ollama_lsp.setup{

  capabilities = capabilities,
  on_attach = function(_, bufnr)
    vim.api.nvim_create_user_command("OllamaSuggestion", ollama_client.request_completions, {desc = "Get Ollama Suggestion"})    
    vim.api.nvim_create_user_command("OllamaAccept", ghost_text.accept_first_extmark_lines, {desc = "Accepts displayed Ollama Suggestion"})
    vim.api.nvim_create_user_command("OllamaReject", ghost_text.delete_first_extmark, {desc = "Rejects displayed Ollama Suggestion"})
    vim.api.nvim_create_user_command("OllamaCancel", ollama_client.cancel_lsp_request, {desc = "Cancels the current LSP request"})
     
  end,


  handlers = {
    ["textDocument/completion"] = function(err, result, ctx, config)
      local line = ctx['params']['position']['line']
      local col = ctx['params']['position']['character']
    end,
    ['$/tokenStream'] = function(err, result, ctx, config)
      local opts  = ghost_text.build_opts_from_text(result['completion']['total'])
      ghost_text.add_extmark(result['line'], result['character'], opts)
    end
}
}


vim.api.nvim_set_keymap('n', '<leader>o', '<Cmd>OllamaSuggestion<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>pm', '<Cmd>OllamaAccept<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>rm', '<Cmd>OllamaReject<CR>', { noremap = true })
vim.api.nvim_set_keymap('n', '<leader>cm', '<Cmd>OllamaCancel<CR>', { noremap = true })
vim.api.nvim_set_keymap('i', '<C-a>', '<Esc>:OllamaAccept<CR>a', {noremap = true, silent = true})
