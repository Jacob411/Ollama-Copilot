-- local params = {
--     textDocument= {
--         uri = full_uri,
--     },
--     position = position,
-- }
--


function request_completions()
  -- Use the provided arguments instead of fetching them again
  local client_id = vim.lsp.get_clients()[3]['id']
  local client = vim.lsp.get_client_by_id(client_id)
  local cursor_loc = vim.api.nvim_win_get_cursor(0)
  local pos = {line = cursor_loc[1], character = cursor_loc[2]}
  local uri = vim.uri_from_bufnr(0)
  local comp_params = {
    textDocument = {
      uri = uri,
    },
    position = pos,
  }
  client.request('textDocument/completion', comp_params)
end

request_completions()
-- Bind the completion function to a keymap (optional)
vim.api.nvim_set_keymap('n', '<leader>cc', '<cmd>lua request_completions()<CR>', { noremap = true })

