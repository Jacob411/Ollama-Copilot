
local id_2 = vim.lsp.get_clients()[3]['id'] -- Replace with your client ID
print(vim.inspect(id_2))

local lsp_client = vim.lsp.get_client_by_id(id_2)
print(vim.inspect(lsp_client['name']))

local cursor = vim.api.nvim_win_get_cursor(0)
local position = {line = cursor[1], character = cursor[2]} -- Convert to zero-based indexing

full_uri = vim.uri_from_bufnr(0)
print(vim.inspect(full_uri))

local params = {
    textDocument= {
        uri = full_uri,
    },
    position = position,
}

completions = lsp_client.request('textDocument/completion', params)
print(vim.inspect(completions))


local ghost_text = require('ghost_text') 
ghost_text.add_extmark()

function request_completions()
  -- Use the provided arguments instead of fetching them again
  local client_id = vim.lsp.get_clients()[3]['id']
  local client = vim.lsp.get_client_by_id(client_id)
  local cursor_loc = vim.api.nvim_win_get_cursor(0)
  local pos = {line = cursor_loc[1], character = cursor_loc[2]}

  local comp_params = {
    textDocument = {
      uri = full_uri,
    },
    position = pos,
  }
  local success = client.request('textDocument/completion', comp_params)
end

request_completions()
-- Bind the completion function to a keymap (optional)
vim.api.nvim_set_keymap('n', '<leader>cc', '<cmd>lua request_completions()<CR>', { noremap = true })

