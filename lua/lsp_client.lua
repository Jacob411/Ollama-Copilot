-- local params = {
--     textDocument= {
--         uri = full_uri,
--     },
--     position = position,
-- }
--


function request_completions()
  -- Use the provided arguments instead of fetching them again
  -- find client_id of ollama_lsp
  local clients = vim.lsp.get_clients()
  local client_id
  for _, client in ipairs(clients) do
    if client.name == "ollama_lsp" then
      client_id = client.id
    end
  end
  if not client_id then
    print('ollama_lsp not attached')
    return
  end

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

-- Bind the completion function to a keymap (optional)
-- vim.api.nvim_set_keymap('n', '<leader>cc', '<cmd>lua request_completions()<CR>', { noremap = true })

return {
  request_completions = request_completions
  }
