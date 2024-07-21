-- local params = {
--     textDocument= {
--         uri = full_uri,
--     },
--     position = position,
-- }
--

function get_client_id(client_name)
    local clients = vim.lsp.get_clients()
    local client_id
    for _, client in ipairs(clients) do
        if client.name == client_name then
            client_id = client.id
        end
    end
    return client_id
end

-- Function to cancel the current LSP request
function cancel_lsp_request()
    local client_id = get_client_id('ollama_lsp')
    if not client_id then
        print('ollama_lsp not attached')
        return
    end
    local client = vim.lsp.get_client_by_id(client_id)
    if client and client.requests then
        for id, _ in pairs(client.requests) do
            client.notify('$/cancelRequest', { id = id })
        end
    end
end

function request_completions()
  local client_id = get_client_id('ollama_lsp')
  if not client_id then
    print('ollama_lsp not attached')
    return
  end

  local client = vim.lsp.get_client_by_id(client_id)
  local cursor_loc = vim.api.nvim_win_get_cursor(0)
  local pos = {line = cursor_loc[1] - 1, character = cursor_loc[2]}
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
  request_completions = request_completions,
  cancel_lsp_request = cancel_lsp_request
  }
